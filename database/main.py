from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependecy:
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fetching Data
@app.get("/users/", response_model=List[schemas.User])
def readUsers(skip: int = 0, limit: int = 100, db: Session = Depends(getDB)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users


# Fetching Data
@app.get("/users/{user_id}", response_model=schemas.User)
def readUser(userID: int, db: Session = Depends(getDB)):
    userDB = crud.getUser(db, userID=userID)
    if userDB is None:
        raise HTTPException(status_code=404, detail="User not found")
    return userDB


# Inserting Data
@app.post("/users/", response_model=schemas.User)
def createUser(user: schemas.UserCreate, db: Session = Depends(getDB)):
    userDB = crud.getUserByEmail(db, email=user.email)

    if userDB:
        raise HTTPException(status_code=400, detail="Email Used")
    return crud.create_user(db=db, user=user)
