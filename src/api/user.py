# /c/Users/관리자/Desktop/projects/todos/src/api/user.py 내용
from fastapi import Body, HTTPException, Depends, APIRouter
from src.schema.request import SignUpRequest, LogInRequest  # 추가
from src.schema.response import UserSchema, JWTResponse     # 추가
from src.service.user import UserService
from src.database.orm import User
from src.database.repository import UserRepository

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

    # user(id, username) 값 반환
    return UserSchema.from_orm(user)

@router.post("/log-in")                     # 추가
def user_log_in_handler(
    request: LogInRequest,
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends(),
    
):
    # 사용자 정보 DB 조회
    user: User | None = user_repo.get_user_by_username(username=request.username)
    if not user:
        raise HTTPException(status_code=404, detail = "User Not Found")
    
    # 비밀번호 검증
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password
    )
    if not verified:
        raise HTTPException(status_code=401, detail = "Not Authorized")
    
    # jwt 생성
    access_token: str = user_service.create_jwt(username=user.username)
    
    # jwt 반환
    return JWTResponse(access_token=access_token)