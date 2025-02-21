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

    config.base_url = url or os.environ.get('AWX_URL', 'http://127.0.0.1:38835/')
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

def crear_template(client, nombre, proyecto_id, playbook, inventario_id, credencial_id):
    """"""
    try:
        # obtencion de artefactos
        proyecto = client.projects.get(id=proyecto_id)
        inventario = client.inventory.get(id=inventario_id)
        credencial = client.credentials.get(id=credencial_id)   

        # print("PROYECTO:", proyecto)
        # print("CREDENCIAL:", credencial)
        # print("INVENTARIO:", inventario)

        # creacion template
        template = client.job_templates.post({
            'name': nombre,
            'description': f'Template de {nombre}',
            'job_type': 'run',
            'inventory': inventario_id,
            'project': proyecto_id,
            'playbook': playbook,
            'credential': credencial_id,
            'become_enabled': True
        })

        # print("Template creada correctamente")
        return template
    
    except Exception as e:
        print(f"Error al crear la template: {e}")
        return None


def crear_proyecto(client, nombre, url_git, nombre_organizacion = "Default", branch='main'):
    """"""

    try:
        organizaciones = client.organizations.get().results
        organizacion = None

        for org in organizaciones:
            if org.name == nombre_organizacion:
                organizacion = org
                break

        if not organizacion:
                print(f"No se encontró la organización: {nombre_organizacion}")
                return None    

        proyecto = client.projects.post({
                'name': nombre,
                'description': f'Proyecto {nombre}',
                'scm_type': 'git',
                'scm_url': url_git,
                'scm_branch': branch,
                'organization': organizacion.id
            }) 

        return proyecto   
    except Exception as e:
        print(f"Error en la creacion del proyecto: {e}")
        return None



if __name__ == "__main__":
    
    # session_connection = conectar_awx("http://127.0.0.1:38835/", "admin", 'ehMpvwjPDl2Z6SA54KEEPNDTojatMfE0')
    session_connection = conectar_awx()

    if session_connection:
        proyecto = crear_proyecto(
            session_connection,
            "Protecto_From_Python",
            "https://github.com/jalbacar/ansible-pac2.git"
        )
    else:
        print("No se ha podido establecer la conexión.")

    # test
    # template_by_id = session_connection.job_templates.get(id=28).results[0]
    # print(template_by_id)
    # nombre_template = input("Nombre de la nueva template:")
    # demojob3_template = crear_template(
    #                         client=session_connection, 
    #                         nombre=nombre_template, 
    #                         proyecto_id=33, 
    #                         playbook="playbooks/playbook1.yml",
    #                         inventario_id=5,
    #                         credencial_id=6
    #                     )
    # if demojob3_template is not None:
    #     demojob3_template.credential = 6
    #     print("Temmplate creada correctamente")
    #     print(f"ID template:{demojob3_template.id}")
    #     print(f"Nombre template:{demojob3_template.name}")