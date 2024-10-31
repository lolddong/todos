# /c/Users/관리자/Desktop/projects/todos/src/service/user.py 내용
import bcrypt

class UserService:
    encoding: str = "UTF-8"
    def hash_password(self, plain_password: str) -> str:
        '''
        input:
            - plain_password: string
        output:
            - hashed_password: string
        '''
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)