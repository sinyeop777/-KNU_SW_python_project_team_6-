import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from sqlalchemy import create_engine

# ✅ 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def run():
    print("▶ 탐색적 데이터 분석 시작 중...\n")

    # ✅ MySQL 연결
    engine = create_engine("mysql+mysqlconnector://root:hanover109%40%40@127.0.0.1:3306/pp")
    poll_df = pd.read_sql("SELECT * FROM pp1", engine)

    # ✅ 엑셀 불러오기
    result_df = pd.read_excel("elec_result.xlsx", header=None)
    result_df.columns = ['elec_num', 'cand_num', 'cand_name', 'actual_rate']

    # ✅ 마지막 여론조사 + 실제 결과 비교 출력
    last_poll_df = poll_df.sort_values(by='date').groupby(['elec_num', 'cand_num', 'cand_name']).tail(1)
    compare_df = pd.merge(last_poll_df, result_df, on=['elec_num', 'cand_num', 'cand_name'])
    compare_df['gap'] = compare_df['actual_rate'] - compare_df['rate']

    print("▶ [후보별 실제 지지율과 마지막 여론조사 비교]")
    print(compare_df[['elec_num', 'cand_name', 'rate', 'actual_rate', 'gap']])

    # ✅ 후보별 고정 색상 매핑
    all_names = poll_df['cand_name'].unique()
    palette = sns.color_palette("tab10", len(all_names))
    name_color_map = dict(zip(all_names, palette))

    # ✅ 모든 선거 그래프를 하나의 창에 2x2 형태로 표시
    elec_nums = sorted(poll_df['elec_num'].unique())
    total = len(elec_nums)
    cols = 2
    rows = (total + 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(14, 6 * rows))
    axes = axes.flatten()

    for idx, elec in enumerate(elec_nums):
        sub_df = poll_df[poll_df['elec_num'] == elec]
        actual_sub = result_df[result_df['elec_num'] == elec]
        ax = axes[idx]

        for name in sub_df['cand_name'].unique():
            df = sub_df[sub_df['cand_name'] == name]
            ax.plot(df['date'], df['rate'], label=name, marker='o', color=name_color_map[name])

        for _, row in actual_sub.iterrows():
            ax.axhline(y=row['actual_rate'], linestyle='--', linewidth=1.2,
                       color=name_color_map.get(row['cand_name'], 'gray'),
                       label=f"{row['cand_name']} 실제({row['actual_rate']}%)")

        ax.set_title(f"{elec}대 대선 여론조사 vs 실제 투표율")
        ax.set_xlabel("날짜")
        ax.set_ylabel("지지율 (%)")
        ax.tick_params(axis='x', labelrotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.legend(loc='best', fontsize=8)

    # 불필요한 subplot 제거
    for j in range(idx + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    plt.show()

if __name__ == "__main__":
    run()
