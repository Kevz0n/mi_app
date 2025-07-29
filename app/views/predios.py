# app/views/predios.py

from fastapi import APIRouter, Request, Depends, Form, HTTPException
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


# 1) Vista HTML lista de predios
@router.get("/html", response_class=HTMLResponse)
def list_predios_html(request: Request, db: Session = Depends(get_db)):
    predios = crud.get_predios(db)
    return templates.TemplateResponse(
        "predios_list.html",
        {"request": request, "predios": predios}
    )


# 2) Formulario HTML para crear/editar predio
@router.get("/form", response_class=HTMLResponse)
def form_predio(request: Request, id: int = None, db: Session = Depends(get_db)):
    predio = crud.get_predio(db, id) if id else None
    propietarios = crud.get_propietarios(db)
    return templates.TemplateResponse(
        "predios_form.html",
        {"request": request, "predio": predio, "propietarios": propietarios}
    )


# 3) Guardar (crear o actualizar) predio
@router.post("/save")
def save_predio(
    nombre: str = Form(...),
    tipo: schemas.TipoPredio = Form(...),
    numero_catastral: str = Form(...),
    propietarios_ids: list[int] = Form([]),
    id: int = Form(None),
    db: Session = Depends(get_db)
):
    datos = schemas.PredioCreate(
        nombre=nombre,
        tipo=tipo,
        numero_catastral=numero_catastral,
        propietarios_ids=propietarios_ids
    )
    if id:
        crud.update_predio(db, id, datos)
    else:
        crud.create_predio(db, datos)
    return RedirectResponse(url="/predios/html", status_code=303)


# 4) Eliminar predio
@router.get("/delete/{id}")
def delete_predio(id: int, db: Session = Depends(get_db)):
    crud.delete_predio(db, id)
    return RedirectResponse(url="/predios/html", status_code=303)


# 5) API JSON: listado de predios con URLs absolutas
@router.get(
    "/",
    response_model=list[schemas.PredioOut],
    response_model_exclude_none=True
)
def list_predios_api(request: Request, db: Session = Depends(get_db)):
    preds = crud.get_predios(db)
    salida: list[schemas.PredioOut] = []
    for p in preds:
        link = str(request.url_for("get_predio", predio_id=p.id))
        data = schemas.Predio.from_orm(p).model_dump()
        data["url"] = link
        salida.append(schemas.PredioOut.model_validate(data))
    return salida


# 6) API JSON: detalle de un predio con URL absoluta
@router.get(
    "/{predio_id}",
    response_model=schemas.PredioOut,
    name="get_predio",
    response_model_exclude_none=True
)
def get_predio_endpoint(
    predio_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    p = crud.get_predio(db, predio_id)
    if not p:
        raise HTTPException(status_code=404, detail="Predio no encontrado")

    link = str(request.url_for("get_predio", predio_id=p.id))
    predio_dict = schemas.Predio.from_orm(p).model_dump()
    predio_dict["url"] = link
    return schemas.PredioOut.model_validate(predio_dict)

