from pydantic import BaseModel
from typing import Optional

class AccesoCreate(BaseModel):
    empleado: str
    area: str
    hora: str

class Acceso(AccesoCreate):
    id: Optional[int] = None