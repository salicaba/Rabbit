from abc import ABC, abstractmethod
from typing import List
from domain.models import Acceso

class AccesoRepository(ABC):
    @abstractmethod
    def save(self, acceso: Acceso) -> Acceso:
        pass

    @abstractmethod
    def get_all(self) -> List[Acceso]:
        pass

class LogPublisher(ABC):
    @abstractmethod
    async def publish_log(self, message: str):
        pass