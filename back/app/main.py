from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .routers import users, books, comments, loan, external_books, programs, librarians

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 각 파일에서 정의된 라우터를 main에 추가
app.include_router(users.router, prefix="", tags=["User"])
app.include_router(books.router, prefix="", tags=["Book"])
app.include_router(comments.router, prefix="", tags=['Comments'])
app.include_router(loan.router, prefix="", tags=["Loan"])
app.include_router(external_books.router, prefix="", tags=["External_books"])
app.include_router(programs.router, prefix="", tags=["Programs"])
app.include_router(librarians.router, prefix="", tags=["Librarians"])

@app.get("/")
def root():
    return {"message": "Hi"}


# Swagger UI에 Bearer Token 인증 추가
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API with JWT Bearer Token Authentication",
        routes=app.routes,
    )
    # Bearer Auth 스키마 정의
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # 모든 경로에 BearerAuth 적용
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# OpenAPI 스키마 커스터마이즈
app.openapi = custom_openapi
