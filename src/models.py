from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass(frozen=True)
class LecturaPropiedad:
    """DTO que representa una fila procesada del XML."""
    archivo_origen: str
    cod_comunidad: str
    nombre_comunidad: str
    propiedad_codigo: str
    propiedad_nombre: str
    propietario: str
    lectura_ant: int
    lectura_act: int
    consumo: int
    importe_total: str  # Mantenemos str para preservar el formato "36,55"
