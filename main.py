#pip install fastapi uvicorn
#uvicorn main:app --port 8080 --reload
#ctrl+shift+I открыть DevTools
#git add .
#git commit -m "Первый коммит"
#git push -u origin master
#taskkill /F /IM python.exe
from fastapi import FastAPI,status
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*']
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TakeUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

tasks: list[TaskSchema] = []

@app.get('/tasks')
def read_tasks() -> list[TaskSchema]:
    return tasks

@app.post('/tasks')
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()),title=payload.title,completed=False)
    tasks.append(new_task)
    return new_task

@app.patch('/tasks/{task_id}')
def update_task(task_id:str,payload: TakeUpdateSchema):
    global tasks
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str) -> None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return

#категории

class CategorySchema(BaseModel):
    id: str | None = None
    name: str | None = None

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str

categories:list[CategorySchema] = []

@app.get('/categories')
def read_category() -> list[CategorySchema]:
    return categories

@app.post('/categories')
def create_category(payload:CategoryCreateSchema) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()),name=payload.name)
    categories.append(new_category)
    return new_category

@app.patch('/categories/{category_id}')
def update_category(category_id: str,payload:CategoryUpdateSchema):
    global categories
    for category in categories:
        if category_id == category.id:
            if payload.name is not None:
                category.name = payload.name
            return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

@app.delete('/categories/{category_id}')
def delete_category(category_id:str) -> None:
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

