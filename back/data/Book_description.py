import requests
import mysql.connector
from mysql.connector import Error

# 알라딘 API 설정
API_KEY = "ttbgravesknife1930001"
API_URL = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"

# MySQL 연결 설정
db_config = {
    'host': 'localhost',
    'database': 'dg_library',
    'user': 'root',
    'password': 'sang8429',
    'port': 3306
}

# 알라딘 API로 데이터 가져오기
def fetch_book_description(isbn):
    params = {
        "ttbkey": API_KEY,
        "itemIdType": "ISBN13",
        "ItemId": isbn,
        "output": "js",
        "Version": "20131101"
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "item" in data and len(data["item"]) > 0:
            return data["item"][0].get("description", "No description available")
        else:
            return "No description available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for ISBN {isbn}: {e}")
        return None

# 데이터베이스에서 ISBN 가져오고 업데이트하기
def update_books_description():
    try:
        # MySQL 연결
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # ISBN 조회
        cursor.execute("SELECT id, isbn FROM books WHERE description IS NULL OR description = '' limit 3000;")
        books = cursor.fetchall()

        # 각 ISBN에 대해 알라딘 API로 데이터 가져와 업데이트
        for book in books:
            isbn = book["isbn"]
            book_id = book["id"]
            description = fetch_book_description(isbn)

            if description:
                cursor.execute("UPDATE books SET description = %s WHERE id = %s", (description, book_id))
                print(f"Updated book ID {book_id} with description.")
        
        # 변경사항 커밋
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# 실행
if __name__ == "__main__":
    update_books_description()
