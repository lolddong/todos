# /c/Users/관리자/Desktop/projects/todos/src/api/todo.py 내용
from fastapi import Body, HTTPException, Depends, APIRouter
from typing import List	

from database.repository import ToDoRepository, ToDo
from schema.response import ToDoSchema, ToDoListSchema
from schema.request import CreateToDoRequest

router = APIRouter(prefix='/todos')

# GET Method 사용하여 전체 조회 API
@router.get("", status_code=200)
def get_todos_handler(
    order: str | None = None,
    todo_repo: ToDoRepository = Depends(),
) -> ToDoListSchema:
    todos: List[ToDo] = todo_repo.get_todos()
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
    todo: ToDo = todo_repo.create_todo(todo=todo) # id=int
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
    