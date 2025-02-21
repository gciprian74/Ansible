from awxkit.api import job_templates

from awx_conn import conectar_awx
from gest_templates import crear_template


def obtener_inventario_por_nombre(client, nombre):
    """
    Obtiene un inventyario de awx por su nombre
    """
    try:
        inventario = client.inventory.get(name=nombre).results[0]
        print("Inventario encontrado")
        return inventario
    except Exception:
        print("No se ha encontrado el inventario")
        return None

def main():
    
    client = conectar_awx()
    if client:
        try:

            # obtener proyecto
            proyecto = client.projects.get(name="myGitHubProject").results[0]

            # obtener inventario
            inventario = obtener_inventario_por_nombre(client, "Linux")
            # print("INVENTARIO:", inventario)

            # Obtener credencial
            credencial = client.credentials.get(name="LinuxCred").results[0]

            # crear template
            template = crear_template(
                            client=client, 
                            nombre="DemoJob7", 
                            proyecto_id=proyecto.id, 
                            playbook="playbooks/playbook1.yml",
                            inventario_id=inventario.id,
                            credencial_id=credencial.id
            )

            job_templates.JobTemplate.add_credential(template, credential=credencial)

            launch = job_templates.JobTemplate.launch(template)

            job_templates.JobTemplate.wait_until_status(launch, status='succesful', timeout=12)


        except Exception as e:
            print(f"Error en el proceso: {e}")

if __name__ == "__main__":
    main()

