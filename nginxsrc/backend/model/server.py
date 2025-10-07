from .. import Server


class ServerDTO(Server):
    id: int

    def no_id(self):
        data = self.model_dump()
        del data["id"]
        return Server(**data)