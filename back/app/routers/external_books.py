from fastapi import FastAPI, HTTPException, APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from back.app.services import token
from datetime import datetime, timedelta
from pytz import timezone

router = APIRouter()

# MySQL 데이터베이스 연결 정보
DATABASE_URL = "mysql+pymysql://root:sang8429@svc.sel4.cloudtype.app:31721/dg_library"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BookRequest(BaseModel):
    author: str
    title: str
    publicate_year: str
    regist_day: str
    status: str | None = "available"
    isbn: str
    image: str | None = None

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/external_books")
def get_external_books(
    title: str = Query(None),
    author: str = Query(None),
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    try:
        query = """
        SELECT id, author, title, publicate_year, regist_day, status, isbn, image, description
        FROM external_books 
        WHERE 1=1
        """
        query_params = {}
        if title:
            query += " AND title LIKE :title"
            query_params["title"] = f"%{title}%"
        if author:
            query += " AND author LIKE :author"
            query_params["author"] = f"%{author}%"
        count_query = f"SELECT COUNT(*) FROM ({query}) as total"
        query += " LIMIT :limit OFFSET :offset"
        query_params["limit"] = limit
        query_params["offset"] = offset
        total_count = db.execute(text(count_query), query_params).scalar()
        result = db.execute(text(query), query_params).mappings().fetchall()
        books = [
            {
                "id": row["id"],
                "author": row["author"],
                "title": row["title"],
                "publicate_year": row["publicate_year"],
                "regist_day": row["regist_day"],
                "status": row["status"],
                "isbn": row["isbn"],
                "image": row["image"],
                "description": row["description"]
            }
            for row in result
        ]
        return {
            "total_count": total_count,
            "books": books
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"책 리스트를 가져오는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.get("/api/external_books/{book_id}")
def get_external_book_details(book_id: int, db: Session = Depends(get_db)):
    try:
        query = """
        SELECT id, author, title, publicate_year, regist_day, status, isbn, image, description
        FROM external_books
        WHERE id = :book_id
        """
        result = db.execute(text(query), {"book_id": book_id}).mappings().fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="책 정보가 없습니다.")
        return{
            "id": result["id"],
            "author": result["author"],
            "title": result["title"],
            "publicate_year": result["publicate_year"],
            "regist_day": result["regist_day"],
            "status": result["status"],
            "isbn": result["isbn"],
            "image": result["image"],
            "description": result["description"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"책 정보를 가져오는 중 오류가 발생했습니다.{str(e)}"
        )

@router.put("/api/external_books/interloan/{external_book_id}")
def interloan_book(
    external_book_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        current_time = datetime.now(timezone('Asia/Seoul'))
        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        if not user_id:
            raise HTTPException(
            status_code=404,
            detail="유저 정보가 잘못되었습니다."
        )

        user_id = user_id[0]

        query_check_status = """
        SELECT status FROM external_books WHERE id = :book_id
        """
        book_status = db.execute(text(query_check_status), {"book_id": external_book_id}).mappings().fetchone()

        if not book_status:
            raise HTTPException(
                status_code=404,
                detail="책을 찾을 수 없습니다."
            )

        if book_status["status"] == "borrowed":
            return {"message": "이미 상호대차 중인 책입니다.", "status": "already_borrowed"}
        
        # 상호대차 기록 삽입
        query_insert_loan = """
        INSERT INTO interloan (user_id, external_book_id, request_date, status)
        VALUES (:user_id, :book_id, :request_date, :status)
        """
        db.execute(text(query_insert_loan), {
            "user_id": user_id,
            "book_id": external_book_id,
            "request_date": current_time,
            "status": "progress"
        })

        query = """
        UPDATE external_books
        SET status = "borrowed"
        WHERE id = :book_id
        """
        db.execute(text(query), {"book_id": external_book_id})

        return_date = current_time + timedelta(days=28)

        # 도서 테이블에 도서 삽입
        query_insert_book = """
        INSERT INTO books (author, title, publicate_year, regist_day, status, isbn, 
        interloaned_from_external, return_due_external, external_book_id, image)
        SELECT e.author, e.title, e.publicate_year, e.regist_day, e.status, e.isbn, 
        1, :return_date, e.id, e.image FROM external_books e WHERE e.id = :external_book_id
        """
        db.execute(text(query_insert_book), {
            "return_date": return_date,
            "external_book_id": external_book_id
        })

        db.commit()
        return {"message": "상호대차 신청을 완료했습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"상호대차 신청에 실패했습니다. {str(e)}"
        )
    
@router.put("/api/external_books/return/{interloan_id}")
def return_loan(
    interloan_id: int,  # 상호대차 ID
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        current_time = datetime.now(timezone('Asia/Seoul'))
        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        if not user_id:
            raise HTTPException(
            status_code=404,
            detail="유저 정보가 잘못되었습니다."
        )

        user_id = user_id[0]

        # 상호대차 기록 존재 여부 확인
        query_check_loan = """
        SELECT id, status FROM interloan WHERE id = :loan_id
        """
        interloan_record = db.execute(text(query_check_loan), {"loan_id": interloan_id}).mappings().fetchone()

        if not interloan_record:
            raise HTTPException(
                status_code=404,
                detail="해당 상호대차 기록을 찾을 수 없습니다."
            )

        if interloan_record["status"] == "complete":
            return {"message": "이미 완료된 상호대차입니다."}

        # 상호대차 기록 업데이트
        query_update_loan = """
        UPDATE interloan
        SET status = :status
        WHERE id = :interloan_id
        """
        db.execute(text(query_update_loan), {
            "status": "complete",
            "interloan_id": interloan_id
        })

        # 상호대차된 책 상태 업데이트 (책을 다시 대출 가능 상태로 변경)
        query_update_book = """
        UPDATE external_books
        SET status = 'available'
        WHERE id = (SELECT external_book_id FROM interloan WHERE id = :interloan_id)
        """
        db.execute(text(query_update_book), {"interloan_id": interloan_id})

        # 상호대차된 책 도서 테이블에서 삭제
        query_delete_book = """
        DELETE from books
        WHERE external_book_id = (SELECT external_book_id FROM interloan WHERE id = :interloan_id)
        """
        db.execute(text(query_delete_book), {"interloan_id": interloan_id})

        db.commit()

        return {"message": "반납이 완료되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"반납 처리 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.get("/api/loan/user-interloan")
def get_loan_history(
    limit: int = 20,  # 최대 반환 개수
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user),  # 인증된 유저
):
    try:
        # 현재 유저의 user_id 가져오기
        query_user = """
        SELECT id FROM users WHERE username = :username
        """
        result = db.execute(text(query_user), {"username": current_user}).mappings().fetchone()

        if not result:
            return { "message": "유저 정보를 찾을 수 없습니다. "}

        user_id = result["id"]

        # 대출 내역 조회 쿼리
        query = """
        SELECT id, user_id, external_book_id, request_date, status
        FROM interloan
        WHERE user_id = :user_id
        ORDER BY request_date DESC
        LIMIT :limit
        """
        interloan_results = db.execute(text(query), {"user_id": user_id, "limit": limit}).mappings().fetchall()

        # 결과를 JSON 형식으로 반환
        interloan_history = [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "external_book_id": row["external_book_id"],
                "request_date": row["request_date"],
                "status": row["status"],
            }
            for row in interloan_results
        ]
        return interloan_history

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"대출 내역을 가져오는 중 오류가 발생했습니다. {str(e)}"
        )