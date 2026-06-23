from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from database.orm import ToDo

from schema.response import ToDoListSchema, ToDoSchema
from schema.request import CreateToDoRequest

app = FastAPI()


#----------------GET 조회-----------------------------


@app.get("/")
def health_check_handler():
    return {"Hello": "World"}

todo_data = {
    1: {
        "id": 1,
        "contents": "실전 Fastapi 1번",
        "is_done": False
    },
    2: {
        "id": 2,
        "contents": "실전 Fastapi 2번",
        "is_done": True},

    3: {
        "id": 3,
        "contents": "실전 Fastapi 3번",
        "is_done": False,
        }}

@app.get("/todos", status_code=200)
def get_todos_handler(
        order : str | None = None,
        session:Session = Depends(get_db),
):
    todos : List[ToDo] = get_todos(session=session)
    if order and order == "DESC" :
        return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos])

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id:int,
        session:Session = Depends(get_db),):
        todo : ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
        if todo :
            return ToDoSchema.from_orm(todo)
        raise HTTPException(status_code=404, detail="Not Found")

#----------------POST 생성 -----------------------------


@app.post("/todos", status_code=201)
def create_todo_handler(
        request:CreateToDoRequest,
        session:Session = Depends(get_db),
)->ToDoSchema:
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo)
    return ToDoSchema.from_orm(todo)


#----------------PATCH 수정-----------------------------
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id:int,
        is_done : bool = Body(..., embed=True),
        session:Session = Depends(get_db),
):
        todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
        if todo :
            todo.done() if is_done else todo.undone()
            todo: ToDo = update_todo(session=session, todo=todo)
            return ToDoSchema.from_orm(todo)
        raise HTTPException(status_code=404, detail="Not Found")


#----------------DELTE 수정-----------------------------
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id:int,
        session:Session = Depends(get_db),
):
        todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Not Found")

        delete_todo(session=session, todo_id=todo_id)


