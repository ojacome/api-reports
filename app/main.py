from fastapi import FastAPI
from presentation.routes import router as api_router
from presentation.ws_routes import ws_router
from infrastructure.db import Base, engine, seed_initial_data
from usage.infrastructure import models_usage as usage_models

app = FastAPI(title="TelcoX Self-Service API", version="2.0.0 (DNI-based)")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)      
    seed_initial_data()                         
    usage_models.UsageBase.metadata.create_all(bind=engine)

# REST
app.include_router(api_router, prefix="/api")
# WebSockets
app.include_router(ws_router)
