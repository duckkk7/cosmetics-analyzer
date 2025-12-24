from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="Cosmetics Analyzer API",
    description="API для анализа состава косметики",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Cosmetics Analyzer API is running! Use /api/analyze"}
