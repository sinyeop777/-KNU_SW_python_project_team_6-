# -KNU_SW_python_project_team_6-
대선 예측 프로그램
1. 데이터 수집, 출처: 중앙선거관리위원회(https://www.nec.go.kr/site/vt/main.do), 중앙선거여론조사심의위원회(https://www.nesdc.go.kr/portal/main.do)
2. 데이터 처리: 여론조사 결과 문서 내 표 분석, 데이터 수치화 - DB삽입. (후보 별 통합 지지율, 연령 별 후보 지지율 등..) 
3. 탐색적 데이터 분석: 1. 데이터 분포 확인 2. 범주형 데이터 시각 3. 변수 간 관계 분석 4. 데이터 변환 및 특성 엔지니어링
4. 모델링 및 분석: Scikit-Learn(sklearn)사용, 머신러닝 모델 학습, 분류 모델 예제
5. 결과 시각화 및 인사이트 노출: 실제 값과 예측 값 비교, 모델 성능 평가
6. 생성형 AI와의 추론 비교: 사람이 만든 수학적 모델 vs 언어 모델(GPT), 예상 OPENAPI는 결과를 기반으로 인과관계나 정치적 맥락을 도출해낼 수 있을거라 예상  

사용한 라이브러리
GUI( 기본 인터페이스 ) :  `tkinter`                                                       
EDA( 데이터 시각화, 통계분석 ) :  `pandas`, `matplotlib`, `seaborn`, `plotly`, `pandas_profiling`
DB( MySQL 연동 ) : `mysql-connector-python` 또는 `sqlalchemy`                        
ML( 예측모델, 해석력 ): `scikit-learn`, `xgboost`, `shap`                               
GPT형 보조( EDA 해석 보조 (옵션) ): `transformers`, `openai`                                        

사용방법
1. pp1.sql문, elec_result.xlsx, 2025_prediction_results, elec_result를 다운받는다
2. main_gui.py, eda_analysis.py, model_traing.py, gpt_analysis.py 를 다운받는다.
3. main_gui.py 를 실행 시키면 프로그램의 작동이 시작됩니다.

목적
갑작스러운 이슈로 인해 대선이 앞당겨져 많은 사람들이 관심을 가지고 있습니다. 수많은 뉴스와 여론 조사들이 쏟아지는 가운데,
이러한 정보를 바탕으로 국민 여론과 데이터의 상관관계를 분석하고, 대선을 예측하는 프로그램을 만들어 실제 결과와의 유사성을 
검증해보고자 합니다.

기능
1. EDA를 활용한 18대, 19대, 20대, 21대 대선의 여론조사 지지율과 실제 지지율을 표로 한눈에 볼 수 있습니다.
2. EDA를 활용한 정보를 바탕으로 5가지의 러닝 머신 모델을 사용해서 21대 대선의 지지율을 예측할 수 있습니다.
3. 이를 통해 각 러닝 머신 모델의 특징을 공부할 수 있고, 실제 지지율에 근접한 모델을 확인할 수 있습니다.
4. GPT API를 활용하여, 여론 조사와 실제 지지율의 상관관계만을 분석한 것에 그치지 않고 동일한 데이터를
   GPT에게 주고 어떻게 분석할 것인지, GPT는 더 다양한 데이터를 가지고 올 수 있기에 지지율 예측에
   다양한 시각을 제공해 줄 수 있습니다.

개선할점
1. 단순한 UI
2. 모자란 표본조사 데이터
3. 다양한 변수(정치적 상황, 사건사고)들 고려

재밌었던 점
1. 이번 학기 인공지능개론에서 배웠던 다양한 회귀 분석을 실제로 사용해 볼 수 있어서 좋았습니다.
2. 랜덤 포레스트 회귀를 사용한 모델이 실제 득표율과 비슷한 결과를 내어서 재미있었고,
   왜 그러한 결과를 나왔는지 공부하는 것도 유익한 시간이었습니다.
4. GPT로 확인한 분석이 매우 정확한 것에 놀랐고, 단순 여론조사 뿐만 아니라
   여당 대통령 탄핵, 정치 불확실성, 경제 침체등을 고려하여 분석하는 부분이
   재미있었습니다.
