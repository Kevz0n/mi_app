# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

# ---------------- Predios CRUD ----------------

def get_predios(db: Session):
    return db.query(models.Predio).all()

def get_predio(db: Session, predio_id: int):
    return db.query(models.Predio).filter(models.Predio.id == predio_id).first()

def create_predio(db: Session, predio: schemas.PredioCreate):
    db_predio = models.Predio(
        nombre=predio.nombre,
        tipo=predio.tipo,
        numero_catastral=predio.numero_catastral
    )
    # Asociar propietarios
    for pid in predio.propietarios_ids:
        p = db.get(models.Propietario, pid)
        if p:
            db_predio.propietarios.append(p)
    db.add(db_predio)
    db.commit()
    db.refresh(db_predio)
    return db_predio

def update_predio(db: Session, predio_id: int, datos: schemas.PredioCreate):
    db_predio = get_predio(db, predio_id)
    if not db_predio:
        return None
    # Actualizar campos
    db_predio.nombre = datos.nombre
    db_predio.tipo = datos.tipo
    db_predio.numero_catastral = datos.numero_catastral
    # Resetear propietarios
    db_predio.propietarios.clear()
    for pid in datos.propietarios_ids:
        p = db.get(models.Propietario, pid)
        if p:
            db_predio.propietarios.append(p)
    db.commit()
    db.refresh(db_predio)
    return db_predio

def delete_predio(db: Session, predio_id: int):
    db_predio = get_predio(db, predio_id)
    if db_predio:
        db.delete(db_predio)
        db.commit()
    return db_predio

# -------------- Propietarios CRUD --------------

def get_propietarios(db: Session):
    return db.query(models.Propietario).all()

def get_propietario(db: Session, propietario_id: int):
    return db.get(models.Propietario, propietario_id)

def create_propietario(db: Session, propietario: schemas.PropietarioCreate):
    db_prop = models.Propietario(**propietario.dict())
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

def update_propietario(db: Session, propietario_id: int, datos: schemas.PropietarioCreate):
    db_prop = get_propietario(db, propietario_id)
    if not db_prop:
        return None
    db_prop.nombre = datos.nombre
    db_prop.tipo_persona = datos.tipo_persona
    db_prop.numero_identificacion = datos.numero_identificacion
    db_prop.tipo_identificacion = datos.tipo_identificacion
    db.commit()
    db.refresh(db_prop)
    return db_prop

def delete_propietario(db: Session, propietario_id: int):
    db_prop = get_propietario(db, propietario_id)
    if db_prop:
        db.delete(db_prop)
        db.commit()
    return db_prop

