import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Solo importar los routers de MongoDB que necesitas
from app.routers import menu_mongo, auth_mongo, images
from app.routers import secciones_imagenes

app = FastAPI(
    title="Restaurante API",
    description="API para el sistema de gestión del restaurante",
    version="1.0.0"
)

# Configurar CORS para desarrollo y producción
allowed_origins = [
    "http://localhost:5173", 
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]

# Agregar dominios de producción si están definidos
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

# Para desarrollo, permitir todos los orígenes si está en modo DEBUG
if os.getenv("DEBUG", "False").lower() == "true":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir solo routers de MongoDB para producción
app.include_router(auth_mongo.router, prefix="/api/auth", tags=["Autenticación MongoDB"])
app.include_router(menu_mongo.router, prefix="/api/menu", tags=["Menú MongoDB"])
app.include_router(images.router, prefix="/api", tags=["Imágenes Públicas"])
app.include_router(secciones_imagenes.router, tags=["Secciones de Imágenes"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Restaurante"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}