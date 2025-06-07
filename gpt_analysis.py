import pandas as pd
import openai

# Hard coded OpenAI API key
openai.api_key =  " "

import pandas as pd
import openai

# 선거 전제 정보
PREMISE = (
    "제21대 대통령 선거는 여당 소속 대통령이 탄핵되어 치러진 선거입니다."
)

# 후보자 정보 테이블을 시스템 프롬프트에 포함하기 위한 상수
CANDIDATE_INFO = '''
대한민국 제21대 대통령 선거 주요 후보자 정보 (2025년 6월 3일 기준)

후보자 (이름) | 소속 정당 (여당/야당) | 현직 여부 | 최신 경제지표(실업률/물가상승률/1분기 GDP 성장률) | 주요 정책 테마
---|---|---|---|---
이재명 | 더불어민주당 (야당) | 현직 국회의원 (당 대표) | 2.9% / 1.9% / -0.2% | 헌정질서 회복·권력기관 개혁, 민생 경제 회복·AI 신산업 육성, 행복 증진·복지 강화, 한반도 평화·안보 강화
김문수 | 국민의힘 (여당) | 신인 (전 경기지사) | 2.9% / 1.9% / -0.2% | 자유주도 경제성장·기업 친화, 첨단산업 육성, 청년·주거 지원, 튼튼한 안보
이준석 | 개혁신당 (야당) | 신인 (전 당대표) | 2.9% / 1.9% / -0.2% | 행정 개혁·여가부 폐지, 리쇼어링·지방 세제 권한 이양, 연금·노동 개혁, 청년·교육 지원
권영국 | 민주노동당 (야당) | 신인 (노동변호사) | 2.9% / 1.9% / -0.2% | 노동권 강화·불평등 해소, 증세·복지 확대, 사회 정의·차별 해소, 기후·농어민 대책
황교안 | 무소속 (야당 성향) | 신인 (전 국무총리) | 2.9% / 1.9% / -0.2% | 부정선거 척결, 강경 노조 대응·법치 강화, 대공수사권 강화·국방력 확보, 보수 가치 강화
송진호 | 무소속 (야당 성향) | 신인 (기업인) | 2.9% / 1.9% / -0.2% | 가상자산 활성화·블록체인, 건설 경기 부양, 청년·중산층 지원, 지역 발전 전략
'''

def construct_prompt(poll_df: pd.DataFrame, pred_df: pd.DataFrame) -> str:
    """
    poll_df: DataFrame with ['cand_name','rate'] raw survey rates
    pred_df: DataFrame with ['cand_name','pred_rate'] ML predicted rates
    """
    lines = [
        '다음은 과거 대선 후보 별 득표율 데이터입니다:'
    ]
    for _, row in poll_df.iterrows():
        lines.append(f"- {row['cand_name']}: 후보 별 득표율 {row['rate']:.2f}%")

    lines.append('다음은 머신러닝 모델이 예측한 대통령 당선 확률 (predictions_latest.csv)입니다:')
    for _, row in pred_df.iterrows():
        lines.append(f"- {row['cand_name']}: 예측 당선 확률 {row['pred_rate']:.2f}%")

    lines.extend([
        '숫자는 % 단위만 사용, 900자 이내로 응답해주세요',
        '위 두 데이터를 바탕으로 다음을 수행해주세요:',
        '1) 먼저 득표율 데이터를 기반으로 최종 당선자가 누구인지 결론과 당선 확률(%)을 간단히 제시해주세요.',
        '2) 그 결론의 근거를 간략하게 설명해주세요.',
        '3) 이후 더 자세한 분석을 제공해주세요: 머신러닝 예측 결과와의 차이, 시사점을 포함해주세요.'
    ])

    return f"{CANDIDATE_INFO}\n" + "\n".join(lines)


def run():
    # 1) Raw survey data from pp1.csv
    try:
        df = pd.read_csv(
            "pp1.csv",
            header=None,
            names=['elec_num','cand_num','cand_name','rate','date']
        )
        poll_df = df[df['elec_num'] == 21][['cand_name', 'rate']]
    except Exception as e:
        print(f"❌ CSV에서 raw 데이터 읽기 실패: {e}")
        return

    if poll_df.empty:
        print("❌ 대선 raw 데이터가 없습니다 (pp1.csv).")
        return

    # 2) ML predictions data
    try:
        pred_df = pd.read_csv("data/predictions_latest.csv")
    except Exception as e:
        print(f"❌ CSV에서 예측 결과 읽기 실패: {e}")
        return

    if not {'cand_name','pred_rate'}.issubset(pred_df.columns):
        print("❌ predictions_latest.csv에 필요한 컬럼이 없습니다: cand_name, pred_rate")
        return

    # 3) Construct prompt
    prompt = construct_prompt(poll_df, pred_df)

    # 4) Call GPT
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": "당신은 정치분석 전문가입니다. 아래 후보자 정보를 전제로 분석하세요:"},
                {"role": "system", "content": PREMISE},
                {"role": "system", "content": CANDIDATE_INFO},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
    except Exception as e:
        print(f"❌ OpenAI 호출 오류: {e}")
        return

    # 5) Print result
    result = response.choices[0].message.content
    print("\n▶ GPT 분석 결과:\n")
    print(result)

if __name__ == "__main__":
    run()