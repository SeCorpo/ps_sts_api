from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.core.session import connect_to_redis, close_redis_connection
from src.core.database import test_connection
# from src.core.database import setup_schema


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await connect_to_redis()
    await test_connection()
    # await setup_schema()
    yield
    await close_redis_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
