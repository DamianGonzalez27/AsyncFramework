
from pydantic import BaseModel

class BaseModelRequest(BaseModel):

    __db_exclude__: set[str] = set()
    
    def to_db(self) -> dict:
        """
        Convierte el modelo a tipos primitivos
        seguros para ORM / DB drivers.
        """
        return self.model_dump(
            mode="json", 
            exclude=self.__db_exclude__
        )