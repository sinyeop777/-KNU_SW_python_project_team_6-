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
