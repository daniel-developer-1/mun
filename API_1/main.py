from fastapi import FastAPI

model_tags = [
    {"name": "Users"},
    {"name": "Sistem"}
]

app = FastAPI(title="API_1.0.0",
              openapi_tags=model_tags)


@app.get("/", tags=["Users"])
def get_root():
    return {"Message": "Welcome to my API"}


@app.head("", tags=["Sistem"])
def get_health():
    return
