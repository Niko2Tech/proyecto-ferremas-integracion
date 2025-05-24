from fastapi import FastAPI, APIRouter
from app.db.database import Base, engine
from fastapi.staticfiles import StaticFiles
from app.api import clientes, productos, upload_data, webpay, ventas, utils
from fastapi.middleware.cors import CORSMiddleware


# Crea el router general con prefijo /api
api_router = APIRouter(prefix="/api")

# Incluye tus routers en el router principal
api_router.include_router(clientes.router)
api_router.include_router(productos.router)
api_router.include_router(upload_data.router)
api_router.include_router(webpay.router)
api_router.include_router(ventas.router)
api_router.include_router(utils.router)

app = FastAPI()
# CORS
origins = [
    "http://localhost:5173",
    "localhost"
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Crear la base de datos
Base.metadata.create_all(bind=engine)

# Montar el directorio de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)