from fastapi import FastAPI
from common.base_testing import create_tables, initialize_db, start_dependencies
from infrastructure.database import engine

app = FastAPI()


@app.on_event("startup")
async def start_app() -> None:
    await create_tables()
    await initialize_db()
    start_dependencies()


@app.on_event("shutdown")
async def shutdown_app() -> None:
    await engine.dispose()
