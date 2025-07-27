from pydantic import BaseModel
from typing import Optional, List

class ValidateUser(BaseModel):
    username: str
    password: str
    
class RegisterUser(BaseModel):
    username: str
    password: str
    email: str 
    phone: str