from models.item import ItemDocument
from models.user import User
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from decouple import config

from routers import items, auth

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(items.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def app_init():
    """Initialize application services"""
    client = AsyncIOMotorClient(config('MONGO_URI'))
    await init_beanie(client.db_name, document_models=[ItemDocument, User])
