# /c/Users/관리자/Desktop/projects/todos/src/api/user.py 내용
from fastapi import Body, HTTPException, Depends, APIRouter, BackgroundTasks    # 추가
from src.schema.request import SignUpRequest, LogInRequest, CreateOTPRequest, VerifyOTPRequest  # 추가
from src.schema.response import UserSchema, JWTResponse
from src.service.user import UserService
from src.database.orm import User
from src.database.repository import UserRepository
from src.security import get_access_token
from src.cache import redis_client

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

@router.post("/log-in")
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

@router.post('/email/otp')
def create_otp_handler(
    request: CreateOTPRequest,                  # request body로 email 받음 (request가 get_access_token보다 위로 와야 에러 안 남)
    _: str = Depends(get_access_token),         # access_token 사용 (즉, 회원가입 한, 인증된 사용자만 이메일 인증 가능)
                                                    # 헤더에 access_token이 있어야지만 여기를 통과하지만, access_token을 여기 로직에서 사용할 것은 아니라서 지금은 _로 줄 것
                                                    # 즉, 헤더에 있는지 검증만 하고 실제로 이 값을 사용하지 않을 것
    user_service: UserService = Depends()
    ):
    otp: int = user_service.create_otp()        # OTP 생성 (랜덤한 4자리 숫자)
    redis_client.set(request.email, otp)        # redis에 저장 (key: email, value: OTP, exp=3min)
    redis_client.expire(request.email, 3 * 60)  # 초 단위로 전달해야됨
    return {'otp': otp}                         # OTP를 email에 전송하는 로직을 실습에선 간략하게 이렇게만 구현할 것

@router.post('/email/otp/verify')           # 수정
def verify_otp_handler(
    request: VerifyOTPRequest,                      # request body로 email, otp 받음 (request가 get_access_token보다 위로 와야 에러 안 남)
    background_tasks: BackgroundTasks,      # 추가
    access_token: str = Depends(get_access_token),   # access_token 사용 (즉, 회원가입 한, 인증된 사용자만 요청 가능)
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    ):

    # request로 받은 otp와 redis.get(email)로 받은 otp 비교하여 이메일 인증
    otp: str | None = redis_client.get(request.email)   # key가 잘못됬거나 만료 시 None 반환
    if not otp:
        raise HTTPException(status_code=400, detail='Bad Request')
    if request.otp != int(otp):
        raise HTTPException(status_code=400, detail='Bad Request')
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail='User Not Found')
    # save email to user
    	# 실습에서는 사용자 이메일을 저장했다고 가정하고 진행
    # send email to user                                           # 추가
    background_tasks.add_task(                                     # 추가
        user_service.send_email_to_user,                           # 추가
        email='admin@fastapi.com'                                  # 추가
    )
    return UserSchema.from_orm(user)                # User가 잘 조회되는지 확인