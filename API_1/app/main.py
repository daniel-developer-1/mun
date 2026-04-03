from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.database import engine
from app.models.user import Base

# Crear tablas
Base.metadata.create_all(bind=engine)

model_tags = [
    {"name": "Users"},
    {"name": "Authentication"},
    {"name": "System"}
]

app = FastAPI(
    title="API_1.0.0 with JWT Auth",
    openapi_tags=model_tags
)

# Incluir routers
app.include_router(user_router, prefix="/router")
app.include_router(auth_router)


@app.head("/", tags=["System"])
def get_health():
    return
