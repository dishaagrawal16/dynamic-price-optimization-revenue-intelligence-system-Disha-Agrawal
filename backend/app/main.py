from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models.product import Product
from app.api.products import router as product_router
from app.api import auth
from app.api.dashboard import router as dashboard_router
# Create tables

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PricePilot AI",
    description="Dynamic Pricing Optimization & Revenue Intelligence System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product_router)
app.include_router(auth.router)
app.include_router(dashboard_router)
@app.get("/")
def home():
    return {
        "message": "Backend is running successfully🚀"
    }

@app.get("/test-db")
def test_db():
    try:
        connection = engine.connect()
        connection.close()
        return {"message": "Database connected successfully ✅"}
    except Exception as e:
        return {"error": str(e)}