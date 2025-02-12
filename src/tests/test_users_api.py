# /c/Users/관리자/Desktop/projects/todos/src/tests/test_users_api.py 내용
from src.service.user import UserService
from src.database.orm import User
from src.database.repository import UserRepository

username = 'test11'
def test_user_sign_up(client, mocker):                  # mocker는 fixture
    hashed_password = mocker.patch.object(              # UserService.hash_password 메소드에 mocking 적용
        UserService,
        "hash_password",
        return_value="hashed"
    )
    
    user_create = mocker.patch.object(                  # User.create 메소드에 mocking 적용
        User,
        "create",
        return_value=User(id=None, username=username, password="hashed")
    )
    
    mocker.patch.object(                                # UserRepository.save_user 메소드에 mocking 적용
        UserRepository,
        "save_user",
        return_value=User(id=1, username=username, password="hashed")
    )
    
    body = {                                            # API에 넘겨줄 body 추가
        "username": username,
        "password": "plain"
    }
    response = client.post("users/sign-up", json=body)  # json 형식으로 body 넘겨줘서 POST 요청 보내기 추가
    print(hashed_password.call_args_list)
    hashed_password.assert_called_once_with(            # UserService.hash_password 호출 여부 검증
        plain_password="plain"
    )

    user_create.assert_called_once_with(                # User.create 호출 여부 검증
        username=username, hashed_password="hashed"
    )
    
    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": username}     # 반환값으로 UserRepository.save_user 검증