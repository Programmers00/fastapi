from distutils.util import strtobool
from urllib import request  #URL handling modules
import uvicorn #ASGI web server implemenation for Python
from typing import Optional #Support for type hints
from fastapi import FastAPI
from pydantic import BaseModel  #Data validation and settings management using python type annotations
import requests #Simple HTTP library for Python

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str

@app.get("/cities")
def get_cities():
    results = []
    for city in db:
        strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        r = requests.get(strs)
        cur_time = r.json()['datetime']
        results.append({'name': city['name'], 'timezone': city['timezone'], 'cuttent_time':cur_time})
    return results

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
    r = requests.get(strs)
    cur_time = r.json()['datetime']
    return {'name': city['name']}, {'timezone': city['timezone']}, {'cuttent_time':cur_time}

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())

    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}

# @app.get("/users/{user_id}")
# def get_user(user_id: str):
#     return {"user_id": user_id}

# @app.get("/")   # GET / 를 호출할 수 있는 앤드 포인트
# def read_root():    # 함수명
#     return {"Hello": "World"}   # 반환


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    # uvicorn.run(app)
    uvicorn.run("main:app", reload=True) #실제로는 코드밖에서 실행해야 하기때문에 지금의 uvicron.run(app, reload=True)와 같이 사용할 수 없다.
