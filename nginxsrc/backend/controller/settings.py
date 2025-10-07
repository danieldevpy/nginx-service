from dataclasses import dataclass
from .. import NginxSettingsService

@dataclass
class SettingsController:
    settings_service: NginxSettingsService

    def reload(self):
        return self.settings_service.reload()
    
    def status(self):
        return self.settings_service.get_status()
    
    def clean_servers(self):
        return self.settings_service.clean_servers()