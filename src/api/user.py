# /c/Users/관리자/Desktop/projects/todos/src/api/user.py 내용
from fastapi import APIRouter, Depends
from schema.request import SignUpRequest
from schema.response import UserSchema          # 추가
from service.user import UserService
from database.orm import User
from database.repository import UserRepository

router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends()
):
    # 해싱된 비밀번호 생성
    hashed_password: str = user_service.hash_password(
        plain_password = request.password
    )
    # 사용자 생성
    user: User = User.create(
        username = request.username,
        hashed_password = hashed_password
    )
    # 사용자를 DB에 저장
    user: User = user_repo.save_user(user=user) # 이 시점에서 사용자의 id 값 = int로 들어감, 실제 DB에 사용자가 생성됨

    # user(id, username) 값 반환                # 추가
    return UserSchema.from_orm(user)

@router.post("/log-in")
def user_log_in_handler():
    return True