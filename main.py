from fastapi import FastAPI
from backend import *
from backend.checkAPI import resultResponse
from backend.templates.base import base

app = FastAPI()


@app.get("/")
async def hello():
    return resultResponse()


# called the function settings
if __name__ == "__main__":
    get_api_settings()
    base()
