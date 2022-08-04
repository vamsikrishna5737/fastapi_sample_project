from sqlalchemy import Column, Integer, String
from .database import Base


# creating table for database 
# Initializing all the column in database with validation 

class UserData(Base):
    __tablename__ = "usertable"

    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    mobileNumber = Column(Integer)
    state = Column(String)
    country = Column(String)

class AccountData(Base):
    __tablename__ = "Accounttable"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

