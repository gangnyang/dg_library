from fastapi import FastAPI, HTTPException, APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from back.app.services import token
from datetime import datetime, timedelta

router = APIRouter()

# MySQL 데이터베이스 연결 정보
DATABASE_URL = "mysql+pymysql://root:sang8429@localhost:3306/dg_library"

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
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        query = text("""
        SELECT id, author, title, publicate_year, regist_day, status, isbn, image 
        FROM external_books 
        WHERE 1=1
        """)
        query_params = {}
        if title:
            query += text(" AND title LIKE :title")
            query_params["title"] = f"%{title}%"
        if author:
            query += text(" AND author LIKE :author")
            query_params["author"] = f"%{author}%"
        count_query = text(f"SELECT COUNT(*) FROM ({query}) as total")
        query += text(" LIMIT :limit OFFSET :offset")
        query_params["limit"] = limit
        query_params["offset"] = offset
        total_count = db.execute(count_query, query_params).scalar()
        result = db.execute(query, query_params).fetchall()
        books = [
            {
                "id": row["id"],
                "author": row["author"],
                "title": row["title"],
                "publicate_year": row["publicate_year"],
                "regist_day": row["regist_day"],
                "status": row["status"],
                "isbn": row["isbn"],
                "image": row["image"]
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
            detail="책 리스트를 가져오는 중 오류가 발생했습니다."
        )
    
@router.put("/api/external_books/{external_book_id}")
def interloan_book(
    external_book_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        current_time = datetime.now()
        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        if not user_id:
            raise HTTPException(
            status_code=404,
            detail="유저 정보가 잘못되었습니다."
        )

        query_check_status = text("""
        SELECT status FROM external_books WHERE id = :book_id
        """)
        book_status = db.execute(query_check_status, {"book_id": external_book_id}).fetchone()

        if not book_status:
            raise HTTPException(
                status_code=404,
                detail="책을 찾을 수 없습니다."
            )

        if book_status["status"] == "borrowed":
            return {"message": "이미 대출 중인 책입니다.", "status": "already_borrowed"}
        
        # 상호대차 기록 삽입
        query_insert_loan = text("""
        INSERT INTO interloan (user_id, external_book_id, request_date, status)
        VALUES (:user_id, :book_id, :request_date, :status)
        """)
        db.execute(query_insert_loan, {
            "user_id": user_id,
            "book_id": external_book_id,
            "request_date": current_time,
            "status": "progress"
        })

        query = text("""
        UPDATE external_books
        SET status = "borrowed"
        WHERE id = :book_id
        """)
        db.execute(query, {"book_id": external_book_id})

        return_date = current_time + timedelta(days=28)

        # 도서 테이블에 도서 삽입
        query_insert_book = text("""
        INSERT INTO books (author, title, publicate_year, regist_day, status, isbn, 
        interloaned_from_external, return_due_external, external_book_id, image)
        SELECT e.author, e.title, e.publicate_year, e.regist_day, e.status, e.isbn, 
        1, :return_date, e.id, e.image FROM external_books e
        """)
        db.execute(query_insert_book, {
            "return_date": return_date
        })

        db.commit()
        return {"message": "상호대차 신청을 완료했습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="상호대차 신청에 실패했습니다."
        )
    
@router.put("/api/external_books/{interloan_id}")
def return_loan(
    interloan_id: int,  # 상호대차 ID
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        current_time = datetime.utcnow()
        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        if not user_id:
            raise HTTPException(
            status_code=404,
            detail="유저 정보가 잘못되었습니다."
        )

        # 상호대차 기록 존재 여부 확인
        query_check_loan = text("""
        SELECT id, status FROM interloan WHERE id = :loan_id
        """)
        interloan_record = db.execute(query_check_loan, {"loan_id": interloan_id}).fetchone()

        if not interloan_record:
            raise HTTPException(
                status_code=404,
                detail="해당 상호대차 기록을 찾을 수 없습니다."
            )

        if interloan_record["status"] == "complete":
            return {"message": "이미 완료된 상호대차입니다."}

        # 상호대차 기록 업데이트
        query_update_loan = text("""
        UPDATE interloan
        SET status = :status
        WHERE id = :interloan_id
        """)
        db.execute(query_update_loan, {
            "status": "complete",
            "interloan_id": interloan_id
        })

        # 상호대차된 책 상태 업데이트 (책을 다시 대출 가능 상태로 변경)
        query_update_book = text("""
        UPDATE external_books
        SET status = 'available'
        WHERE id = (SELECT book_id FROM interloan WHERE id = :interloan_id)
        """)
        db.execute(query_update_book, {"interloan_id": interloan_id})

        # 상호대차된 책 도서 테이블에서 삭제
        query_delete_book = text("""
        DELETE from books
        WHERE id = (SELECT book_id FROM interloan WHERE id = :interloan_id)
        """)
        db.execute(query_delete_book, {"interloan_id": interloan_id})

        db.commit()

        return {"message": "반납이 완료되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="반납 처리 중 오류가 발생했습니다."
        )