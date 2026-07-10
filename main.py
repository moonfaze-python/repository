#pip install fastapi uvicorn
#uvicorn main:app --port 8000 --reload
#ctrl+shift+I открыть DevTools
#git add .
#git commit -m "Первый коммит"
#git push -u origin master
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

book = ''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ('http://localhost:3000'),
    allow_methods = ['*']
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

tasks: list[TaskSchema] = []

@app.get('/tasks')
def read_tasks() -> list[TaskSchema]:
    return tasks

@app.post('/tasks')
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()),title=payload.title,completed=False)
    tasks.append(new_task)
    return new_task

class TaskCreateBook(BaseModel):
    book : str

@app.post('/book')
def create_book(payload: TaskCreateBook):
    global book
    book = payload.book
    return book

@app.get('/book')
def read_book():
    global book
    return f'Любимая книга {book}'