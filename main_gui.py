import threading
import tkinter as tk
from tkinter import ttk, messagebox

for name in dir(tk):
    cls = getattr(tk, name)
    if isinstance(cls, type) and hasattr(cls, "__del__"):
        try:
            cls.__del__ = lambda self: None
        except Exception:
            pass
import io, sys

import eda_analysis
import model_training
import gpt_analysis


# GUI 메인 윈도우 설정
root = tk.Tk()
root.title("대통령 선거 예측 프로그램")
root.geometry("600x500")
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

# EDA 실행 함수
def run_eda():
    eda_analysis.run()

# ML 예측 실행 함수
def run_model():
    model_type = selected_model.get()
    try:
        model_training.run(model_type)
    except Exception as e:
        messagebox.showerror("오류", f"머신러닝 예측 중 오류 발생: {e}")

def run_gpt_async():
    loading = tk.Toplevel(root)
    loading.title("로딩 중")
    ttk.Label(loading, text="GPT 분석 중입니다...", font=("Segoe UI", 12)).pack(padx=20, pady=20)
    loading.geometry("200x100")
    loading.transient(root)
    loading.grab_set()

    def task():
        err = None
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            gpt_analysis.run()
        except Exception as e:
            err = e
        finally:
            sys.stdout = old_stdout
            result_text = buf.getvalue()
            def on_done():
                loading.destroy()
                if err:
                    messagebox.showerror("오류", f"GPT 분석 호출 중 오류 발생: {err}")
                else:
                    popup = tk.Toplevel(root)
                    popup.title("GPT 분석 결과")
                    popup.geometry("800x600")  # 창 크기 확대
                    popup.configure(bg="#ffffff")
                    # 결과 텍스트 표시
                    text = tk.Text(popup, wrap='word', font=("Segoe UI", 14), bg="#ffffff")
                    text.insert('1.0', result_text)
                    text.config(state='disabled')
                    # 줄 간격 태그 설정
                    text.tag_configure("spacing", spacing1=4, spacing3=4)
                    text.tag_add("spacing", "1.0", "end")
                    text.pack(fill='both', expand=True, padx=10, pady=10)
                    # 스크롤바
                    scrollbar = ttk.Scrollbar(popup, orient='vertical', command=text.yview)
                    text['yscrollcommand'] = scrollbar.set
                    scrollbar.pack(side='right', fill='y')
            root.after(0, on_done)

    threading.Thread(target=task, daemon=True).start()

# GPT 실행 함수
def run_gpt():
    run_gpt_async()


# 버튼들
btn_eda = ttk.Button(root, text="탐색적 데이터 분석 (EDA)", command=run_eda)
btn_eda.pack(pady=10)

btn_model = ttk.Button(root, text="머신러닝 예측 실행", command=run_model)
btn_model.pack(pady=10)

btn_gpt = ttk.Button(root, text="GPT 분석 실행", command=run_gpt)
btn_gpt.pack(pady=10)

btn_quit = ttk.Button(root, text="종료", command=root.quit)
btn_quit.pack(pady=20)

root.mainloop()
