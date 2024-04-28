from fastapi import FastAPI

from app.entities.collections import set_indexes

app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    await set_indexes()
