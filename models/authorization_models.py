from pydantic import BaseModel

class ValidateUser(BaseModel):
    username: str
    password: str
    
class RegisterUser(BaseModel):
    username: str
    password: str
    email: str
    phone: str