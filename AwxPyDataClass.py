from dataclasses import dataclass
from typing import Optional, Dict, Any
from awxkit import api, config, utils
from awxkit.api import ApiV2, job_templates
from awxkit.api.resources import resources
import os
from enum import Enum

@dataclass
class AWXCredentials:
    """Dataclass para almacenar las credenciales de AWX"""
    username: str
    password: str
    url: str
    environment: str = "production"  # o "testing"

    @classmethod
    def from_env(cls, environment: str = "production") -> 'AWXCredentials':
        return cls(
            username=os.environ.get('AWX_USERNAME', ''),
            password=os.environ.get('AWX_PASSWORD', ''),
            url=os.environ.get('AWX_URL', 'https://127.0.0.1'),
            environment=environment
        )

@dataclass
class JobResult:
    """Dataclass para resultados de jobs"""
    job_id: int
    status: str
    success: bool
    error_message: Optional[str] = None

class JobStatus(Enum):
    """Estados posibles de un job"""
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'
    ERROR = 'error'

class AWXError(Exception):
    """Excepción base para errores de AWX"""
    pass

class AWXConnectionError(AWXError):
    """Excepción para errores de conexión"""
    pass

class AWXResourceError(AWXError):
    """Excepción para errores de recursos"""
    pass

class AWXJobError(AWXError):
    """Excepción para errores de jobs"""
    pass

class AWXManager:
    """Clase principal para gestionar AWX"""
    def __init__(self, credentials: Optional[AWXCredentials] = None):
        self._credentials = credentials or AWXCredentials.from_env()
        self._session = None
        self._connected = False

    def connect(self) -> bool:
        """Establece la conexión con AWX"""
        try:
            self._configure_connection()
            connection = ApiV2()
            self._session = connection.load_session().get()
            self._session.get(resources)
            self._connected = True
            return True
        except Exception as e:
            raise AWXConnectionError(f"Error al conectar con AWX: {e}")

    def _configure_connection(self) -> None:
        """Configura los parámetros de conexión"""
        config.base_url = self._credentials.url
        config.credentials = utils.PseudoNamespace({
            'default': {
                'username': self._credentials.username,
                'password': self._credentials.password
            }
        })

    def get_inventory(self, name: str = "inventario") -> Dict[str, Any]:
        """Obtiene un inventario por nombre"""
        if not self._connected:
            raise AWXConnectionError("No hay conexión establecida con AWX")
        
        try:
            inventory = self._session.inventory.get(name=name).results[0]
            return {
                'id': inventory.id,
                'name': inventory.name
            }
        except Exception as e:
            raise AWXResourceError(f"Error al obtener inventario: {e}")

    def get_template(self, name: str) -> Dict[str, Any]:
        """Obtiene una template por nombre"""
        if not self._connected:
            raise AWXConnectionError("No hay conexión establecida con AWX")
        
        try:
            template = self._session.job_templates.get(name=name).results[0]
            return {
                'id': template.id,
                'name': template.name,
                'template_obj': template
            }
        except Exception as e:
            raise AWXResourceError(f"Error al obtener template: {e}")

    def execute_template(self, template: Any, extra_vars: Optional[Dict] = None) -> JobResult:
        """Ejecuta una template y espera su finalización"""
        if not self._connected:
            raise AWXConnectionError("No hay conexión establecida con AWX")

        try:
            job = template.launch(payload={'extra_vars': extra_vars or {}})
            job.wait_until_completed()

            return JobResult(
                job_id=job.id,
                status=job.status,
                success=job.status == JobStatus.SUCCESSFUL.value,
                error_message=None if job.status == JobStatus.SUCCESSFUL.value 
                            else f"Job falló con estado: {job.status}"
            )
        except Exception as e:
            raise AWXJobError(f"Error al ejecutar template: {e}")

class AWXExecutionManager:
    """Clase para gestionar la ejecución de templates"""
    def __init__(self, awx_manager: AWXManager):
        self.awx = awx_manager

    def run_installation_template(self) -> JobResult:
        """Ejecuta el template de instalación"""
        try:
            template = self.awx.get_template("Instalar Aplicaciones")
            return self.awx.execute_template(template['template_obj'])
        except Exception as e:
            return JobResult(0, "error", False, str(e))

    def run_configuration_template(self, service: str, port: int) -> JobResult:
        """Ejecuta el template de configuración"""
        try:
            template = self.awx.get_template("Configurar Servicios")
            return self.awx.execute_template(
                template['template_obj'],
                {'servicio': service, 'puerto': port}
            )
        except Exception as e:
            return JobResult(0, "error", False, str(e))

def main():
    try:
        # Crear credenciales
        credentials = AWXCredentials(
            url="http://127.0.0.1:40097/",
            username="gciprian",
            password="0841"
        )

        # Inicializar managers
        awx = AWXManager(credentials)
        awx.connect()
        execution_manager = AWXExecutionManager(awx)

        # Obtener inventario
        inventory = awx.get_inventory()
        print(f"Inventario obtenido: {inventory['name']}")

        # Ejecutar templates
        install_result = execution_manager.run_installation_template()
        if install_result.success:
            print(f"Instalación completada. Job ID: {install_result.job_id}")
        else:
            print(f"Error en instalación: {install_result.error_message}")

        config_result = execution_manager.run_configuration_template("nginx", 80)
        if config_result.success:
            print(f"Configuración completada. Job ID: {config_result.job_id}")
        else:
            print(f"Error en configuración: {config_result.error_message}")

    except AWXConnectionError as e:
        print(f"Error de conexión: {e}")
    except AWXResourceError as e:
        print(f"Error de recursos: {e}")
    except AWXJobError as e:
        print(f"Error en ejecución: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()