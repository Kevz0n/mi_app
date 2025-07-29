from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Tabla intermedia many-to-many entre Predio y Propietario
predio_propietario = Table(
    "predio_propietario", Base.metadata,
    Column("predio_id", Integer, ForeignKey("predios.id"), primary_key=True),
    Column("propietario_id", Integer, ForeignKey("propietarios.id"), primary_key=True),
)

class Predio(Base):
    __tablename__ = "predios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    # Se usa String en lugar de Enum para permitir valores en cualquier case
    tipo = Column(String, nullable=False)
    numero_catastral = Column(String(30), unique=True, index=True, nullable=False)

    # Relación many-to-many con Propietario
    propietarios = relationship(
        "Propietario",
        secondary=predio_propietario,
        back_populates="predios"
    )

class Propietario(Base):
    __tablename__ = "propietarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo_persona = Column(String, nullable=False)
    numero_identificacion = Column(String, unique=True, index=True, nullable=False)
    tipo_identificacion = Column(String, nullable=False)

    # Relación many-to-many con Predio
    predios = relationship(
        "Predio",
        secondary=predio_propietario,
        back_populates="propietarios"
    )