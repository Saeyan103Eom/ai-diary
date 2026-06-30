from fastapi import FastAPI

from api import todo

app = FastAPI()
app.include_router(todo.router)


#----------------GET 조회-----------------------------


@app.get("/")
def health_check_handler():
    return {"Hello": "World"}




