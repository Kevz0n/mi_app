# app/views/propietarios.py

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def list_propietarios(request: Request, db: Session = Depends(get_db)):
    propietarios = crud.get_propietarios(db)
    return templates.TemplateResponse(
        "propietarios_list.html",
        {"request": request, "propietarios": propietarios}
    )

@router.get("/form", response_class=HTMLResponse)
def form_propietario(request: Request, id: int = None, db: Session = Depends(get_db)):
    propietario = crud.get_propietario(db, id) if id else None
    return templates.TemplateResponse(
        "propietario_form.html",
        {"request": request, "propietario": propietario}
    )

@router.post("/save")
def save_propietario(
    nombre: str = Form(...),
    tipo_persona: schemas.TipoPersona = Form(...),
    numero_identificacion: str = Form(...),
    tipo_identificacion: schemas.TipoIdentificacion = Form(...),
    id: int = Form(None),
    db: Session = Depends(get_db)
):
    datos = schemas.PropietarioCreate(
        nombre=nombre,
        tipo_persona=tipo_persona,
        numero_identificacion=numero_identificacion,
        tipo_identificacion=tipo_identificacion
    )
    if id:
        crud.update_propietario(db, id, datos)
    else:
        crud.create_propietario(db, datos)
    return RedirectResponse(url="/propietarios/", status_code=303)

@router.get("/delete/{id}")
def delete_propietario(id: int, db: Session = Depends(get_db)):
    crud.delete_propietario(db, id)
    return RedirectResponse(url="/propietarios/", status_code=303)
