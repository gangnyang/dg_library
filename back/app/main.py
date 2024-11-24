from fastapi import FastAPI
from routers import users, books, comments, loan, interloan, external_books, programs, librarians

app = FastAPI()

# 각 파일에서 정의된 라우터를 main에 추가
app.include_router(users.router, prefix="/api/user", tags=["User"])
app.include_router(books.router, prefix="/api/book", tags=["Book"])
app.include_router(comments.router, prefix="/api/comment", tags=['Comments'])
app.include_router(loan.router, prefix="/api/loan", tags=["Loan"])
app.include_router(interloan.router, prefix="/api/interloan", tags=["Interloan"])
app.include_router(external_books.router, prefix="/api/external_books", tags=["External_books"])
app.include_router(programs.router, prefix="/api/programs", tags=["Programs"])
app.include_router(librarians.router, prefix="/api/librarians", tags=["Librarians"])

@app.get("/")
def root():
    return {"message": "Hi"}
