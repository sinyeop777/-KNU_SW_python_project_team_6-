import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import model_training
import eda_analysis

# GUI 메인 윈도우 설정
root = tk.Tk()
root.title("대통령 선거 예측 프로그램")
root.geometry("500x450")
root.configure(bg="#f0f4f8")

# 스타일 설정
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 14), background="#f0f4f8")

# 타이틀 라벨
title_label = ttk.Label(root, text="🗳️ 대통령 선거 예측 시스템", font=("Helvetica", 18, "bold"))
title_label.pack(pady=30)

# 모델 선택 라벨
model_label = ttk.Label(root, text="📊 사용할 머신러닝 모델을 선택하세요:")
model_label.pack(pady=5)

# 드롭다운 메뉴 생성
model_options = ["LinearRegression", "DecisionTree", "RandomForest", "KNN", "SVR"]
selected_model = tk.StringVar(value=model_options[0])
model_menu = ttk.Combobox(root, textvariable=selected_model, values=model_options, state="readonly", font=("Helvetica", 12))
model_menu.pack(pady=10)

# 실행 버튼 정의
def run_model():
    model_type = selected_model.get()
    model_training.run(model_type)

# EDA 실행 함수
def run_eda():
    eda_analysis.run()

# 버튼들
ttk.Button(root, text="탐색적 데이터 분석 (EDA)", command=run_eda).pack(pady=10)
ttk.Button(root, text="머신러닝 예측 실행", command=run_model).pack(pady=10)
ttk.Button(root, text="종료", command=root.quit).pack(pady=20)

# GUI 루프 실행
root.mainloop()
