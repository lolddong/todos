# /c/Users/관리자/Desktop/projects/todos/src/api/todo.py 내용
from fastapi import Body, HTTPException, Depends, APIRouter
from typing import List	

from src.database.repository import ToDoRepository, ToDo, UserRepository, User
from src.schema.response import ToDoSchema, ToDoListSchema
from src.schema.request import CreateToDoRequest
from src.security import get_access_token
from src.service.user import UserService

router = APIRouter(prefix='/todos')

# GET Method 사용하여 username의 todo 조회 API          # 변경 (원래: GET Method 사용하여 전체 조회 API)
@router.get("", status_code=200)
def get_todos_handler(
    access_token: str = Depends(get_access_token),
    order: str | None = None,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    # todo_repo: ToDoRepository = Depends(),             # 삭제
) -> ToDoListSchema:
    username: str = user_service.decode_jwt(access_token=access_token)  # 이 username을 통해 사용자 조회
    user: User | None = user_repo.get_user_by_username(username=username)  # 이 user_id를 통해 User(테이블)를 불러와 User에 담긴 ToDo 조회
    if not user: # 회원 탈퇴, etc. 경우
        raise HTTPException(status_code=404, detail='User Not Found')
    # todos: List[ToDo] = todo_repo.get_todos()         # 삭제
    todos: List[ToDo] = user.todos                      # User에 있는 ToDo들을 todos에 담음
    if order and order == "DESC":
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

# GET Method 사용하여 단일 조회 API
@router.get("/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(),
    ) -> ToDoSchema:
    todo:ToDo | None = todo_repo.get_todo_by_todo_id(todo_id = todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# POST Medthod 사용하여 todo 생성 API
@router.post("", status_code=201)
def create_todo_handler(
    request: CreateToDoRequest,
    todo_repo: ToDoRepository = Depends(),
    ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)          # id=None
    todo: ToDo = todo_repo.create_todo(todo=todo)      # id=int
    return ToDoSchema.from_orm(todo)

# PATCH Method 사용하여 is_done 값 수정 API
@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: ToDoRepository = Depends(),
    ):
    todo:ToDo | None = todo_repo.get_todo_by_todo_id(todo_id = todo_id)
    if todo:
        # update - is_done값이 True이면 todo.done() 실행, False이면 todo.undone() 실행
        todo.done() if is_done else todo.undone()
        todo: ToDo = todo_repo.update_todo(todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# DELETE Method 사용하여 todo 아이템 삭제 API
@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(),
    ):
    todo:ToDo | None = todo_repo.get_todo_by_todo_id(todo_id = todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    todo_repo.delete_todo(todo_id=todo_id)
    