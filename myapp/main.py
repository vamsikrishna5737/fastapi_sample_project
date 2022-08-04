from typing import List
from fastapi import FastAPI , Depends,status, HTTPException
from . import schemas, models
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .hashing import hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/createuserdata',status_code=201, tags=["User Management"])
def create_userData(req : schemas.test, db : Session = Depends(getDb)):
    try:
        newData = models.UserData(
            userName = req.userName,
            mobileNumber = req.mobileNumber,
            state = req.state,
            country = req.country
        )

        db.add(newData)
        db.commit()
        db.refresh(newData)

        return {
            "status": "ok",
            "message": "data created"
        }


    except Exception as e:
        return {
            "status": "Failed",
            "message": str(e)
        }    

@app.get('/getuserdata', response_model= List[schemas.Showtest], tags=["User Management"])
def Get_UserData(db : Session = Depends(getDb)):

    try:
        allData = db.query(models.UserData).all()
        if not allData:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"no users available")
        return allData

    except Exception as e:
        return {
            "status": "Failed",
            "message": str(e)
        }   

@app.get('/getuserbyid/{id}',response_model= schemas.Showtest, tags=["User Management"])
def Get_Userbyid(id,db : Session = Depends(getDb)):
    iddata = db.query(models.UserData).filter(models.UserData.id == id).first()
    if not iddata:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"no user with id {id} available")
    return iddata    

@app.put('/edituserdata/{id}', tags=["User Management"])
def Edit_UserData(id: int,req: schemas.test ,db : Session = Depends(getDb)):
    try:
        updatedata = {
        "userName" : req.userName,
        "mobileNumber" : req.mobileNumber,
        "state" : req.state,
        "country" : req.country
        }   

        updateddata =  db.query(models.UserData).filter(models.UserData.id == id).update(updatedata)

        if not updateddata:
            return {
                "status":"failed",
                "msg":f"user id {id} not found"
            }
        db.commit()

        return {
            "status": "ok",
            "data": updatedata
        }    
    except Exception as e:
        return{
            "status": "failed",
            "msg": str(e)
        }    

@app.delete('/deleteuserdata/{id}', tags=["User Management"])
def Delete_UserData(id: int,db : Session = Depends(getDb)):
    try:
        deletedUser =db.query(models.UserData).filter(models.UserData.id == id).delete(synchronize_session=False)
        if not deletedUser:
            return{
                "status":"failed",
                "msg": f'Data not found in database with id:{id}'
            }
        db.commit()    

        return {
            "status": "ok",
            "message": f"successfully deleted the id:{id}"
        }
    except Exception as e:
        return{
            "status": "failed",
            "msg": str(e)
        }            



@app.post('/Create_Account',status_code=201, tags=["Account Management"])
def Create_Account(req : schemas.Account,db : Session = Depends(getDb)):
    
    newAccount = models.AccountData(
        name = req.name,
        email = req.email,
        password = hash.bcrypt(req.password)
    )

    db.add(newAccount)
    db.commit()
    db.refresh(newAccount)
    
    return {
        "status" : "created Account",
        "data" : newAccount
    }

@app.get('/Get_Account/{id}', response_model=schemas.ShowAccount, tags=["Account Management"])
def Get_Account(id,db:Session =Depends(getDb)):
    account = db.query(models.AccountData).filter(models.AccountData.id == id).first()
    if not account:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"user with th id {id} is not available")
    return account



@app.post('/Login_Account', tags=["Account Management"])
def Login_Account(req : schemas.Login,db:Session =Depends(getDb)):
    logged= db.query(models.AccountData).filter(models.AccountData.email == req.username).first()
    if not logged:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"no user")
    if not hash.verify(logged.password,req.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"wrong password")

    return logged    


      