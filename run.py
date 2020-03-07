import os
from app import create_app

# Script usado para arrancar la aplicacion. Primero se importa el metodo create_app encargado de crear una
#  instancia de la aplicacion con la configuracion indicada en la variable de entorno. Si no esta declarada
#  la variable de entorno en el sistema no sera posible crear la instancia de la aplicacion.

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
