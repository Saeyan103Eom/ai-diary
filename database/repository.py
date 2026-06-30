from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database.orm import ToDo
from typing import List

class ToDoRepository:
     def __init__(self, session:Session):
          self.session = session

     def get_todos(self) -> List[ToDo]:
          return list(self.session.scalars(select(ToDo)))

     def get_todo_by_todo_id(self, todo_id:int) -> ToDo | None:
          return self.session.scalar(select(ToDo).where(ToDo.id == todo_id))

     def create_todo(self, todo:ToDo):
          self.session.add(instance=todo)
          self.session.commit()
          self.session.refresh(instance=todo)
          return todo

     def update_todo(self, todo:ToDo):
          self.session.add(instance=todo)
          self.session.commit()
          self.session.refresh(instance=todo)
          return todo

     def delete_todo(self, todo_id:int) -> None:
          self.session.execute(delete(ToDo).where(ToDo.id == todo_id))
          self.session.commit()

