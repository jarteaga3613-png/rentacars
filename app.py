
from flask import Flask
from database import mysql

from routes.acceso import acceso
from routes.administrador import administrador
from routes.cliente import cliente

app = Flask(__name__)

# Configuración de MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "flaskuser"
app.config["MYSQL_PASSWORD"] = "flaskpass"
app.config["MYSQL_DB"] = "renta_vehiculos"

# Clave para sesiones que se utilizará más adelante
app.secret_key = "123456"

# Inicializar MySQL
mysql.init_app(app)

# Registrar Blueprints
app.register_blueprint(acceso)
app.register_blueprint(administrador)
app.register_blueprint(cliente)

if __name__ == "__main__":
    app.run(debug=True)  # correr el servidor por defecto en el puerto 5000
