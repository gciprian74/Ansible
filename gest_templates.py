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
