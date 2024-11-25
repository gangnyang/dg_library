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

class LibrarianRequest(BaseModel):
    librarian_name: str
    work_details: str
    hire_date: str 

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/librarians")
def get_librarians(db: Session = Depends(get_db)):
    try:
        # 사서 정보 조회 쿼리
        query = """
        SELECT id, librarian_name AS librarian_name, work_details, hire_date
        FROM librarians
        """
        results = db.execute(text(query)).mappings().fetchall()

        # 결과를 JSON 형식으로 변환
        librarians = [
            {
                "id": row["id"],
                "librarian_name": row["librarian_name"],
                "work_details": row["work_details"],
                "hire_date": row["hire_date"],
            }
            for row in results
        ]

        return librarians

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"사서 정보를 가져오는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.post("/api/librarians")
def create_librarian(librarian: LibrarianRequest, db: Session = Depends(get_db)):
    try:
        # 사서 정보 삽입 쿼리
        query = """
        INSERT INTO librarians (librarian_name, work_details, hire_date)
        VALUES (:name, :work_details, :hire_date)
        """
        result = db.execute(text(query), {
            "name": librarian.librarian_name,
            "work_details": librarian.work_details,
            "hire_date": librarian.hire_date
        })

        # 반환된 ID 가져오기
        librarian_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        db.commit()

        return [{"id": librarian_id, "message": "사서 등록이 완료되었습니다."}]

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"사서를 등록하는 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.delete("/api/librarians/{librarian_id}")
def delete_librarian(
    librarian_id: int,
    db: Session = Depends(get_db)
):
    try:
        query_check_librarian = """
        SELECT id FROM librarians WHERE id = :librarian_id
        """
        librarian = db.execute(text(query_check_librarian), {"librarian_id": librarian_id}).mappings().fetchone()

        if not librarian:
            raise HTTPException(
                status_code=404,
                detail="해당 사서를 찾을 수 없습니다."
            )

        # 사서 삭제 쿼리
        query_delete_librarian = """
        DELETE FROM librarians WHERE id = :librarian_id
        """
        db.execute(text(query_delete_librarian), {"librarian_id": librarian_id})
        db.commit()

        return {"id": librarian_id, "message": "사서가 성공적으로 삭제되었습니다."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"사서를 삭제하는 중 오류가 발생했습니다. {str(e)}"
        )