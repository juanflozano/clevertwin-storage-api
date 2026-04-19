from pydantic import BaseModel

class UserRegister(BaseModel):
    company: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Event(BaseModel):
    company: str
    event_type: str
    file_size: int
    file_type: str