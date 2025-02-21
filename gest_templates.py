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


def ejecutar_template(template, extra_vars=None):
    """
    Ejecuta una template y espera a su finalizacion
    """
    try:
        
        job = template.launch(payload={'extra_vars': extra_vars or {}})
        print(f"Job con id {job.id} iniciado!")

        job.wait_until_completed()

        if job.status == 'successful':
            print("Trabajo completado correctamente")
            return True
        else:
            print("Trabajo completado con fallo")
            return False


    except Exception as e:
        print(f"Error en la ejecución: {e}")
        return False
    
def obtener_workflow(client, nombre):
    """
    Obtiene un workflow por nombre
    """
    try:
        workflow = client.workflow_job_templates.get(name=nombre).results[0]
        print("Workflow encontrado")
        return workflow
    except Exception:
        print("Error obteniendo el workflow")
        return None

def ejecutar_workflow(workflow, extra_vars=None):
    """
    Ejecuta un workfloy y monitoriza resultado
    """
    try:
        workflow_job = workflow.launch(payload={'extra_vars': extra_vars or {}})
        print("Se ha iniciadop la ejecucion del workflow")

        workflow_job.wait_until_completed()

        if workflow_job.status == "successful":
            print("WK completado correctamente")
            return True
        else:
            print("WK completado con fallo")
            return False

    except Exception:
        print("Error ejecutando el workflow")
        return False