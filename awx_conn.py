from awxkit import config, utils
from awxkit.api import ApiV2
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