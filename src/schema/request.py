# /c/Users/관리자/Desktop/projects/todos/src/schema/request.py 내용
from pydantic import BaseModel

class CreateToDoRequest(BaseModel):
    contents: str
    is_done: bool
    
class SignUpRequest(BaseModel):
    username: str
    password: str

class LogInRequest(BaseModel):
    username: str
    password: str