
from fastapi import Request,HTTPException,status,Depends
from sqlmodel import Session,select
from core.db import get_db
from auth.models import User
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from core.settings import setting


async def get_current_user(request: Request,db : Session = Depends(get_db)):
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
    auth_header = request.headers.get("Authorization")
    print(f"Auth header is {auth_header}")
    if not auth_header or not auth_header.startswith("jwt"):
        raise error

    token = auth_header.split(" ")[1]
    print(f"Toke is {token}")
    if not token: 
        raise error
    try:
        token_data = jwt.decode(token,setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        print(f"Token data is {token_data}")
    except ExpiredSignatureError as e:
        print(f"Error 1 {e}")
        raise error
    except InvalidTokenError as e:
        print(f"Error 2 {e}")
        raise error
        
    print(f"Decoded values is {token_data}")
    user_email = token_data.get("email")
    if not user_email:
        raise error
    print("Decoded email is",user_email)
        
    user = db.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise error        
        
    return user
