from fastapi import FastAPI
from .routes import userRoute

app = FastAPI()

app.include_router(userRoute.router)