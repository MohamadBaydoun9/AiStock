from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.db.mongo import mongo_db
from app.api import routes_auth, routes_products, routes_stats, routes_ml_stub, routes_product_types, routes_price, routes_train

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Events
@app.on_event("startup")
async def startup_db_client():
    await mongo_db.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await mongo_db.close_mongo_connection()

# Routes
app.include_router(routes_auth.router, prefix="/auth", tags=["auth"])
app.include_router(routes_products.router, prefix="/products", tags=["products"])
app.include_router(routes_stats.router, prefix="/stats", tags=["stats"])
app.include_router(routes_ml_stub.router, prefix="/ml", tags=["ml"])
app.include_router(routes_product_types.router, prefix="/product-types", tags=["product-types"])
app.include_router(routes_price.router, prefix="/ml", tags=["price-prediction"])
app.include_router(routes_train.router, prefix="/train", tags=["training"])


@app.get("/")
async def root():
    return {"message": "SmartStock AI Backend is running"}
