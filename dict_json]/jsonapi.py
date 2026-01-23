from datetime import datetime
import random
import string

from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

app=FastAPI()

import json
from pydantic import BaseModel
class UserCreate(BaseModel):

    name:str
    age:int
    is_active:bool
class OrderCreate(BaseModel):
    name:str
    tip:str
    is_active:bool


FILE_NAME = "data.json"

def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)
@app.post("/users")
def create_user(user:UserCreate):
    data = load_data()

    user_id = max([int(i) for i in data.keys()], default=0) + 1

    data[user_id] = {
        "id": user_id,
        "name": user.name,
        "age": user.age,
        "is_active": user.is_active
    }

    save_data(data)
    return data[user_id]




@app.get("/user/")
def user_list():
    data=load_data()
    try:
        return data
    except :
        JSONResponse(status_code=404)


@app.get("/user/{user_id}/get")
def user_one(user_id:int):
    data=load_data()
    try:
        user=data[f"{user_id}"]

        return user
    except:
        JSONResponse(status_code=404)

@app.put("/user/{user_id}/put")
def update_user(user_id:int):
    data=load_data()
    try:
        user=data[f"{user_id}"]
        user["name"]="Asror"
        user["age"]=20
        data[f"{user_id}"]=user
        save_data(data)
        return data[f"{user_id}"]
    except:
     JSONResponse(status_code=404)
@app.delete("user/{user_id}/delete")
def user_delete(user_id:int):
    data=load_data()
    try:
        del data[user_id]
        return "o'chirildi"
    except:
        return JSONResponse(status_code=404)
    
@app.patch("/user/{user_id}/putch")
def user_patch(user_id:int):
    data=load_data()
    try:
        user=data[f"{user_id}"]
        user["age"]=25
        data[f"{user_id}"]=user
        return data[f"{user_id}"]
    except:
        return JSONResponse(status_code=404)
    

@app.get("/user/{user_name}/")
def user_name_list(user_name:str):
    data=load_data()
    try:
     for i in  data.keys():
       if data[i]["name"]==user_name:
           return data[i]
    except:
        return JSONResponse(status_code=404) 
      
@app.post("/order/create")
def create_order(order:OrderCreate):
    data=load_data()
    id=max([int(i) for i in data.keys()],default=0)+1
    data[id]={
        "id":id,
        "name":order.name,
        "tip":order.is_active

    }
    save_data(data=data)
    return data[id]
@app.get("/order/list")
def order_list():
    data=load_data()
    try:
        return data
    except:
        JSONResponse(status_code=404)
@app.put("/order/{order_id}/")
def update_order(order_id:int):
    data=load_data()
    try:
        order=data[order_id]
        order["name"]="Olma"
        order["tip"]="Meva"
        order["is_active"]=True
        data[order_id]=order
        return order
    except:
        return JSONResponse(status_code=404)        
    