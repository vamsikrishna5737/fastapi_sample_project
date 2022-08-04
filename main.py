from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class test(BaseModel):
    id : int
    name : str

@app.post('/')
def home(sample : test):
    return {'message' : sample.name}

@app.get('/item/{id}')
def items(id: int):
    return {'item_id' : id}    

@app.get('/item')
def query(score : int,limit : int):
    return {'data': {f'this is my score -{score}',limit}}


