# /c/Users/관리자/Desktop/projects/todos/src/service/user.py 내용
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
import logging

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "a0ef6b27d5050d0040867160134b69bd673f640dd1db8db8b0ee0166114f4cfa"
    jwt_algorithm: str = "HS256"
    
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
        
    def create_jwt(self, username: dict) -> str:
        return jwt.encode(
            {"sub": username,
             "exp": datetime.now() + timedelta(days=1) },
            self.secret_key,
            algorithm=self.jwt_algorithm
        )
    
    def decode_jwt(self, access_token: str) -> str:       # 추가
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # expire: 원래는 여기서 토큰의 만료 기간을 검증하는 부분 필요하나 우리는 거기까지 안 할 것임
        return payload['sub'] # username