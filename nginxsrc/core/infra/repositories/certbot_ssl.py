import subprocess
from datetime import datetime
from typing import Optional
from ...domain.repositories.ssl_repository import SSLRepository
from ...domain.models.ssl import SSL

class CertbotSSLRepository(SSLRepository):
    """
    Implementação do SSLRepository que utiliza o Certbot (Let's Encrypt)
    para gerenciar certificados SSL no Linux.

    Esta classe executa comandos do Certbot via subprocess, permitindo
    instalar, remover e consultar certificados de forma programática.

    Exemplo de uso:
        repo = CertbotSSLRepository()
        repo.install("meusite.com", "admin@meusite.com")
        info = repo.info("meusite.com")
        print(info.expiry)
    """

    def _run_command(self, command: list[str]) -> subprocess.CompletedProcess:
        """Executa um comando shell e retorna o resultado, lançando erro em falhas."""
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Erro ao executar comando: {' '.join(command)}\n"
                f"Saída de erro: {e.stderr.strip()}"
            )

    def install(self, server_name: str, email: str) -> SSL:
        """
        Instala um certificado SSL para o domínio especificado.

        Args:
            server_name (str): Nome do domínio (ex: meusite.com)
            email (str): E-mail de contato para o Certbot.

        Returns:
            SSL: Objeto contendo o estado e data de expiração do certificado.
        """
        command = [
            "certbot", "certonly",
            "--nginx",
            "-d", server_name,
            "--non-interactive",
            "--agree-tos",
            "--email", email
        ]
        result = self._run_command(command)
        print(result.stdout)

        # Após a instalação, obtemos as informações do certificado
        return self.info(server_name)

    def uninstall(self, server_name: str):
        """
        Remove o certificado SSL do domínio especificado.
        """
        command = [
            "certbot", "delete",
            "--cert-name", server_name,
            "--non-interactive",
            "--quiet",
            "--no-self-upgrade"
        ]
        try:
            self._run_command(command)
        except RuntimeError as e:
            if "No certificate found" in str(e):
                print(f"Nenhum certificado encontrado para {server_name}.")
            else:
                raise

    def info(self, server_name: str) -> SSL:
        """
        Retorna informações sobre o certificado SSL do domínio informado.

        Executa `certbot certificates` e faz o parse da saída.

        Returns:
            SSL: Objeto contendo status, expiração e e-mail.
        """
        command = ["certbot", "certificates", "--cert-name", server_name]
        try:
            result = self._run_command(command)
            output = result.stdout

            active = "VALID" in output or "Certificate Name" in output
            expiry: Optional[datetime] = None
            email: Optional[str] = None

            for line in output.splitlines():
                if "Expiry Date:" in line:
                    # Exemplo: "Expiry Date: 2025-01-04 03:01:11+00:00 (VALID: 89 days)"
                    date_str = line.split("Expiry Date:")[1].split("(")[0].strip()
                    expiry = datetime.fromisoformat(date_str)
                elif "Email:" in line:
                    email = line.split("Email:")[1].strip()

            return SSL(active=active, expiry=expiry, email=email)

        except RuntimeError as e:
            # Certificado não encontrado
            if "No certificate found" in str(e) or "not found" in str(e).lower():
                return SSL(active=False)
            raise
