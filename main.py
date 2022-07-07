from fastapi import FastAPI
from backend import *

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello, FastAPI"}

# called the function settings
if __name__ == "__main__":
    app
    get_api_settings()