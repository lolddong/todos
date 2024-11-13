# /c/Users/관리자/Desktop/projects/todos/src/database/orm.py 내용
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from schema.request import CreateToDoRequest

Base = declarative_base()

# ToDo 클래스 모델링 한 것
class ToDo(Base):
    __tablename__ = 'todo'
    
    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    
    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"
    
    @classmethod
    def create(cls, request: CreateToDoRequest) -> "ToDo":
        return cls(
            # id값은 DB에 의해 자동으로 결정 되서 별도로 지정안해줌
            contents=request.contents,
            is_done=request.is_done,
        )
        
    def done(self) -> "ToDo":    # ToDo의 is_done 값을 True로 변경 후 ToDo 반환
        self.is_done = True
        return self
    
    def undone(self) -> "ToDo":  # ToDo의 is_done 값을 False로 변경 후 ToDo 반환
        self.is_done = False
        return self

# User 클래스 모델링 한 것
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, nullable=False) # unique=True는 내가 넣은 것임
    password = Column(String(256), nullable=False)
    todos = relationship("ToDo", lazy="joined")
    
    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return cls(
            username=username,
            password=hashed_password,
        )