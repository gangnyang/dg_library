from fastapi import FastAPI, HTTPException, APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from back.app.services import token

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
    interloaned_from_external: int | None = 0
    return_due_external: str | None = None
    external_book_id: int | None = None
    image: str | None = None

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/books")
def get_books(
    title: str = Query(None),
    author: str = Query(None),
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        query = text("""
        SELECT id, author, title, publicate_year, regist_day, status, borrowed, isbn, image 
        FROM books 
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
                "borrowed": row["borrowed"],
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
    
@router.get("/api/books/{book_id}")
def get_book_details(book_id: int, db: Session = Depends(get_db)):
    try:
        query = text("""
        SELECT id, author, title, publicate_year, regist_day, status, borrowed, isbn, image
        FROM books
        WHERE id = :book_id
        """)
        result = db.execute(query, {"book_id": book_id}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="책 정보가 없습니다.")
        return{
            "id": result["id"],
            "author": result["author"],
            "title": result["title"],
            "publicate_year": result["publicate_year"],
            "regist_day": result["regist_day"],
            "status": result["status"],
            "borrowed": result["borrowed"],
            "isbn": result["isbn"],
            "image": result["image"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="책 정보를 가져오는 중 오류가 발생했습니다."
        )
    
@router.put("/api/books/{book_id}")
def loan_book(
    book_id: int,
    loan_date: str,
    will_return_date: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
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
        SELECT status FROM books WHERE id = :book_id
        """)
        book_status = db.execute(query_check_status, {"book_id": book_id}).fetchone()

        if not book_status:
            raise HTTPException(
                status_code=404,
                detail="책을 찾을 수 없습니다."
            )

        if book_status["status"] == "borrowed":
            return {"message": "이미 대출 중인 책입니다.", "status": "already_borrowed"}
        
        # 대출 기록 삽입
        query_insert_loan = text("""
        INSERT INTO loan (user_id, book_id, loan_date, will_return_date, status)
        VALUES (:user_id, :book_id, :loan_date, :will_return_date, :status)
        """)
        db.execute(query_insert_loan, {
            "user_id": user_id,
            "book_id": book_id,
            "loan_date": loan_date,
            "will_return_date": will_return_date,
            "status": "progress"
        })

        query = text("""
        UPDATE books
        SET borrowed = borrowed + 1, status = "borrowed"
        WHERE id = :book_id
        """)
        db.execute(query, {"book_id": book_id})
        db.commit()
        return {"message": "책 대출 신청을 완료했습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="대출 신청에 실패했습니다."
        )
    
@router.post("/api/books/add")
def add_book(book: BookRequest, db: Session = Depends(get_db)):
    try:
        query = text("""
        INSERT INTO books (author, title, publicate_year, regist_day, status, isbn,
        interloaned_from_external, return_due_external, external_book_id, image)
        VALUES(:author, :title, :publicate_year, :regist_day, :status, :isbn, 
        :interloaned_from_external, :return_due_external, :external_book_id, :image)
        """)
        db.execute(query, {
            "author": book.author,
            "title": book.title,
            "publicate_year": book.publicate_year,
            "regist_day": book.regist_day,
            "status": book.status,
            "isbn": book.status,
            "interloaned_from_external": book.interloaned_from_external,
            "return_due_external": book.return_due_external,
            "external_book_id": book.external_book_id,
            "image": book.image
        })
        db.commit()

        return {"message": "책 등록이 완료되었습니다."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="책 등록에 실패했습니다."
        )
    
@router.delete("/api/books/{book_id}")
def delete(
    book_id: int,
    db: Session = Depends(get_db)
):
    try:
        id = db.execute(
            text("SELECT id FROM books WHERE id = :book_id"),
            {"book_id": book_id}
        ).fetchone()

        if not id:
            raise HTTPException(
                status_code=404,
                detail="삭제하려는 책이 없습니다."
            )

        query = text("""
        DELETE from books
        WHERE id = :book_id
        """)

        db.execute(query, {
            "book_id": book_id
        })
        db.commit()
        return{"message": "책 삭제가 완료되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="오류가 발생했습니다."
        )