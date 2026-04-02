from fastapi import FastAPI
try:
    from .routers.user import router
    from .database import engine
    from .models.user import Base
except:
    from routers.user import router
    from database import engine, Base

Base.metadata.create_all(bind=engine)


model_tags = [
    {"name": "Users"},
    {"name": "Sistem"}
]

app = FastAPI(title="API_1.0.0",
              openapi_tags=model_tags)

app.include_router(router, prefix="/router", tags=["Users"])


@app.head("", tags=["Sistem"])
def get_health():
    return
