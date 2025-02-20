from awxkit import config, utils
from awxkit.api import ApiV2, job_templates
from awxkit.api.resources import resources


# conexion (credenciales)
config.base_url = "http://127.0.0.1:40097/"
config.credentials = utils.PseudoNamespace(
    {
        'default': {
            'username': 'gciprian',
            'password': '0841'
        }
    }
)

session_connection = ApiV2().load_session().get()
session_connection.get(resources)

template_by_id = session_connection.job_templates.get(id=22).results[0]
print(template_by_id)
