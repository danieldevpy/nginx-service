from typing import Protocol, List, Union
from ..model.server import ServerDTO, Server


class ServerRepository(Protocol):

    def get_all(self) -> List[ServerDTO]:
        ...

    def get_by_id(self, id: int) -> Union[ServerDTO, None]:
        ...

    def create(self, server: Server) -> ServerDTO:
        ...
        
    def update(self, id: int, server: Server) -> ServerDTO:
        ...

    def delete(self, id: int) -> bool:
        ...