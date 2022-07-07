from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status

from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

secretKey = "fd542b4ca80cf45e28f41c828e0fa91fd90f4db1fac21a716f5c727ed01875ed"
accessTokenExpMin = 15
algorithmHash = "HS256"

users_db = {
    "carlosvinimsouza": {
        "username": "carlosvinimsouza",
        "full_name": "Carlos Vini. M. Souza",
        "email": "carlosvinimsouza@gmail.com",
        "hashed_password": "$50084369314ff45748bf8b5e8ecc714589ca971b692928019412eab366c72cb6",
        "disabled": False,
    },
    "carloSouza": {
        "username": "carloSouza",
        "full_name": "Carlos Souza",
        "email": "carlosouza@gmail.com",
        "hashed_password": "$fd8e75e93d4f6c46559fd7886cf69b1acbad74376a2e1228c935070facd46017",
        "disabled": True,
    },
}


# Handle JWT tokens
class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    username: str | None = None


# Creating our User
class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    fullName: str | None = None
    disabled: bool | None = None


class UserSaveDB(UserBase):
    hashPassword: str


# Cryptography
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


# Validation Password hashed
def verifyPassword(plainPassword, hashPassword):
    return passwordContext.verify(plainPassword, hashPassword)


def getPasswordHash(password):
    return passwordContext.hash(password)


# Validation User
def getUser(db, username: str):
    if username in db:
        userDict = db[username]
        return UserSaveDB(**userDict)


def authUser(fakeDB, username: str, password: str):
    user = getUser(fakeDB, username)

    if not user:
        return False

    if not verifyPassword(password, user.hashPassword):
        return False

    return user


# Check the next version of 'fakeDecodeToken()'
# New Version in OAuth2 with Password (and hashing)
def createAccessToken(data: dict, expiresDelta: timedelta | None = None):
    toEncode = data.copy()

    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)

    toEncode.update({"expire in": expire})
    encodedJWT = jwt.encode(toEncode, secretKey, algorithm=algorithmHash)
    return encodedJWT


async def getCurrentUser(token: str = Depends(oauth2Scheme)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate your credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secretKey, algorithms=[algorithmHash])
        username: str = payload.get("sub")
        if username is None:
            raise credentialsException
        tokenData = TokenData(username=username)
    except JWTError:
        raise credentialsException

    user = getUser(users_db, username=tokenData.username)
    if user is None:
        raise credentialsException

    return user


async def getCurrentActiveUser(currentUser: User = Depends(getCurrentUser)):
    if currentUser.disabled:
        raise HTTPException(
            status_code=400,
            detail="User Deactivated"
        )

    return currentUser


# GET Methods
@app.get("/users/mylogin/")
async def readMe(currentUser: User = Depends(getCurrentActiveUser)):
    return currentUser


# POST Methods
@app.post("/login/")
async def loginUser(formData: OAuth2PasswordRequestForm = Depends()):
    # Checking username
    userDict = users_db.get(formData.username)

    if not userDict:
        raise HTTPException(
            status_code=400,
            detail="Login Invalid"
        )

    # Checking password
    user = UserSaveDB(**userDict)
    hash_password = pwdHasher(formData.password)

    if not hash_password == user.hashPassword:
        raise HTTPException(
            status_code=400,
            detail="Infos Uncorrected"
        )

    # Return Token
    return {"accessToken": user.username, "tokenType": "bearer"}
