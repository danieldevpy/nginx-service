from typing import Dict, Set
from threading import Lock


class InMemoryNginxRepository:
    """
    Implementação em memória do NginxRepository.
    Simula operações de gerenciamento de servidores Nginx sem interagir com o sistema real.
    """

    def __init__(self):
        self._storage: Dict[str, str] = {}       # Map: server_name -> config
        self._enabled: Set[str] = set()          # Servidores "ativos" (simulação do sites-enabled)
        self._lock = Lock()                      # Para thread-safety

    def server_exists(self, server_name: str) -> bool:
        return server_name in self._storage

    def get_server_config(self, server_name: str) -> str:
        if not self.server_exists(server_name):
            raise ValueError(f"Server '{server_name}' does not exist")
        return self._storage[server_name]

    def save_server_config(self, server_name: str, content: str) -> None:
        with self._lock:
            self._storage[server_name] = content

    def delete_server_config(self, server_name: str) -> None:
        with self._lock:
            if self.server_exists(server_name):
                del self._storage[server_name]
                self._enabled.discard(server_name)  # também desativa, se ativo
            else:
                raise ValueError(f"Server '{server_name}' does not exist")

    def validate_server_config(self, content: str) -> bool:
        """
        Simula a validação de configuração.
        Aqui usamos apenas uma regra simples: o conteúdo não pode estar vazio.
        """
        return bool(content and content.strip())

    def enable_server(self, server_name: str) -> None:
        """
        Simula ativar um servidor (equivalente a criar symlink em sites-enabled).
        """
        if not self.server_exists(server_name):
            raise ValueError(f"Server '{server_name}' does not exist")
        self._enabled.add(server_name)

    def disable_server(self, server_name: str) -> None:
        """
        Simula desativar um servidor (equivalente a remover symlink de sites-enabled).
        """
        if server_name not in self._enabled:
            raise ValueError(f"Server '{server_name}' is not enabled")
        self._enabled.remove(server_name)

    def is_server_enabled(self, server_name: str) -> bool:
        return server_name in self._enabled

    def restart_service(self) -> None:
        """
        Simula o restart do serviço Nginx.
        """
        print("Simulated Nginx restart with configs:", list(self._enabled))
