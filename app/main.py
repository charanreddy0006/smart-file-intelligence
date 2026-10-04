from fastapi import FastAPI
from app.api.routes import router
from app.core.database import init_db

app = FastAPI(
    title="Smart File Intelligence",
    version="1.0.0",
    description="Intelligent file classification, duplicate detection and semantic-style search.",
)

app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()
