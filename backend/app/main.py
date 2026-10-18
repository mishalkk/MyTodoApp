from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine


app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Page to health check Database Connections
@app.get("/health/db")
def db_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(
            status_code = 503,
            detail      = "Database Unavailable",
        ) from None

    return {"status": "ok"}

