from pydantic import BaseModel, constr, HttpUrl
from typing import List
import enum

# --- Enums ---

class TipoPredio(str, enum.Enum):
    Urbano = "Urbano"
    Rural  = "Rural"

class TipoPersona(str, enum.Enum):
    Natural = "Natural"
    Juridica = "Jurídica"

class TipoIdentificacion(str, enum.Enum):
    CC = "Cédula de ciudadanía"
    CE = "Cédula de extranjería"
    NIT = "Número de identificación tributaria"
    TI = "Tarjeta de identidad"

# --- Propietario Schemas ---

class PropietarioBase(BaseModel):
    nombre: str
    tipo_persona: TipoPersona
    numero_identificacion: constr(min_length=1)
    tipo_identificacion: TipoIdentificacion

class PropietarioCreate(PropietarioBase):
    pass

class Propietario(PropietarioBase):
    id: int

    class Config:
        from_attributes = True

# --- Predio Schemas ---

class PredioBase(BaseModel):
    nombre: str
    tipo: TipoPredio
    numero_catastral: constr(min_length=30, max_length=30)
    propietarios_ids: List[int] = []

class PredioCreate(PredioBase):
    pass

class Predio(PredioBase):
    id: int
    propietarios: List[Propietario] = []

    class Config:
        from_attributes = True

# --- Output Schema con URL absoluta ---

class PredioOut(Predio):
    url: HttpUrl

    class Config:
        from_attributes = True

