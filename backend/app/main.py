import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .database import engine, Base, SessionLocal
from .routers.prediction import router as prediction_router
from .routers.shopping import router as shopping_router
from . import crud

load_dotenv()

Base.metadata.create_all(bind=engine)
with SessionLocal() as seed_db:
    crud.seed_products(seed_db)

app = FastAPI(
    title="Cart Rescue AI",
    description="Predict cart abandonment and provide insights for recovery.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(prediction_router, prefix="/api")
app.include_router(shopping_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Cart Rescue AI backend is running."}
