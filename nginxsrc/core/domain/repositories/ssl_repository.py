from typing import Protocol
from ..models.ssl import SSL


class SSLRepository(Protocol):
    """
    Protocolo que define a interface para operações relacionadas à
    gestão de certificados SSL em um servidor.

    Este repositório abstrai as operações de instalação, remoção
    e consulta de informações de certificados SSL, permitindo que
    diferentes implementações (por exemplo, Certbot, Let's Encrypt,
    ou outras APIs) sigam um mesmo contrato.

    Métodos:
        install(server_name: str, email: str) -> SSL:
            Instala um novo certificado SSL para o domínio especificado.
            Pode utilizar ferramentas como Certbot para realizar o processo
            de emissão e configuração automática do certificado.

        uninstall(server_name: str) -> None:
            Remove o certificado SSL associado ao domínio informado.
            Essa operação deve também limpar qualquer configuração
            relacionada ao certificado, se aplicável.

        info(server_name: str) -> SSL:
            Retorna informações sobre o certificado SSL do domínio especificado,
            incluindo se está ativo, a data de expiração e o e-mail associado.

    Exemplo de uso:
        >>> repo: SSLRepository = CertbotSSLRepository()
        >>> ssl = repo.install("meusite.com", "admin@meusite.com")
        >>> print(ssl.expiry)
        2025-11-06 12:00:00
    """

    def install(self, server_name: str, email: str) -> SSL:
        """Instala um certificado SSL para o domínio especificado."""
        ...

    def uninstall(self, server_name: str):
        """Remove o certificado SSL do domínio informado."""
        ...

    def info(self, server_name: str) -> SSL:
        """Retorna informações sobre o certificado SSL do domínio informado."""
        ...
