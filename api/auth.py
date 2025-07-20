from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel,Field 
from database import collection
from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from jose import jwt,JWTError
import uuid


router=APIRouter()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


class UserBase(BaseModel):
    username:str
    password:str
    
class ToDoBase(BaseModel):
    title: str = None
    desc: str = None
    checked: bool = None
    
class ToDoWithId(BaseModel):
    title:str
    desc:str
    checked:bool=False
    id:str=Field(default_factory=lambda:str(uuid.uuid4()))

def get_user(username:str):
    if collection.find_one({"username":username}):
        return True
    else:
        return False
@router.post("/register",status_code=201)
async def create_user(user:UserBase):
    username=user.username
    password=user.password
    if(get_user(username)):
        raise HTTPException(status_code=400,detail="Username already exist")
    hashed_pw = pwd_context.hash(password)
    new_user = {
        "username": username,
        "hashed_password": hashed_pw,
        "todos": []
    }
    collection.insert_one(new_user)
    return {"message":"User Created Successfully"}

@router.post("/login")
async def login_for_access_token(user:UserBase):
    db_user=collection.find_one({"username":user.username})
    if not db_user or not pwd_context.verify(user.password,db_user['hashed_password']):
        raise HTTPException(status_code=400,detail='Invalid username or password')
    token=create_access_token({"sub":db_user['username']})
    return {"access_token": token, "token_type": "bearer"}

def create_access_token(data:dict):
    to_encode=data.copy()
    expire_time=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
@router.get("/verify-token")
def verify(token: str):
    payload = verify_token(token)
    return {"message": "Token is valid", "user": payload["sub"]}

async def get_curr_user(token:str):
    payload=verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user=collection.find_one({"username":payload['sub']})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return {"username":user["username"]}


@router.post("/add-todo")
async def add_todo(todo:ToDoBase,current_username: dict = Depends(get_curr_user)):
    user_todo=ToDoWithId(title=todo.title,desc=todo.desc,checked=todo.checked)
    db_user=collection.find_one({"username": current_username["username"]})
    if db_user is None:
        raise HTTPException(status_code=400,detail="Adding todo failed")
    collection.update_one(
        {"username": current_username["username"]},
        {"$push": {"todos": user_todo.model_dump()}} 
    )

    return {"message": "Todo created", "todo": user_todo}
    
@router.delete("/delete-todo")
async def delelte_todo(todo_id:str,current_username:dict=Depends(get_curr_user)):
    todos=collection.find_one({"username": current_username["username"]})["todos"]
    k=False
    for dic in todos:
        if(dic["id"]==todo_id):
            k=True
    if not k:
        raise HTTPException(status_code=400,detail='No such todo')
    collection.update_one(
       {"username": current_username["username"]},
        {"$pull":{"todos":{"id":todo_id}}}
    )
    return {"message":"Todo deleted successfully"}

@router.get("/todos")
async def get_todos(current_username:dict=Depends(get_curr_user)):
    user = collection.find_one({"username": current_username["username"]})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"todos": user["todos"]}

@router.put("/update-todo")
async def update_todo(todo_id:str,todo_update:ToDoBase,current_username:dict=Depends(get_curr_user)):
    db_user = collection.find_one({"username": current_username["username"]})
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    todos = db_user.get("todos", [])

    updated = False
    for todo in todos:
        if todo["id"] == todo_id:
            if todo_update.title is not None:
                todo["title"] = todo_update.title
            if todo_update.desc is not None:
                todo["desc"] = todo_update.desc
            if todo_update.checked is not None:
                todo["checked"] = todo_update.checked
            updated = True
            break

    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")

    collection.update_one(
        {"username": current_username["username"]},
        {"$set": {"todos": todos}}
    )

    return {"message": "Todo updated successfully"}