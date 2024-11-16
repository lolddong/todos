# /c/Users/관리자/Desktop/projects/todos/src/service/user.py 내용
from datetime import datetime, timedelta        # 추가
from jose import JWTError                       # 추가
import bcrypt
import logging

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "a0ef6b27d5050d0040867160134b69bd673f640dd1db8db8b0ee0166114f4cfa"    # 추가
    jwt_algorithm: str = "HS256"                                                            # 추가
    
    def hash_password(self, plain_password: str) -> str:
        '''
        input: plain_password (str)
        output: hashed_password (str)
        function: receives plain-text password and returns hashed password
        '''
        logging.info("hash_password called with: %s", plain_password)
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        '''
        input: plain_password (str)
        output: hashed_password (str)
        function: receives plain-text password and hashed password, returns bool whether they are the same password or not
        '''
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )
        
    def create_jwt(self, username: dict) -> str:        # 추가
        return jwt.encode(
            {"sub": username,
             "exp": datetime.now() + timedelta(days=1) },
            self.secret_key,
            algorithm=self.jwt_algorithm
        )