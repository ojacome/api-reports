from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.routes import router as api_router
from presentation.ws_routes import ws_router
from infrastructure.db import Base, engine, seed_initial_data
from usage.infrastructure import models_usage as usage_models
from presentation.routes_dev import dev_router

app = FastAPI(title="TelcoX Self-Service API", version="1.0.0 (DNI-based)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)      
    seed_initial_data()                         
    usage_models.UsageBase.metadata.create_all(bind=engine)

# REST
app.include_router(api_router, prefix="/api")
app.include_router(dev_router)

# WebSockets
app.include_router(ws_router)
