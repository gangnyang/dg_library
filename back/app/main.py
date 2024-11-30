from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
from .routers import users, books, comments, loan, external_books, programs, librarians

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React 개발 서버 주소
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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request headers: {request.headers}")
    response = await call_next(request)
    return response


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

conf = ConnectionConfig(
    MAIL_USERNAME="dwdw7645@gmail.com",
    MAIL_PASSWORD="lfap ncsm onev conc", 
    MAIL_FROM="dwdw7645@gmail.com",
    MAIL_FROM_NAME="dwdw7645",
    MAIL_PORT=587, 
    MAIL_SERVER="smtp.gmail.com", 
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    VALIDATE_CERTS=True,
)

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

@app.post("/send-mail/")
async def send_mail(email: EmailSchema, background_tasks: BackgroundTasks):
    # 메일 구성
    message = MessageSchema(
        subject=email.subject,
        recipients=["2020111983@dgu.ac.kr"],  # 받는 이메일
        body=f"From: {email.email}\n\n{email.message}",
        subtype="html",  # HTML 형식 가능
    )

    # 메일 전송
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)  # 비동기 백그라운드 전송
    return {"message": "성공적으로 전송되었습니다!"}