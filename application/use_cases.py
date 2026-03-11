from domain.models import Acceso, AccesoCreate
from domain.ports import AccesoRepository, LogPublisher
from typing import List

class AccesoService:
    def __init__(self, repository: AccesoRepository, publisher: LogPublisher):
        self.repository = repository
        self.publisher = publisher

    # Nota que aquí recibimos AccesoCreate (sin ID)
    async def registrar_acceso(self, datos_acceso: AccesoCreate) -> Acceso:
        # 1. Convertimos los datos de entrada a la Entidad Acceso (con id = None)
        acceso = Acceso(**datos_acceso.model_dump())
        
        # 2. Guardar en Base de Datos (MySQL le generará su ID autoincrementable)
        acceso_guardado = self.repository.save(acceso)
        
        # 3. Procesamiento asíncrono: Publicar evento en RabbitMQ
        mensaje_log = f"[{acceso_guardado.hora}] SEGURIDAD: Ingreso de {acceso_guardado.empleado} al área de {acceso_guardado.area}."
        await self.publisher.publish_log(mensaje_log)
        
        return acceso_guardado

    def obtener_accesos(self) -> List[Acceso]:
        return self.repository.get_all()