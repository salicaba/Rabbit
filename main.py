from fastapi import FastAPI
from domain.models import Acceso, AccesoCreate
from application.use_cases import AccesoService
from infrastructure.mysql_adapter import MySQLAccesoRepository
from infrastructure.rabbitmq_adapter import RabbitMQPublisher
from typing import List

app = FastAPI(title="API de Control de Accesos - Hexagonal")

repository = MySQLAccesoRepository(host="localhost", user="root", password="", database="empresa_db")
publisher = RabbitMQPublisher()
acceso_service = AccesoService(repository, publisher)

# POST: Recibe datos sin ID (AccesoCreate), pero responde con el ID generado (Acceso)
@app.post("/accesos/", response_model=Acceso)
async def registrar_acceso(acceso: AccesoCreate):
    return await acceso_service.registrar_acceso(acceso)

# GET: Devuelve toda la lista con sus IDs
@app.get("/accesos/", response_model=List[Acceso])
def obtener_accesos():
    return acceso_service.obtener_accesos()