from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from back.app.services import token
from back.app.services import hash

router = APIRouter()

# MySQL 데이터베이스 연결 정보
DATABASE_URL = "mysql+pymysql://root:sang8429@localhost:3306/dg_library"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRequest(BaseModel):
    username: str
    password: str
    phone: str | None = None
    name: str

class UserUpdateRequest(BaseModel):
    password: str
    phone: str | None = None
    name: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    message: str

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# 회원가입 API 엔드포인트
@router.post("/api/users", response_model=UserResponse)
def register_user(user: UserRequest, db: Session = Depends(get_db)):
    try:
        # 데이터 삽입 쿼리 실행
        query = """
        INSERT INTO users (username, password, phone, name)
        VALUES (:username, :password, :phone, :name)
        """
        hashed = hash.hash_password(user.password)
        db.execute(text(query), {
            "username": user.username,
            "password": hashed,
            "phone": user.phone,
            "name": user.name
        })
        db.commit()

        # 삽입된 사용자 ID 가져오기
        result = db.execute(text("SELECT LAST_INSERT_ID() as id"))
        user_id = result.mappings().fetchone()["id"]

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="회원가입에 실패했습니다."
        )

    return {"user_id": user_id, "message": "회원가입에 성공했습니다."}

@router.post("/api/users/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    # 사용자 검색
    db_user = db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": user.username}
    ).mappings().fetchone()

    # 1. 아이디가 존재하지 않는 경우
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 아이디입니다."
        )

    # 2. 비밀번호가 일치하지 않는 경우
    if not hash.verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=400,
            detail="비밀번호가 일치하지 않습니다."
        )

    # 3. 로그인 성공 - JWT 토큰 발행
    access_token = token.create_access_token(data={"sub": db_user["username"]})
    return {
        "message": "로그인에 성공했습니다.",
        "token": access_token
    }

@router.put("/api/users/update")
def update(
    updated_user: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    if not updated_user.password:
        raise HTTPException(
            status_code=400,
            detail="비밀번호가 누락되었습니다."
        )

    try:
        query = """
        UPDATE users
        SET password = :password, phone = :phone, name = :name WHERE username = :username
        """
        db.execute(text(query), {
            "password": hash.hash_password(updated_user.password),
            "phone": updated_user.phone,
            "name": updated_user.name,
            "username": current_user
        })
        db.commit()
        return {"message": "회원정보를 수정했습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = 400,
            detail = "회원정보를 수정하지 못했습니다."
        )

@router.delete("/api/users/delete")
def withdraw(
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user)
):
    try:
        id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        if not id:
            raise HTTPException(
                status_code=404,
                detail="탈퇴하려는 계정이 존재하지 않습니다."
            )

        query = """
        DELETE from users
        WHERE username = :username
        """

        db.execute(text(query), {
            "username": current_user
        })
        db.commit()
        return{"message": "회원탈퇴가 완료되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="오류가 발생했습니다."
        )

@router.get("/api/users/{user_id}")
def get_book_details(user_id: int, db: Session = Depends(get_db)):
    try:
        query = """
        SELECT username
        FROM users
        WHERE id = :user_id
        """
        result = db.execute(text(query), {"user_id": user_id}).mappings().fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="책 정보가 없습니다.")
        return{
            "username" : result["username"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"책 정보를 가져오는 중 오류가 발생했습니다.{str(e)}"
        )