# Gestor de Predios, Propietarios y Folios JSON

Una aplicación web construida con **FastAPI**, **SQLAlchemy** y **Jinja2** que permite:
- CRUD de predios y propietarios.
- Gestión de “folios” (archivos JSON), con subida múltiple, visualización, eliminación.
- Extracción automática de códigos de “ESPECIFICACION” mediante regex.

---

## 📁 Estructura de carpetas-dale a editar para ver la estructura como debe ser

mi_app/
├── app/
│ ├── crud.py
│ ├── database.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── static/
│ │ ├── style.css
│ │ └── json-file.png
│ ├── templates/
│ │ ├── base.html
│ │ ├── predios_list.html
│ │ ├── predios_form.html
│ │ ├── propietarios_list.html
│ │ ├── propietario_form.html
│ │ └── folios_upload.html
│ └── views/
│ ├── predios.py
│ ├── propietarios.py
│ └── folios.py
├── folios/ ← Carpeta donde se guardan los JSON subidos
├── requirements.txt
└── README.md

---

## 🚀 Prerrequisitos

- **Python 3.10+**  
- Una base de datos **PostgreSQL** (o ajusta `DATABASE_URL` en `app/database.py` a tu motor preferido).

---

## ⚙️ Instalación

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/Kevz0n/mi_app.git
   cd mi_app

   Crea y activa un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

Instala las dependencias
pip install --upgrade pip
pip install -r requirements.txt



Configura la conexión a la base de datos
DATABASE_URL = "postgresql://usuario:password@localhost:5432/mi_base"
usuario:alexroel
password:123456

 Ejecutar la aplicación
 uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload


