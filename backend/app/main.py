import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import Base, engine
from app.models import Product, User  # noqa: F401 (registers tables)
from app.api.products import router as product_router
from app.api import auth
from app.api.dashboard import router as dashboard_router
from app.api.prediction import router as prediction_router
from app.api.forecast import router as forecast_router
from app.api.competitor import router as competitor_router
from app.api.profitability import router as profitability_router
from app.api.pricing_strategy import router as pricing_strategy_router
from app.api.executive_report import router as executive_report_router

app = FastAPI(
    title="PricePilot AI",
    description="Dynamic Pricing Optimization & Revenue Intelligence System",
    version="1.0.0"
)

# Allowed frontend URLs come from the FRONTEND_URLS env variable (comma-separated)
# e.g. FRONTEND_URLS=http://localhost:5173,https://pricepilot-ai.vercel.app
origins = [
    url.strip().rstrip("/")
    for url in os.getenv(
        "FRONTEND_URLS", "http://localhost:5173,http://localhost:5174"
    ).split(",")
    if url.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Vercel preview URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    # Don't crash the server if the DB is unreachable; /test-db shows the error.
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables ready")
    except Exception as e:
        print(f"❌ Could not create tables: {e}")


app.include_router(product_router)
app.include_router(auth.router)
app.include_router(dashboard_router)
app.include_router(prediction_router)
app.include_router(forecast_router)
app.include_router(competitor_router)
app.include_router(profitability_router)
app.include_router(
    pricing_strategy_router
)
app.include_router(
    executive_report_router
)
@app.get("/")
def home():
    return {
        "message": "Backend is running successfully🚀"
    }

@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            version = connection.execute(text("SELECT VERSION()")).scalar()
        return {"message": "Database connected successfully ✅", "version": version}
    except Exception as e:
        return {"error": str(e)}