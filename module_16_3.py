from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

users = {
    '1': 'Имя: Example, возраст: 18'
}

@app.get('/users')
def get_users():
    return users


@app.post('/user/{username}/{age}')
def add_user(
        username: str = Path(..., min_length=5, max_length=20, example="UrbanUser", description="Enter username"),
        age: int = Path(..., ge=18, le=120, example=24, description="Enter age")
):
    user_id = str(max(map(int, users.keys())) + 1) if users else '1'
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"User {user_id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: str,
        username: str = Path(..., min_length=5, max_length=20, example="UrbanProfi", description="Enter username"),
        age: int = Path(..., ge=18, le=120, example=28, description="Enter age")
):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"User {user_id} has been updated"


@app.delete('/user/{user_id}')
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return f"User {user_id} has been deleted"


# Запуск сервера FastAPI
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

