# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from .database import engine, Base
from .views.predios import router as predios_router
from .views.propietarios import router as propietarios_router
from .views.folios import router as folios_router

# (Re)crea tablas si es necesario
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestor de Predios, Propietarios y Folios")

# Carpeta de estáticos (CSS, imágenes, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(
    predios_router,
    prefix="/predios",
    tags=["Predios"]
)
app.include_router(
    propietarios_router,
    prefix="/propietarios",
    tags=["Propietarios"]
)
app.include_router(
    folios_router,
    prefix="/folios",
    tags=["Folios"]
)

# Redirige la raíz "/" a la vista HTML de predios
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/predios/html")



