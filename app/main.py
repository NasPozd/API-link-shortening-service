from fastapi import FastAPI
from app.core.config import LOGGING_LEVEL, DATABASE_URL
import logging

logging.basicConfig(level=LOGGING_LEVEL)
from .routers import links, users, stats
from .db.database import init_db

init_db()

app = FastAPI()

logging.info("Application startup initiated.")

app.include_router(links.router)
app.include_router(users.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API Link Shortening Service!"}
