from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import init_db
from routes.string_analyzer import router as string_router
from routes.filters import router as filter_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="String Analyzer API", lifespan=lifespan)

app.include_router(filter_router, prefix="/strings", tags=["filters"])
app.include_router(string_router, prefix="/strings", tags=["strings"])
