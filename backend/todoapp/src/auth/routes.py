from fastapi import APIRouter,Depends,HTTPException,status, Request
from .schemas import UserLogin,UserSignup
from core.db import get_db
from sqlmodel import Session,select
from .utils import Hasher, create_access_token
from .models import User
from core.settings import setting
from core.dependency import get_current_user


#logging.basicConfig(filename="app.log",filemode="a",encoding="utf-8")

auth = APIRouter(prefix="/auth",tags=["auth"])




@auth.post("/signup")
def signup_user(user_info : UserSignup,db : Session = Depends(get_db)):
    existing_email = db.exec(select(User).where(User.email == user_info.email)).first()
    if existing_email:
        print("Already email exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email {user_info.email} already exists")
    else:
        hashed_pass = Hasher.hash_pass(user_info.password)
        db_user = User(email=user_info.email,
                        password=hashed_pass)
        
        print(f"Final user info before saving to db {user_info}")
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"msg" : "User signup success"}
    
    
    
    

@auth.post("/login")
def login_user(user_info : UserLogin, db : Session = Depends(get_db)):
    login_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email or password incorrect")
    is_email_exists = db.exec(select(User).where(User.email == user_info.email)).first()
    
    if not is_email_exists:
        raise login_error
    
    is_password_correct = Hasher.verify_pass(user_info.password,is_email_exists.password)
    if not is_password_correct:
        raise login_error
    
    data = {"email": is_email_exists.email,"_id": is_email_exists.id}
    token = create_access_token(data)
    
    
    return {"token" : token}






@auth.get("/is_authenticated")
def is_autheticated(user = Depends(get_current_user)):
    print(f"User we got is {user}")
    return {"authenticated": True}


#Protected route
@auth.get("/test")
def test(user = Depends(get_current_user)):
    return {"msg" : f"Hello {user.email}"}

