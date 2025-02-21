from awxkit.api import job_templates

from awx_conn import conectar_awx
from gest_templates import obtener_workflow, ejecutar_workflow

def main():
    client = conectar_awx()
    if client:
        try:
            workflow = obtener_workflow(client=client, nombre="Pac2_wf")
            if ejecutar_workflow(workflow=workflow):
                print("WORKFLOW OK!")
            else:
                print("WORKFLOW NO OK!")
                
        except Exception:
            print("Errorn el el proceso de workflow")

if __name__ == "__main__":
    main()