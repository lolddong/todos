# /c/Users/관리자/Desktop/projects/todos/src/tests/test_todos_api.py 내용
from src.schema.response import ToDoSchema
from src.database.orm import ToDo, User 
from src.database.repository import ToDoRepository, UserRepository
from src.service.user import UserService

# GET Method 사용하여 전체 조회 API 검증
# def test_get_todos(client, mocker):
#     # order = ASC
#     mocker.patch.object(ToDoRepository, "get_todos", return_value=[
#         ToDo(id=1, contents="FastAPI Section 0", is_done=True),
#         ToDoSchema(id=2, contents="FastAPI Section 2", is_done=False),
#     ])
#     response = client.get("/todos")
#     assert response.status_code == 200
#     assert response.json() == {
#         "todos": [
#             {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
#             {"id": 2, "contents": "FastAPI Section 2", "is_done": False},
#         ]
#     }
    
#     # order = DESC
#     response = client.get("/todos?order=DESC")
#     assert response.status_code == 200
#     assert response.json() == {
#         "todos": [
#             {"id":2, "contents": "FastAPI Section 2", "is_done": False},
#             {"id":1, "contents": "FastAPI Section 0", "is_done": True},
#         ]
#     }

# GET Method 사용하여 username의 todo 목록 조회 API 검증
def test_get_todos(client, mocker):
    access_token: str = UserService().create_jwt(username="test")
    headers = {'Authorization': f"Bearer {access_token}"}
    user = User(id=1, username="test", password="hashed")
    user.todos = [
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ]
    mocker.patch.object(
        UserRepository, "get_user_by_username", return_value=user
    )
    # order = ASC
    response = client.get('/todos', header=headers)
    assert response.status_code == 200

# GET Method 사용하여 단일 조회 API 검증
def test_get_todo(client, mocker):
    # 상태코드 200
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id"
        return_value = ToDo(id=1, contents="todo", is_done=True),
    )   
    response = client.get("/todos/1")   # path에 하위 서브 path 적어주기
    assert response.status_code == 200
    assert response.json() == {"id":1, "contents": "todo", "is_done": True }
    
    # 상태코드 404
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id", return_value = None,)    
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"ToDo Not Found"}

# POST Medthod 사용하여 todo 생성 API 검증
def test_create_todo(client, mocker):
    create_spy = mocker.spy(ToDo, "create")     # mocker의 spy 기능 사용
    mocker.patch.object(ToDoRepository, "create_todo",
        return_value=ToDo(id=1, contents="todo", is_done=False),
    )
    
    body = {
        "contents": "test",
        "is_done": False,
    }
    response = client.post("/todos", json=body)
    
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False
    
    assert response.status_code == 201
    assert response.json() == {"id":1, "contents":"todo", "is_done":False}


# PATCH Method 사용하여 is_done 값 수정 API 검증
def test_update_todo(client, mocker):
    # 상태코드 200
    
    # get_todo_by_todo_id 검증
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id",
        return_value = ToDo(id=1, contents="todo", is_done=True),
    )
    
    # done() 또는 undone() 검증
    # done = mocker.patch.object(ToDo, "done") # ToDo 객체의 done() 메소드 호출
    undone = mocker.patch.object(ToDo, "undone") # ToDo 객체의 undone() 메소드 호출
    
    # update_todo 검증
    mocker.patch.object(ToDoRepository, "update_todo",
        return_value = ToDo(id=1, contents="todo", is_done=False),   # done 경우 is_done = True, undone 경우 is_done=False 주기
    )
    
    response = client.patch("/todos/1", json={"is_done": False})   # done 경우 "is_done": True, undone 경우 "is_done": False 주기
    
    # done() 또는 undone() 검증 - done 또는 undone이 한 번 호출되었는지 확인. 아닐 경우 AssertionError 발생
    # done.assert_called_once_with()
    undone.assert_called_once_with()
    
    assert response.status_code == 200
    assert response.json() == {"id":1, "contents": "todo", "is_done": False }
    
    # 상태코드 404
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id",
        return_value = None,
    )   
    response = client.patch("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {"detail":"ToDo Not Found"}
  
# DELTE Method API 검증  
def test_delete_todo(client, mocker):
    # 상태코드 204
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id",
        return_value = ToDo(id=1, contents="todo", is_done=True),
    )
    mocker.patch.object(ToDoRepository, "delete_todo", return_value = None,) 
    response = client.delete("/todos/1")    # path에 하위 서브 path 적어주기
    assert response.status_code == 204      # status_code만 주고 response.json()는 assert 안 해봐도 됨! 반환값이 없을 것이기에
    
    # 상태코드 404
    mocker.patch.object(ToDoRepository, "get_todo_by_todo_id",return_value = None,) 
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"ToDo Not Found"}