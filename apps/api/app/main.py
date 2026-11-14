"""API du patrimoine de test."""
from fastapi import FastAPI

from . import models  # noqa: F401
from .database import Base, engine
from .routers import campagnes, cas_de_test, projets

app = FastAPI(title="Gestion du patrimoine de test", version="0.1.0")

app.include_router(projets.router, prefix="/api")
app.include_router(cas_de_test.router, prefix="/api")
app.include_router(campagnes.router, prefix="/api")


@app.on_event("startup")
def init_db():
    # En production, préférez des migrations (ex. Alembic).
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok"}
