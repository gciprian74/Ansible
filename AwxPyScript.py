"""
"Desarrolla un script en Python para gestionar proyectos en AWX que cumpla 
con los siguientes requisitos:

Conexión a AWX:

Implementar un sistema de conexión flexible que soporte tanto credenciales directas 
como variables de entorno
Manejar errores de conexión apropiadamente


Gestión de Proyectos SCM:

Crear una función para añadir nuevos proyectos Git a AWX
Permitir especificar:

Nombre del proyecto
URL del repositorio Git
Rama del repositorio (con 'main' como valor por defecto)


Vincular proyectos con organizaciones en AWX


Gestión de Organizaciones:

Implementar dos variantes de creación de proyectos:

Una versión simple que use la organización 'Default'
Una versión avanzada que permita especificar la organización


Verificar la existencia de la organización antes de crear el proyecto


Funcionalidades requeridas:

Búsqueda de organizaciones existentes
Creación de proyectos con parámetros básicos de Git
Manejo de errores en cada operación
Registro de operaciones exitosas y fallidas


El script debe incluir:

Documentación clara de todas las funciones
Manejo de errores robusto
Ejemplo de uso práctico



Ejemplo de uso esperado:

Conexión a una instancia local de AWX
Creación de un proyecto vinculado a un repositorio Git específico
Asignación del proyecto a una organización existente"
"""

from awxkit import config, utils
from awxkit.api import ApiV2, job_templates
from awxkit.api.resources import resources
import os

def conectar_awx(url=None, usuario=None, password=None):
    """""" # docstring

    config.base_url = url or os.environ.get('AWX_URL', 'http://127.0.0.1:40097/')
    config.credentials = utils.PseudoNamespace(
        {
            'default': {
                'username': usuario or os.environ.get('AWX_USER'),
                'password': password or os.environ.get('AWX_PASSWORD')
            }
        }
    )

    # establecer conexion
    connection = ApiV2()
    session = connection.load_session().get()
    session.get(resources)

    return session 

if __name__ == "__main__":
    
    session_connection = conectar_awx("http://127.0.0.1:40097/", "gciprian", '0841')

    template_by_id = session_connection.job_templates.get(id=9).results[0]
    print(template_by_id)
