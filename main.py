from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import get_todos

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
        return todos[::-1]
    return todos

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id:int):
    todo = todo_data.get(todo_id)
    if todo :
        return todo
    raise HTTPException(status_code=404, detail="Not Found")

#----------------POST 생성 -----------------------------

class CreateToDoRequest(BaseModel):
    id : int
    contents: str
    is_done:bool


@app.post("/todos", status_code=201)
def create_todo_handler(request:CreateToDoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]


#----------------PATCH 수정-----------------------------
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id:int,
        is_done : bool = Body(..., embed=True),
):
    todo = todo_data.get(todo_id)
    if todo :
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_coe=404, detail="Not Found")


#----------------DELTE 수정-----------------------------
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id:int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="Not Found")