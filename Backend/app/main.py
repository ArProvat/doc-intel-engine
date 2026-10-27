from fastapi import FastAPI, HTTPException
from psycopg import AsyncConnection, OperationalError

from app.config import settings

app = FastAPI(title="Document Intelligence API")


@app.get("/health/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def ready() -> dict[str, str]:
    try:
        async with await AsyncConnection.connect(
            host=settings.postgres_host,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password.get_secret_value(),
            connect_timeout=3,
        ) as connection:
            await connection.execute("SELECT 1")
    except OperationalError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"status": "ok"}
