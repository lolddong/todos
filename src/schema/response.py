# /c/Users/관리자/Desktop/projects/todos/src/schema/response.py 내용
from pydantic import BaseModel
from typing import List

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        from_attributes = True
        orm_mode = True # 이거 추가 해야지 ConfigError 안남

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]

class UserSchema(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True
        orm_mode = True # 이거 추가 해야지 ConfigError 안남

class JWTResponse(BaseModel):
    access_token: str