from sqlalchemy.orm import Session
from . import models, schemas


# Read data
def getUser(db: Session, userId: int):
    return db.query(models.User)\
        .filter(models.User.id == userId)\
        .first()


# Read data
def getUserByEmail(db: Session, email: str):
    return db.query(models.User)\
        .filter(models.User.email == email)\
        .first()


# Read data
def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User)\
        .offset(skip).limit(limit).all()


# Create data
def createUser(db: Session, user: schemas.UserCreate):
    fakeHashedPassword = user.password + "not really hashed"
    userDB = models.User(email=user.email, hashed_password=fakeHashedPassword)
    db.add(userDB)
    db.commit()
    db.refresh(userDB)
    return userDB
