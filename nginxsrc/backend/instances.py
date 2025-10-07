from . import (
    ServerService,
    JinjaServerRenderer,
    NginxRepositoryDocker,
    NginxRepositoryLinux,
    NginxSettingsService,
    SSLService,
    CertbotSSLRepository,
    ServerSqlModel,
    create_engine_instance,
    create_tables
    )

class InstancesRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Criando uma nova instância de InstancesRepository")
            cls._instance = super(InstancesRepository, cls).__new__(cls)
            cls._instance._init_repositories()
        return cls._instance

    def _init_repositories(self):
        # Inicialize aqui seus repositórios
        self.repo_nginx = NginxRepositoryDocker()
        self.settings_service = NginxSettingsService(
            repo_nginx=self.repo_nginx
        )
        self.server_service= ServerService(
            repo_nginx=self.repo_nginx,
            repo_render=JinjaServerRenderer()
        )
        engine = create_engine_instance("sqlite:///database.db")
        create_tables(engine)
        self.server_repository = ServerSqlModel(engine)
        self.ssl_service = SSLService(self.repo_nginx, CertbotSSLRepository())
        

