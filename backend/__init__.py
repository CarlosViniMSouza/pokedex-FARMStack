from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from functools import lru_cache
from typing import List
from pydantic import BaseSettings

app = FastAPI()

# localhost:3000 (ReactJS)
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class APISettings(BaseSettings):
    api_v2_route: str = "/api/v2"
    openapi_route: str = "https://pokeapi.co/api/v2/pokemon/"
    backend_cors_origins_str: str = ""  # Should be a comma-separated list of origins

    debug: bool = False
    debug_exceptions: bool = False
    include_admin_routes: bool = False
    disable_superuser_dependency: bool = False

    @property
    def backend_cors_origins(self) -> List[str]:
        return [x.strip() for x in self.backend_cors_origins_str.split(",") if x]

    class Config:
        env_prefix = ""


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()  # reads variables from environment
