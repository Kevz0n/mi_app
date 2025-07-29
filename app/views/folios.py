# app/views/folios.py

import os
import shutil
import json
import re

from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "folios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Patrón para capturar opcionalmente un '>' antes de ESPECIFICACION:
ESPEC_PATTERN = re.compile(r">?ESPECIFICACION:\s*(\d{3,5})", re.IGNORECASE)

def scan_especificaciones() -> dict[str, list[str]]:
    resultados: dict[str, list[str]] = {}
    for fname in sorted(os.listdir(UPLOAD_DIR)):
        if not fname.lower().endswith(".json"):
            continue
        codes: list[str] = []
        try:
            with open(os.path.join(UPLOAD_DIR, fname), encoding="utf-8") as f:
                data = json.load(f)
            texto = data.get("textoAnotaciones", "")
            if isinstance(texto, list):
                for entry in texto:
                    codes += ESPEC_PATTERN.findall(entry)
            else:
                codes = ESPEC_PATTERN.findall(texto)
        except Exception:
            codes = []
        resultados[fname] = codes
    return resultados

@router.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    archivos = sorted(os.listdir(UPLOAD_DIR))
    return templates.TemplateResponse(
        "folios_upload.html",
        {
            "request": request,
            "archivos": archivos,
            "guardados": [],
            "errores": [],
            "especificaciones": None,
        }
    )

@router.post("/upload", response_class=HTMLResponse)
async def upload_files(
    request: Request,
    files: list[UploadFile] = File([])
):
    errores, guardados = [], []
    if not files:
        errores.append("No enviaste ningún archivo.")
    else:
        for file in files:
            fn = file.filename or "<sin nombre>"
            if not fn.lower().endswith(".json"):
                errores.append(f"'{fn}' no es un .json válido")
                continue
            dest = os.path.join(UPLOAD_DIR, fn)
            try:
                with open(dest, "wb") as buf:
                    shutil.copyfileobj(file.file, buf)
                guardados.append(fn)
            except Exception as e:
                errores.append(f"Error guardando '{fn}': {e}")

    archivos = sorted(os.listdir(UPLOAD_DIR))
    return templates.TemplateResponse(
        "folios_upload.html",
        {
            "request": request,
            "archivos": archivos,
            "guardados": guardados,
            "errores": errores,
            "especificaciones": None,
        }
    )

@router.post("/extract", response_class=HTMLResponse)
def extract_codes(
    request: Request,
    extract: str = Form(...)   # coincide con <input name="extract">
):
    archivos = sorted(os.listdir(UPLOAD_DIR))
    especificaciones = scan_especificaciones()
    return templates.TemplateResponse(
        "folios_upload.html",
        {
            "request": request,
            "archivos": archivos,
            "guardados": [],
            "errores": [],
            "especificaciones": especificaciones,
        }
    )

@router.get("/download/{fname}")
def download_file(fname: str):
    """
    Sirve el JSON con Content-Disposition:inline para que el navegador lo muestre
    en lugar de descargarlo.
    """
    path = os.path.join(UPLOAD_DIR, fname)
    if not os.path.isfile(path):
        raise HTTPException(404, f"El archivo '{fname}' no existe.")
    return FileResponse(
        path,
        media_type="application/json",
        headers={
            "Content-Disposition": f"inline; filename={fname}"
        }
    )

@router.get("/delete/{fname}", response_class=HTMLResponse)
def delete_file(request: Request, fname: str):
    path = os.path.join(UPLOAD_DIR, fname)
    errores: list[str]
    if os.path.exists(path) and os.path.isfile(path):
        try:
            os.remove(path)
            errores = []
        except Exception as e:
            errores = [f"No se pudo borrar '{fname}': {e}"]
    else:
        errores = [f"El archivo '{fname}' no existe."]
    archivos = sorted(os.listdir(UPLOAD_DIR))
    return templates.TemplateResponse(
        "folios_upload.html",
        {
            "request": request,
            "archivos": archivos,
            "guardados": [],
            "errores": errores,
            "especificaciones": None,
        }
    )
