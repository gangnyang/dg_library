from fastapi import FastAPI, HTTPException, APIRouter, Depends, Query
from pydantic import BaseModel, Field
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

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

class CommentRequest(BaseModel):
    book_id: int
    context: str
    parent_id: int | None = None

class CommentUpdateRequest(BaseModel):
    comment_id: int
    context: str

@router.get("/api/comments")
def get_comments(
    book_id: int,
    db: Session = Depends(get_db)
):
    try:
        # 최상위 댓글 가져오기 (parent_id가 NULL인 댓글)
        query = """
        SELECT id, book_id, user_id, parent_id, context, created, updated
        FROM comments
        WHERE book_id = :book_id AND parent_id IS NULL
        ORDER BY created DESC
        """
        top_comments = db.execute(text(query), {"book_id": book_id}).mappings().fetchall()

        # 최상위 댓글의 ID 목록 가져오기
        parent_ids = [comment["id"] for comment in top_comments]

        comment_count = db.execute(text("SELECT COUNT(*) AS count FROM comments WHERE book_id = :book_id"), {"book_id":book_id}).mappings().fetchone()

        # 대댓글 가져오기 (parent_id가 상위 댓글 ID 중 하나인 경우)
        if parent_ids:
            query_replies = """
            SELECT id, book_id, user_id, parent_id, context, created, updated
            FROM comments
            WHERE parent_id IN :parent_ids
            ORDER BY created ASC
            """
            replies = db.execute(text(query_replies), {"parent_ids": tuple(parent_ids)}).mappings().fetchall()
        else:
            replies = []

        # 대댓글을 부모 댓글에 매핑
        reply_map = {parent_id: [] for parent_id in parent_ids}
        for reply in replies:
            reply_map[reply["parent_id"]].append({
                "id": reply["id"],
                "user_id": reply["user_id"],
                "parent_id": reply["parent_id"],
                "context": reply["context"],
                "created": reply["created"],
                "updated": reply["updated"],
            })

        # 최상위 댓글 + 대댓글 매핑 결과 생성
        result = []
        for comment in top_comments:
            result.append({
                "id": comment["id"],
                "book_id": comment["book_id"],
                "user_id": comment["user_id"],
                "parent_id": comment["parent_id"],
                "context": comment["context"],
                "created": comment["created"],
                "updated": comment["updated"],
                "replies": reply_map.get(comment["id"], []),
            })


        return {
            "count":comment_count,
            "result":result,
            }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"댓글을 가져오는 중 오류가 발생했습니다. {str(e)}"
        )

@router.post("/api/comments/add")
def create_comment(
    request: CommentRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user),  # JWT 인증된 유저
):
    try:
        # 현재 시간 가져오기
        current_time = datetime.now(timezone('Asia/Seoul'))
        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()
        if not user_id:
            raise HTTPException(
                status_code=404,
                detail="댓글을 작성하려면 로그인해야 합니다."
            )
        user_id = user_id[0]
        # 댓글 삽입
        query_insert_comment = """
        INSERT INTO comments (book_id, user_id, parent_id, context, created, updated)
        VALUES (:book_id, :user_id, :parent_id, :context, :created, :updated)
        """
        db.execute(text(query_insert_comment), {
            "book_id": request.book_id,
            "user_id": user_id,
            "parent_id": request.parent_id,
            "context": request.context,
            "created": current_time,
            "updated": current_time,
        })

        db.commit()

        return {
            "created": current_time,
            "updated": current_time,
            "message": "댓글 작성 완료."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"댓글 작성 중 오류가 발생했습니다.{str(e)}"
        )

@router.put("/api/comments/")
def update_comment(
    request: CommentUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user), 
):
    try:
        # 댓글 존재 여부 및 작성자 확인
        query_check_comment = """
        SELECT id, user_id, created
        FROM comments
        WHERE id = :comment_id
        """
        comment = db.execute(text(query_check_comment), {"comment_id": request.comment_id}).mappings().fetchone()

        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        user_id = user_id[0]

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="댓글을 찾을 수 없습니다."
            )

        if comment["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="댓글을 수정할 권한이 없습니다."
            )

        # 댓글 내용 업데이트
        current_time = datetime.now(timezone('Asia/Seoul'))
        query_update_comment = """
        UPDATE comments
        SET context = :context, updated = :updated
        WHERE id = :comment_id
        """
        db.execute(text(query_update_comment), {
            "context": request.context,
            "updated": current_time,
            "comment_id": request.comment_id
        })

        db.commit()

        return {
            "created": comment["created"],
            "updated": current_time,
            "message": "댓글 수정 완료."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"댓글 수정 중 오류가 발생했습니다. {str(e)}"
        )
    
@router.delete("/api/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(token.get_current_user),
):
    try:
        user_id = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": current_user}
        ).fetchone()

        user_id = user_id[0]

        query_check_comment = """
        SELECT id, user_id, created
        FROM comments
        WHERE id = :comment_id
        """
        comment = db.execute(text(query_check_comment), {"comment_id": comment_id}).mappings().fetchone()

        if not comment:
            raise HTTPException(
                status_code=403,
                detail="댓글을 수정할 권한이 없습니다."
            )
        if comment["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="댓글을 삭제할 권한이 없습니다."
            )
        
        query_delete_comment = """
        DELETE from comments
        WHERE id = :comment_id
        """

        db.execute(text(query_delete_comment), {
            "comment_id": comment_id
        })
        db.commit()
        return{"message": "댓글 삭제가 완료되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"댓글 삭제 중 오류가 발생했습니다. {str(e)}"
        )
    
