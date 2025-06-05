import pandas as pd
import mysql.connector

# 1. 엑셀 파일 읽기
excel_path = 'PP1.xlsx'
df = pd.read_excel(excel_path, header=None, engine='openpyxl')
df.columns = ['elec_num', 'cand_num', 'cand_name', 'rate', 'date']

# 2. 타입 보정 및 결측값 제거
df['elec_num'] = df['elec_num'].astype(int)
df['cand_num'] = df['cand_num'].astype(int)
df['cand_name'] = df['cand_name'].astype(str)
df['rate'] = df['rate'].astype(float)
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
df.dropna(inplace=True)

# 3. MySQL 연결 정보 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'cks3148',
    'database': 'pp',
    'charset': 'utf8mb4'
}

conn = None
cursor = None

# 4. 데이터 삽입
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO pp1 (elec_num, cand_num, cand_name, rate, date)
        VALUES (%s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    print("데이터가 성공적으로 삽입되었습니다.")

except mysql.connector.Error as err:
    print(f"데이터베이스 오류: {err}")

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
