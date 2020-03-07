from flask import Flask, make_response

from app.logging.MyLogger import MyLogger
from config import app_config

logger = MyLogger.__call__().get_logger()

from .init_data import InitData
global_data = InitData()

# Este es el modulo principal de la aplicacion donde se inicializa toda la configuracion de la instancia.
# Esto esta basado en un patron llamado application factory y se puede encontrar en la documentacion de flask.
# Su principal objetivo es poder tener una instancia de la aplicacion y que las diferentes extensiones como el
# framework de base de datos puedan ser compartidas a traves de la instancia. Es similar a un singleton y ademas
# permite cambiar la configuracion facilmente. Dentro del metodo create_app se inicializan las extensiones,
# por ejemplo, sqlalchemy como ORM y celery como scheduler de tareas en background.


def create_app(config_name):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    config_name = 'development'
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    MyLogger().init_app(app)

    # En las siguientes lineas se registran los modelos creados y los diferentes modulos encargados de las
    # funcionalidades de la aplicacion. Esto se hace con un concepto llamado blueprint y se puede encontrar en
    # la documentacion de flask. El objetivo es poder separar las funcionalidades en modulos, que incluyen la
    # logica de las vistas y los rutas de las diferentes funciones.

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    from .load_files import load_files as load_files_blueprint
    app.register_blueprint(load_files_blueprint)

    with app.app_context():

        @app.route('/no_data')
        def no_data_to_show():
            return "No hay datos para trabajar en este ambiente"

        @app.route('/health')
        def health():
            r = make_response("{code:200}")
            r.mimetype = 'application/json'
            return r

    return app

