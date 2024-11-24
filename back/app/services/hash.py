from passlib.context import CryptContext

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 검증
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 비밀번호 해싱
def hash_password(password):
    return pwd_context.hash(password)