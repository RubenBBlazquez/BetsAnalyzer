from dotenv import load_dotenv
from fastapi import FastAPI

from src.sport_monks_client.router import router

load_dotenv(dotenv_path="config/.env")

app = FastAPI()
app.include_router(router)
