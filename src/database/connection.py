# /c/Users/관리자/Desktop/projects/todos/src/database/connection.py 내용
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL,
                       # echo=True,         # 제거: DB에서 쿼리가 계속 발생하면 로그를 보기 힘들기 때문
                       )
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()