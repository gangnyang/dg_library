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

class ProgramRequest(BaseModel):
    name: str
    description: str
    event_date: datetime

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/programs")
def get_programs(limit: int = 20, db: Session = Depends(get_db)):
    try:
        # 도서관 프로그램 조회 쿼리
        query = text("""
        SELECT id, name, description, event_date, participants
        FROM programs
        ORDER BY event_date ASC
        LIMIT :limit
        """)
        results = db.execute(query, {"limit": limit}).fetchall()

        # 결과를 JSON 형식으로 변환
        programs = [
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "event_date": row["event_date"],
                "participants": row["participants"]
            }
            for row in results
        ]

        return programs

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="프로그램 정보를 가져오는 중 오류가 발생했습니다."
        )
    
@router.post("/api/library-programs")
def create_program(program: ProgramRequest, db: Session = Depends(get_db)):
    try:
        # 도서관 프로그램 삽입 쿼리
        query = text("""
        INSERT INTO programs (name, description, event_date)
        VALUES (:name, :description, :event_date)
        RETURNING id
        """)
        result = db.execute(query, {
            "name": program.name,
            "description": program.description,
            "event_date": program.event_date
        })

        # 생성된 프로그램 ID 가져오기
        program_id = result.fetchone()["id"]

        db.commit()

        return {"message": "프로그램 생성 완료", "id": program_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="프로그램 생성 중 오류가 발생했습니다."
        )
    
@router.delete("/api/programs/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    try:
        query_check_program = text("""
        SELECT id FROM programs WHERE id = :program_id
        """)
        librarian = db.execute(query_check_program, {"program_id": program_id}).fetchone()

        if not librarian:
            raise HTTPException(
                status_code=404,
                detail="해당 프로그램을 찾을 수 없습니다."
            )

        query_delete_program = text("""
        DELETE FROM programs WHERE id = :program_id
        """)
        db.execute(query_delete_program, {"program_id": program_id})
        db.commit()

        return {"id": program_id, "message": "프로그램이 성공적으로 삭제되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="프로그램을 삭제하는 중 오류가 발생했습니다."
        )

@router.get("/api/programs/{program_id}/participants")
def get_program_participants(program_id: int, db: Session = Depends(get_db)):
    try:
        # 프로그램 참가자 조회 쿼리
        query = text("""
        SELECT id, program_id, user_id, joined
        FROM program_participants
        WHERE program_id = :program_id
        ORDER BY joined ASC
        """)
        results = db.execute(query, {"program_id": program_id}).fetchall()

        # 결과를 JSON 형식으로 변환
        participants = [
            {
                "id": row["id"],
                "program_id": row["program_id"],
                "user_id": row["user_id"],
                "joined": row["joined"]
            }
            for row in results
        ]

        return participants

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="프로그램 참가자 정보를 가져오는 중 오류가 발생했습니다."
        )

@router.post("/api/programs/{program_id}/participants")
def register_participant(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)  # JWT 인증된 유저
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

        # 프로그램 존재 여부 확인
        query_check_program = text("""
        SELECT id FROM programs WHERE id = :program_id
        """)
        program = db.execute(query_check_program, {"program_id": program_id}).fetchone()

        if not program:
            raise HTTPException(
                status_code=404,
                detail="해당 프로그램을 찾을 수 없습니다."
            )

        # 참가자 중복 등록 확인
        query_check_participant = text("""
        SELECT id FROM program_participants
        WHERE program_id = :program_id AND user_id = :user_id
        """)
        existing_participant = db.execute(query_check_participant, {
            "program_id": program_id,
            "user_id": user_id
        }).fetchone()

        if existing_participant:
            raise HTTPException(
                status_code=400,
                detail="해당 사용자는 이미 프로그램에 등록되어 있습니다."
            )

        # 참가자 등록
        query_insert_participant = text("""
        INSERT INTO program_participants (program_id, user_id, joined)
        VALUES (:program_id, :user_id, :joined)
        """)
        db.execute(query_insert_participant, {
            "program_id": program_id,
            "user_id": user_id,
            "joined": datetime.utcnow()
        })

        db.commit()

        return {"message": "참가자 등록이 완료되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참가자 등록 중 오류가 발생했습니다."
        )

@router.get("/api/programs/{program_id}/librarians")
def get_program_librarians(program_id: int, db: Session = Depends(get_db)):
    try:
        # 프로그램 담당자 조회 쿼리
        query = text("""
        SELECT id, program_id, librarian_id
        FROM program_librarians 
        WHERE program_id = :program_id
        """)
        results = db.execute(query, {"program_id": program_id}).fetchall()

        # 결과를 JSON 형식으로 변환
        participants = [
            {
                "id": row["id"],
                "program_id": row["program_id"],
                "user_id": row["user_id"]
            }
            for row in results
        ]

        return participants

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="프로그램 담당자 정보를 가져오는 중 오류가 발생했습니다."
        )
    
@router.post("/api/programs/{program_id}/librarians")
def register_librarian(
    program_id: int,
    librarian_id: int,
    db: Session = Depends(get_db)
):
    try:
        query_check_librarian = text("""
        SELECT id FROM librarians WHERE id = :librarian_id
        """)
        librarian = db.execute(query_check_librarian, {"librarian_id": librarian_id}).fetchone()
        if not librarian:
            raise HTTPException(
                status_code=404,
                detail="해당 담당자를 찾을 수 없습니다."
            )
        # 프로그램 존재 여부 확인
        query_check_program = text("""
        SELECT id FROM programs WHERE id = :program_id
        """)
        program = db.execute(query_check_program, {"program_id": program_id}).fetchone()

        if not program:
            raise HTTPException(
                status_code=404,
                detail="해당 프로그램을 찾을 수 없습니다."
            )

        # 담당자 중복 등록 확인
        query_check_participant = text("""
        SELECT id FROM program_librarians
        WHERE program_id = :program_id AND librarian_id = :librarian_id
        """)
        existing_librarian = db.execute(query_check_participant, {
            "program_id": program_id,
            "librarian_id": librarian_id
        }).fetchone()

        if existing_librarian:
            raise HTTPException(
                status_code=400,
                detail="해당 담당자 이미 프로그램에 등록되어 있습니다."
            )

        # 담당자 등록
        query_insert_librarian = text("""
        INSERT INTO program_librarians (program_id, librarian_id)
        VALUES (:program_id, :librarian_id)
        """)
        db.execute(query_insert_librarian, {
            "program_id": program_id,
            "librarian_id": librarian_id
        })

        db.commit()

        return {"message": "담당자 등록이 완료되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="담당자 등록 중 오류가 발생했습니다."
        )