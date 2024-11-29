from fastapi import FastAPI, HTTPException, APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from back.app.services import token
from datetime import datetime
from pytz import timezone

router = APIRouter()

# MySQL 데이터베이스 연결 정보
DATABASE_URL = "mysql+pymysql://root:sang8429@localhost:3306/dg_library"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LoanRequest(BaseModel):
    user_id: int
    book_id: int
    loan_date: str
    will_return_date: str
    returned_date: str | None = None
    status: str = "progress"

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/loan/user-loan")
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
            return {"message": "유저 정보를 찾을 수 없습니다."}

        user_id = result["id"]

        # 대출 내역 조회 쿼리
        query = """
        SELECT id, user_id, book_id, loan_date, will_return_date, returned_date, overdue, status
        FROM loan
        WHERE user_id = :user_id
        ORDER BY loan_date DESC
        LIMIT :limit
        """
        loan_results = db.execute(text(query), {"user_id": user_id, "limit": limit}).mappings().fetchall()

        # 결과를 JSON 형식으로 반환
        loan_history = [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "book_id": row["book_id"],
                "loan_date": row["loan_date"],
                "will_return_date": row["will_return_date"],
                "returned_date": row["returned_date"],
                "overdue": row["overdue"],
                "status": row["status"],
            }
            for row in loan_results
        ]
        return loan_history

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"대출 내역을 가져오는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.get("/api/loan")
def get_book_loan_history(
    book_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    try:
        # 책의 대출 내역 조회 쿼리
        query = """
        SELECT id, user_id, book_id, loan_date, will_return_date, returned_date, overdue, status
        FROM loan
        WHERE book_id = :book_id
        ORDER BY loan_date DESC
        LIMIT :limit
        """
        loan_results = db.execute(text(query), {"book_id": book_id, "limit": limit}).mappings().fetchall()

        # 결과를 JSON 형식으로 변환
        loan_history = [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "book_id": row["book_id"],
                "loan_date": row["loan_date"],
                "will_return_date": row["will_return_date"],
                "returned_date": row["returned_date"],
                "overdue": row["overdue"],
                "status": row["status"],
            }
            for row in loan_results
        ]
        return loan_history

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"책 대출 내역을 가져오는 중 오류가 발생했습니다. {str(e)}"
        )

@router.put("/api/loan/return/{loan_id}")
def return_loan(
    loan_id: int,  # 대출 ID (URL 경로 매개변수)
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)  # JWT 인증된 유저 확인
):
    try:
        # 현재 유저의 user_id 가져오기
        query_user = """
        SELECT id FROM users WHERE username = :username
        """
        result = db.execute(text(query_user), {"username": current_user}).mappings().fetchone()

        if not result:
            return {"message": "유저 정보를 찾을 수 없습니다."}
        
        user_id = result["id"]

        # 대출 기록 존재 여부 확인
        query_check_loan = """
        SELECT id, status FROM loan WHERE id = :loan_id
        """
        loan_record = db.execute(text(query_check_loan), {"loan_id": loan_id}).mappings().fetchone()

        if not loan_record:
            raise HTTPException(
                status_code=404,
                detail="해당 대출 기록을 찾을 수 없습니다."
            )

        if loan_record["status"] == "returned":
            return {"message": "이미 반납된 대출입니다."}
        
        returned_date= datetime.now(timezone('Asia/Seoul'))
        status= "returned"
        overdue= 0

        # 대출 기록 업데이트
        query_update_loan = """
        UPDATE loan
        SET returned_date = :returned_date, status = :status, overdue = :overdue
        WHERE id = :loan_id
        """
        db.execute(text(query_update_loan), {
            "returned_date": returned_date,
            "status": status,
            "overdue": overdue,
            "loan_id": loan_id
        })

        # 대출된 책 상태 업데이트 (책을 다시 대출 가능 상태로 변경)
        query_update_book = """
        UPDATE books
        SET status = 'available'
        WHERE id = (SELECT book_id FROM loan WHERE id = :loan_id)
        """
        db.execute(text(query_update_book), {"loan_id": loan_id})

        db.commit()

        return {"message": "반납이 완료되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"반납 처리 중 오류가 발생했습니다. {str(e)}"
        )
    

@router.put("/api/loan/update-overdue")
def update_overdue_status(db: Session = Depends(get_db)):
    try:
        # 현재 날짜 가져오기
        current_date = datetime.now(timezone('Asia/Seoul')).date().isoformat()

        # 연체 상태 업데이트 쿼리
        query_update_overdue = """
        UPDATE loan
        SET overdue = 1, status = 'overdue'
        WHERE (will_return_date < :current_date AND returned_date IS NULL AND overdue = 0)
        OR (will_return_date < returned_date AND overdue = 0)
        """
        result = db.execute(text(query_update_overdue), {"current_date": current_date})

        # 변경된 행 수 확인
        updated_rows = result.rowcount

        db.commit()
        return {"message": f"{updated_rows}개의 대출이 연체 상태로 업데이트되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"연체 상태 업데이트 중 오류가 발생했습니다. {str(e)}"
        )
