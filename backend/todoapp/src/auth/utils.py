from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from core.settings import setting

pass_context = CryptContext(schemes=["argon2"], deprecated="auto")

class Hasher():
    
    @staticmethod
    def hash_pass(palin_pass : str) -> str:
        return pass_context.hash(palin_pass)
    
    @staticmethod
    def verify_pass(plain_pass : str, hash_pass : str) -> bool:
        return pass_context.verify(plain_pass,hash_pass)
    


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt

