from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

users = []

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/users')
def get_users():
    return users

@app.post('/user/{username}/{age}')
def add_user(
        username: str = Path(..., min_length=5, max_length=20, example="UrbanUser", description="Enter username"),
        age: int = Path(..., ge=18, le=120, example=24, description="Enter age")
):
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1

    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{id}/{username}/{age}')
def update_user(
        id: int = Path(..., description="User ID"),
        username: str = Path(..., min_length=5, max_length=20, example="UrbanProfi", description="Enter username"),
        age: int = Path(..., ge=18, le=120, example=28, description="Enter age")
):
    try:
        user = next(user for user in users if user.id == id)
        user.username = username
        user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}', response_model=User)
def delete_user(user_id: int = Path(..., description="User ID")):
    try:
        user = next(user for user in users if user.id == user_id)
        users.remove(user)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.get('/user/{user_id}')
def get_user(request: Request, user_id: int = Path(..., description="User ID")):
    try:
        user = next(user for user in users if user.id == user_id)
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
