from datetime import datetime
import random
import string

from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

app=FastAPI()

user_db=dict()

def generete_random_string(length):
    characters=string.ascii_letters+string.digits
    random_string="".join(random.choices(characters,k=length))
    return random_string

@app.post("/users/create")
def user_create():
    user_id=random.randrange(1,1000)
    name=generete_random_string(10)
    age=random.randint(1,60)
    is_active=random.choice([True,False])

    new_user={"id":user_id,
              "name":name,
              "age":age,
              "is_active":is_active,
              "created_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    user_db[user_id]=new_user
    return new_user

@app.get("/users/list/")
def user_list():
    return user_db

@app.get("/users/{user_id}/")
def user_detail(user_id:int):
    try:
        return user_db[user_id]
    
    except KeyError:
        return JSONResponse(
            content={"error":"user not found"},status_code=404

        )

@app.put("/users/{user_id}/") 
def user_update(user_id:int):
    try:
        user=user_db[user_id]
        user["name"]=generete_random_string(10)
        user["age"]=random.randint(1,60)
        user_db[user_id]=user
        return user
    except KeyError:
        return JSONResponse(status_code=404)
@app.delete("/users/{user_id}/")
def user_delete(user_id:int):
    try:
        del user_db[user_id]
        return JSONResponse(status_code=204) 
    except KeyError:
        return JSONResponse(status_code=404)     