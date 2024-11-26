# /c/Users/관리자/Desktop/projects/todos/src/security.py 내용
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

def get_access_token(
    auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if auth_header is None:
        raise HTTPException(
            status_code=401,
            detail='Not Authorized',
        )
    return auth_header.credentials