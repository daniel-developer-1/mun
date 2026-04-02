from fastapi import FastAPI
from .routers.user import router

model_tags = [
    {"name": "Users"},
    {"name": "Sistem"}
]

app = FastAPI(title="API_1.0.0",
              openapi_tags=model_tags)

app.include_router(router, prefix="/router")


@app.get("/", tags=["Users"])
def get_root():
    return {"Message": "Welcome to my API"}


@app.head("", tags=["Sistem"])
def get_health():
    return
