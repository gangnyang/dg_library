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
        query = """
        SELECT id, name, description, event_date, participants, image
        FROM programs
        ORDER BY event_date ASC
        LIMIT :limit
        """
        results = db.execute(text(query), {"limit": limit}).mappings().fetchall()

        result = db.execute(text("SELECT COUNT(*) AS c FROM programs")).mappings().fetchone()


        # 결과를 JSON 형식으로 변환
        programs = [
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "event_date": row["event_date"],
                "participants": row["participants"],
                "image": row["image"]
            }
            for row in results
        ]

        programs[0]["count"] = result["c"]

        return programs

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"프로그램 정보를 가져오는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.post("/api/library-programs")
def create_program(program: ProgramRequest, db: Session = Depends(get_db)):
    try:
        # 도서관 프로그램 삽입 쿼리
        query = """
        INSERT INTO programs (name, description, event_date)
        VALUES (:name, :description, :event_date)
        """
        result = db.execute(text(query), {
            "name": program.name,
            "description": program.description,
            "event_date": program.event_date
        })

        # 생성된 프로그램 ID 가져오기
        program_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        db.commit()

        return {"message": "프로그램 생성 완료", "id": program_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"프로그램 생성 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.delete("/api/programs/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    try:
        query_check_program = """
        SELECT id FROM programs WHERE id = :program_id
        """
        librarian = db.execute(text(query_check_program), {"program_id": program_id}).fetchone()

        if not librarian:
            raise HTTPException(
                status_code=404,
                detail="해당 프로그램을 찾을 수 없습니다."
            )

        query_delete_program = """
        DELETE FROM programs WHERE id = :program_id
        """
        db.execute(text(query_delete_program), {"program_id": program_id})
        db.commit()

        return {"id": program_id, "message": "프로그램이 성공적으로 삭제되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"프로그램을 삭제하는 중 오류가 발생했습니다. {str(e)}"
        )

@router.get("/api/programs/{program_id}/participants")
def get_program_participants(program_id: int, db: Session = Depends(get_db)):
    try:
        # 프로그램 참가자 조회 쿼리
        query = """
        SELECT id, program_id, user_id, joined
        FROM program_participants
        WHERE program_id = :program_id
        ORDER BY joined ASC
        """
        results = db.execute(text(query), {"program_id": program_id}).mappings().fetchall()

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
            detail=f"프로그램 참가자 정보를 가져오는 중 오류가 발생했습니다. {str(e)}"
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

        user_id = user_id[0]

        # 프로그램 존재 여부 확인
        query_check_program = """
        SELECT id FROM programs WHERE id = :program_id
        """
        program = db.execute(text(query_check_program), {"program_id": program_id}).mappings().fetchone()

        if not program:
            return { "message": "프로그램을 찾을 수 없습니다." }

        # 참가자 중복 등록 확인
        query_check_participant = """
        SELECT id FROM program_participants
        WHERE program_id = :program_id AND user_id = :user_id
        """
        existing_participant = db.execute(text(query_check_participant), {
            "program_id": program_id,
            "user_id": user_id
        }).mappings().fetchone()

        if existing_participant:
            return { "message": "이미 등록된 회원입니다." }

        # 참가자 등록
        query_insert_participant = """
        INSERT INTO program_participants (program_id, user_id, joined)
        VALUES (:program_id, :user_id, :joined)
        """
        db.execute(text(query_insert_participant), {
            "program_id": program_id,
            "user_id": user_id,
            "joined": datetime.now(timezone('Asia/Seoul'))
        })

        # db.execute(text("UPDATE programs set participants = participants+1 WHERE id = :program_id"), {"program_id": program_id})

        db.commit()

        return {"message": "프로그램 참가 등록이 완료되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"프로그램 참가 등록 중 오류가 발생했습니다. {str(e)}"
        )

@router.get("/api/programs/{program_id}/librarians")
def get_program_librarians(program_id: int, db: Session = Depends(get_db)):
    try:
        # 프로그램 담당자 조회 쿼리
        query = """
        SELECT id, program_id, librarian_id
        FROM program_librarians 
        WHERE program_id = :program_id
        """
        results = db.execute(text(query), {"program_id": program_id}).mappings().fetchall()

        # 결과를 JSON 형식으로 변환
        participants = [
            {
                "id": row["id"],
                "program_id": row["program_id"],
                "librarian_id": row["librarian_id"]
            }
            for row in results
        ]

        return participants

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"프로그램 담당자 정보를 가져오는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.post("/api/programs/{program_id}/librarians")
def register_librarian(
    program_id: int,
    librarian_id: int,
    db: Session = Depends(get_db)
):
    try:
        query_check_librarian = """
        SELECT id FROM librarians WHERE id = :librarian_id
        """
        librarian = db.execute(text(query_check_librarian), {"librarian_id": librarian_id}).mappings().fetchone()
        if not librarian:
            return { "message": "해당 담당자를 찾을 수 없습니다." }
        # 프로그램 존재 여부 확인
        query_check_program = """
        SELECT id FROM programs WHERE id = :program_id
        """
        program = db.execute(text(query_check_program), {"program_id": program_id}).mappings().fetchone()

        if not program:
            return { "message": "해당 프로그램을 찾을 수 없습니다." }

        # 담당자 중복 등록 확인
        query_check_participant = """
        SELECT id FROM program_librarians
        WHERE program_id = :program_id AND librarian_id = :librarian_id
        """
        existing_librarian = db.execute(text(query_check_participant), {
            "program_id": program_id,
            "librarian_id": librarian_id
        }).mappings().fetchone()

        if existing_librarian:
            raise HTTPException(
                status_code=400,
                detail="해당 담당자 이미 프로그램에 등록되어 있습니다."
            )

        # 담당자 등록
        query_insert_librarian = """
        INSERT INTO program_librarians (program_id, librarian_id)
        VALUES (:program_id, :librarian_id)
        """
        db.execute(text(query_insert_librarian), {
            "program_id": program_id,
            "librarian_id": librarian_id
        })

        db.commit()

        return {"message": "담당자 등록이 완료되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"담당자 등록 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.get("/api/programs/user-program")
def get_programs(
    limit: int = 20, 
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user),
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

        # 도서관 프로그램 조회 쿼리
        query = """
        SELECT id, name, description, event_date, participants, image
        FROM programs WHERE id IN (
        SELECT program_id from program_participants
        WHERE user_id = :user_id)
        ORDER BY event_date ASC
        LIMIT :limit
        """
        results = db.execute(text(query), {"user_id": user_id, "limit": limit}).mappings().fetchall()


        # 결과를 JSON 형식으로 변환
        programs = [
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "event_date": row["event_date"],
                "participants": row["participants"],
                "image": row["image"]
            }
            for row in results
        ]

        return programs

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"프로그램 정보를 가져오는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.delete("/api/programs/{program_id}/participants")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user),
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

        query_delete_participant = """
        DELETE FROM program_participants WHERE program_id = :program_id AND user_id = :user_id
        """
        db.execute(text(query_delete_participant), {"program_id": program_id, "user_id": user_id})
        db.commit()

        return {"id": program_id, "message": "프로그램 취소가 완료되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"프로그램을 취소하는 중 오류가 발생했습니다. {str(e)}"
        )