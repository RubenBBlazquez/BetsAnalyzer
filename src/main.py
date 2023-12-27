from fastapi import FastAPI
from starlette.config import Config

config = Config('config/.env')
app = FastAPI()
