import subprocess
from pathlib import Path
from typing import Optional
from ...domain.repositories.nginx_repository import NginxRepository


class NginxRepositoryLinux(NginxRepository):
    """
    Implementação de NginxRepository para Linux.
    - Validação de sintaxe usa PID temporário, não precisa de sudo.
    - Operações reais em /etc/nginx requerem sudo/root.
    """

    def __init__(
        self,
        sudo_password: str,
        sites_available: Optional[str] = "/etc/nginx/sites-available",
        sites_enabled: Optional[str] = "/etc/nginx/sites-enabled",
    ):
        self.sudo_password = sudo_password
        self.sites_available = Path(sites_available)
        self.sites_enabled = Path(sites_enabled)

    # ---------------------------
    # Função auxiliar sudo
    # ---------------------------

    def _run_sudo(self, command: list[str]) -> None:
        """Executa um comando com sudo usando a senha fornecida."""
        subprocess.run(
            ["sudo", "-S"] + command,
            input=f"{self.sudo_password}\n",
            text=True,
            check=True
        )

    # ---------------------------
    # Operações de arquivo real
    # ---------------------------

    def server_exists(self, server_name: str) -> bool:
        return (self.sites_available / server_name).exists()

    def get_server_config(self, server_name: str) -> str:
        config_path = self.sites_available / server_name
        if not config_path.exists():
            raise FileNotFoundError(f"Server config '{server_name}' does not exist")
        return config_path.read_text()

    def save_server_config(self, server_name: str, content: str) -> None:
        tmp_path = Path("/tmp") / server_name
        tmp_path.write_text(content)
        target_path = self.sites_available / server_name
        self._run_sudo(["mv", str(tmp_path), str(target_path)])

    def delete_server_config(self, server_name: str) -> None:
        config_path = self.sites_available / server_name
        enabled_path = self.sites_enabled / server_name
        if config_path.exists():
            self._run_sudo(["rm", "-f", str(config_path)])
        if enabled_path.exists() and enabled_path.is_symlink():
            self._run_sudo(["rm", "-f", str(enabled_path)])

    def enable_server(self, server_name: str) -> None:
        available_path = self.sites_available / server_name
        enabled_path = self.sites_enabled / server_name
        if not available_path.exists():
            raise FileNotFoundError(f"Server config '{server_name}' does not exist")
        if not enabled_path.exists():
            self._run_sudo(["ln", "-s", str(available_path), str(enabled_path)])

    def disable_server(self, server_name: str) -> None:
        enabled_path = self.sites_enabled / server_name
        if enabled_path.exists() and enabled_path.is_symlink():
            self._run_sudo(["rm", "-f", str(enabled_path)])

    def is_server_enabled(self, server_name: str) -> bool:
        enabled_path = self.sites_enabled / server_name
        return enabled_path.exists() and enabled_path.is_symlink()

    # ---------------------------
    # Validação de configuração
    # ---------------------------

    def validate_server_config(self, content: str) -> bool:
        """
        Valida a configuração do server sem precisar de root.
        Cria um arquivo temporário em /tmp com PID próprio.
        """
        temp_file = "/tmp/nginx_test.conf"
        Path(temp_file).write_text(self._wrap_in_temp_http_block(content))
        result = subprocess.run(
            ["/usr/sbin/nginx", "-t", "-c", temp_file],
            capture_output=True,
            text=True
        )
        if 'syntax is ok' in result.stderr:
            return True
        return result.returncode == 0

    def _wrap_in_temp_http_block(self, content: str) -> str:
        """
        Coloca o server block em um arquivo temporário completo para teste.
        Define PID em /tmp para não precisar de root.
        """
        return f"pid /tmp/nginx_test.pid;\nevents {{}}\nhttp {{\n{content}\n}}"

    # ---------------------------
    # Reinício do serviço
    # ---------------------------

    def restart_service(self) -> None:
        """Reinicia o serviço Nginx. Necessita de permissão root."""
        self._run_sudo(["systemctl", "restart", "nginx"])
