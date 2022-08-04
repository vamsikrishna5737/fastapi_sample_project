from pydantic import BaseModel 


class test(BaseModel):
    # id : int
    userName : str
    mobileNumber : int
    state : str
    country : str

class Showtest(BaseModel):
    userName : str
    country : str

    class Config:
        orm_mode = True

class Account(BaseModel):
    name : str
    email : str
    password : str

class ShowAccount(BaseModel):
    name : str
    email : str

    class Config:
        orm_mode = True    

class Login(BaseModel):
    username : str
    password : str        