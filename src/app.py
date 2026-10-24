
from flask import Flask
from flask_cors import CORS

from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp

from config import config
from database import mysql

app = Flask(__name__)

CORS(app)

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)


# Página no encontrada
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


app.register_error_handler(404, pagina_no_encontrada)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
