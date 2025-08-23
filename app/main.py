from fastapi import FastAPI
from presentation.routes import router as api_router
from infrastructure.db import Base, engine, seed_initial_data

app = FastAPI(title="TelcoX Self-Service API", version="2.0.0 (DNI-based)")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_initial_data()

app.include_router(api_router, prefix="/api")
