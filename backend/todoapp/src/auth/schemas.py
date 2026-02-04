from pydantic import EmailStr,BaseModel

class UserSignup(BaseModel):
    email : EmailStr 
    password : str
    
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str

    