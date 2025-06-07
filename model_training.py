import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
import numpy as np

# ✅ 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def get_processed_data():
    print("▶ 탐색적 데이터 분석 시작 중...\n")

    # ✅ MySQL 연결
    engine = create_engine("mysql+mysqlconnector://root:cks3148@127.0.0.1:3306/pp")
    poll_df = pd.read_sql("SELECT * FROM pp1", engine)

    # ✅ 엑셀 불러오기
    result_df = pd.read_excel("elec_result.xlsx", header=None)
    result_df.columns = ['elec_num', 'cand_num', 'cand_name', 'actual_rate']

    # ✅ 마지막 여론조사 + 실제 결과 비교 출력
    last_poll_df = poll_df.sort_values(by='date').groupby(['elec_num', 'cand_num', 'cand_name']).tail(1)
    compare_df = pd.merge(last_poll_df, result_df, on=['elec_num', 'cand_num', 'cand_name'])
    compare_df['gap'] = compare_df['actual_rate'] - compare_df['rate']

    return poll_df, result_df, compare_df

def run(model_type="LinearRegression"):
    print(f"\n▶ 선택된 모델: {model_type} - 예측 시작...\n")

    model_dict = {
        "LinearRegression": LinearRegression(),
        "DecisionTree": DecisionTreeRegressor(),
        "RandomForest": RandomForestRegressor(),
        "KNN": KNeighborsRegressor(n_neighbors=3),
        "SVR": SVR()
    }

    if model_type not in model_dict:
        print("❌ 지원하지 않는 모델입니다. LinearRegression / DecisionTree / RandomForest / KNN / SVR 중 선택하세요.")
        return

    model = model_dict[model_type]

    # ✅ 전처리 데이터 활용
    poll_df, result_df, _ = get_processed_data()

    train_df = poll_df[poll_df['elec_num'] < 21]
    last_train = train_df.sort_values(by='date').groupby(['elec_num', 'cand_num']).tail(1)
    merged_train = pd.merge(last_train, result_df, on=['elec_num', 'cand_num'])

    X_train = merged_train[['rate']]
    y_train = merged_train['actual_rate']

    test_df = poll_df[poll_df['elec_num'] == 21]
    last_test = test_df.sort_values(by='date').groupby(['elec_num', 'cand_num', 'cand_name']).tail(1)
    X_test = last_test[['rate']]
    cand_names = last_test['cand_name'].values

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred = np.clip(y_pred, 0, 100)

    print("▶ 21대 대선 후보별 예측 지지율\n")
    for name, pred in zip(cand_names, y_pred):
        print(f"🗳️ {name} 예측 지지율: {round(pred, 2)}%")

    plt.figure(figsize=(8, 8))
    plt.pie(y_pred, labels=cand_names, autopct='%1.1f%%', startangle=140)
    plt.title(f"21대 대선 후보 예측 지지율 ({model_type})")
    plt.tight_layout()
    plt.show()
    
    pred_df = last_test[['elec_num','cand_num','cand_name']].copy()
    pred_df['pred_rate'] = y_pred

    actual_df = pd.read_csv("2025_prediction_results.csv")
    actual_df = actual_df[['elec_num','cand_num','cand_name','final_rate']] \
                     .rename(columns={'final_rate':'actual_rate'})

    save_df = pd.merge(actual_df, pred_df,
                       on=['elec_num','cand_num','cand_name'])

    os.makedirs("data", exist_ok=True)

    csv_path = "data/predictions_latest.csv"
    json_path = "data/predictions_latest.json"
    save_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    save_df.to_json(json_path, orient='records', force_ascii=False, indent=2)

    print(f"\n▶ 결과를 저장 했습니다: {csv_path}, {json_path}")

if __name__ == "__main__":
    run()
