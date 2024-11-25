import pandas as pd
from sqlalchemy import create_engine

# CSV 파일 읽기
df = pd.read_csv("back/data/NL_BO_BOOK_PUB_202410-1.csv")

# 조건 필터링
filtered_df = df[df['LBRRY_CD'] != 12224][['AUTHR_NM', 'TITLE_NM', 'PBLICTE_YEAR', 'REGIST_DE', 'ISBN_THIRTEEN_NO']]

filtered_df = filtered_df.head(200000)

# 컬럼명 매핑
filtered_df.columns = ['author', 'title', 'publicate_year', 'regist_day', 'isbn']

# MySQL 연결
engine = create_engine('mysql+pymysql://root:sang8429@localhost:3306/dg_library')

# 데이터 삽입
filtered_df.to_sql('external_books', con=engine, if_exists='append', index=False)
