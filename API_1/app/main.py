from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.database import engine
from app.models.user import Base
import os
from datetime import datetime
from typing import Dict

# Crear tablas
Base.metadata.create_all(bind=engine)

# Configuración de API Keys
# En Render, configura la variable de entorno VALID_API_KEYS con las keys separadas por coma
# Ejemplo: "free_key_123,pro_key_456,enterprise_key_789"
VALID_API_KEYS = os.getenv("VALID_API_KEYS", "").split(",")

# Para tracking de uso (en memoria - se reinicia si el servidor se cae)
# En producción, usa una base de datos
usage_data: Dict[str, Dict[str, int]] = {}

# Límites por plan (requests por mes)
PLAN_LIMITS = {
    "free": 1000,
    "basic": 10000,
    "pro": 50000,
    "enterprise": 500000
}

# Endpoints públicos (no requieren API Key)
PUBLIC_PATHS = [
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/router/create_user",
    "/auth/token",
    "/auth/login",
    "/auth/verify-token"
]

model_tags = [
    {"name": "Users"},
    {"name": "Authentication"},
    {"name": "System"}
]

app = FastAPI(
    title="API_1.0.0 with JWT Auth",
    description="API completa de autenticación y gestión de usuarios con JWT. Lista para monetizar.",
    version="1.0.0",
    openapi_tags=model_tags
)

# Configurar CORS (permite que cualquier frontend use tu API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_plan_from_api_key(api_key: str) -> str:
    """Determina el plan según la API Key (personalizable)"""
    # Puedes personalizar según prefijos o usar una base de datos
    if api_key.startswith("free_"):
        return "free"
    elif api_key.startswith("basic_"):
        return "basic"
    elif api_key.startswith("pro_"):
        return "pro"
    elif api_key.startswith("enterprise_"):
        return "enterprise"
    else:
        return "free"  # Por defecto


def check_usage_limit(api_key: str) -> bool:
    """Verifica si el API Key ha excedido su límite mensual"""
    current_month = datetime.now().strftime("%Y-%m")
    plan = get_plan_from_api_key(api_key)
    limit = PLAN_LIMITS.get(plan, 1000)

    # Inicializar si no existe
    if api_key not in usage_data:
        usage_data[api_key] = {}

    # Resetear si es un nuevo mes
    if current_month not in usage_data[api_key]:
        usage_data[api_key][current_month] = 0

    usage = usage_data[api_key][current_month]

    if usage >= limit:
        return False

    # Incrementar contador
    usage_data[api_key][current_month] += 1
    return True


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    """Middleware que valida API Key en todos los endpoints protegidos"""
    path = request.url.path

    # Verificar si es un endpoint público
    is_public = any(path.startswith(public_path)
                    for public_path in PUBLIC_PATHS)

    if is_public:
        return await call_next(request)

    # Obtener API Key del header
    api_key = request.headers.get(
        "x-api-key") or request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key required. Please include 'x-api-key' header in your request."
        )

    # Validar que la API Key sea válida
    if api_key not in VALID_API_KEYS and VALID_API_KEYS != ['']:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Please subscribe to get a valid key."
        )

    # Verificar límite de uso mensual
    if not check_usage_limit(api_key):
        plan = get_plan_from_api_key(api_key)
        limit = PLAN_LIMITS.get(plan, 1000)
        raise HTTPException(
            status_code=429,
            detail=f"Monthly limit exceeded ({limit} requests). Please upgrade your plan."
        )

    # Agregar info de la API Key al request state para usarla en endpoints si es necesario
    request.state.api_key = api_key
    request.state.plan = get_plan_from_api_key(api_key)

    return await call_next(request)

# Incluir routers
app.include_router(user_router, prefix="/router")
app.include_router(auth_router)


@app.get("/usage")
async def get_usage(request: Request):
    """Endpoint para consultar el uso actual de tu API Key"""
    api_key = request.headers.get(
        "x-api-key") or request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(status_code=401, detail="API Key required")

    current_month = datetime.now().strftime("%Y-%m")
    plan = get_plan_from_api_key(api_key)
    limit = PLAN_LIMITS.get(plan, 1000)
    usage = usage_data.get(api_key, {}).get(current_month, 0)

    return {
        "api_key": api_key[:8] + "..." if len(api_key) > 8 else api_key,
        "plan": plan,
        "usage_this_month": usage,
        "monthly_limit": limit,
        "remaining": limit - usage,
        "reset_date": f"{datetime.now().year}-{datetime.now().month + 1 if datetime.now().month < 12 else 1}-01"
    }


@app.head("/", tags=["System"])
def get_health():
    return


@app.get("/", tags=["System"])
def get_root():
    return {
        "message": "Welcome to JWT Authentication API",
        "docs": "/docs",
        "status": "operational",
        "version": "1.0.0"
    }
