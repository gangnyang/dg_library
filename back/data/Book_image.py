import requests
import mysql.connector

# 알라딘 API 키 설정
ALADIN_API_KEY = "ttbgravesknife1930001"

# 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sang8429",
    database="dg_library"
)

cursor = db.cursor()

# ISBN 가져오기
cursor.execute("SELECT isbn FROM books WHERE image IS NULL AND id > 90769 ORDER BY id ASC LIMIT 1000")
isbn_list = [row[0] for row in cursor.fetchall()]

# 알라딘 API URL 템플릿
api_url_template = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={}&itemIdType=ISBN13&ItemId={}&output=js&Version=20131101"

# 이미지 링크 업데이트
update_query = "UPDATE books SET image = %s WHERE isbn = %s"

for isbn in isbn_list:
    if isbn:  # ISBN이 존재하는 경우
        try:
            # 알라딘 API 호출
            api_url = api_url_template.format(ALADIN_API_KEY, isbn)
            response = requests.get(api_url)
            data = response.json()
            
            # 이미지 URL 추출
            if "item" in data and len(data["item"]) > 0:
                image_url = data["item"][0]["cover"]
                # 데이터베이스에 이미지 링크 업데이트
                cursor.execute(update_query, (image_url, isbn))
                print(f"이미지 링크 업데이트 완료: {isbn}")
            else:
                print(f"이미지 없음: {isbn}")
        except Exception as e:
            print(f"오류 발생: {isbn}, {e}")

# 변경 사항 커밋
db.commit()

# 데이터베이스 연결 닫기
cursor.close()
db.close()
