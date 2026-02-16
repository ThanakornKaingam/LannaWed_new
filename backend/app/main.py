from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.config import settings
from app.routers.predict_router import router as predict_router
from app.routers.auth_router import router as auth_router

# =========================
# Create App
# =========================
app = FastAPI(
    title="Flower Veg Enterprise API",
    docs_url="/docs",
    redoc_url=None
)
# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-zaax.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# =========================
# Create Database Tables
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# Routers
# =========================
app.include_router(predict_router)
app.include_router(auth_router)

# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {"status": "API Running"}
    
@app.get("/ping")
def ping():
    return {"pong": True}
