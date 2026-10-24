from flask import Blueprint, jsonify, request
from database import mysql


maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


# Consultar todos los maestros
@maestros_bp.route("/", methods=["GET"])
def lista_maestro():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM maestros"
        cursor.execute(sql)

        datos = cursor.fetchall()

        maestros = []

        for fila in datos:
            maestro = {
                "idmaestro": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }

            maestros.append(maestro)

        return jsonify({
            "maestros": maestros,
            "mensaje": "Lista de maestros",
            "exito": True
        }), 200

    except Exception as ex:
        current_app.logger.error("Error al consultar maestros: %s", ex)

        return jsonify({
            "mensaje": "Error al consultar los maestros",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

 
 # Consultar un alumno por matrícula
@alumnos_bp.route("/<string:matricula>", methods=["GET"])
def leer_alumno(matricula):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM alumnos WHERE matricula = %s",
            (matricula,)
        )

        fila = cursor.fetchone()

        if fila is None:
            return jsonify({
                "mensaje": "Alumno no encontrado",
                "exito": False
            }), 404

        alumno = fila_a_diccionario(cursor, fila)

        return jsonify({
            "alumno": alumno,
            "exito": True
        }), 200

    except Exception as ex:
        current_app.logger.error("Error al consultar alumno: %s", ex)

        return jsonify({
            "mensaje": "Error al consultar el alumno",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# Registrar un alumno
@alumnos_bp.route("/", methods=["POST"])
def registrar_alumno():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Se requiere un objeto JSON",
            "exito": False
        }), 400

    campos = [
        "matricula",
        "nombre",
        "apaterno",
        "amaterno",
        "correo"
    ]

    if any(
        campo not in datos
        or not isinstance(datos[campo], str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            "mensaje": "Faltan campos obligatorios",
            "exito": False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        matricula = datos["matricula"].strip()

        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula = %s",
            (matricula,)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                "mensaje": "La matrícula ya existe",
                "exito": False
            }), 409

        cursor.execute("""
            INSERT INTO alumnos
            (matricula, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(datos[campo].strip() for campo in campos))

        mysql.connection.commit()

        return jsonify({
            "mensaje": "Alumno registrado correctamente",
            "exito": True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        current_app.logger.error("Error al registrar alumno: %s", ex)

        return jsonify({
            "mensaje": "Error al registrar el alumno",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# Modificar un alumno
@alumnos_bp.route("/<string:matricula>", methods=["PUT"])
def modificar_alumno(matricula):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict) or not datos:
        return jsonify({
            "mensaje": "No se recibieron datos para modificar",
            "exito": False
        }), 400

    nombre = datos.get("nombre")
    apaterno = datos.get("apaterno")
    amaterno = datos.get("amaterno")
    correo = datos.get("correo")

    if (
        not isinstance(nombre, str) or not nombre.strip()
        or not isinstance(apaterno, str) or not apaterno.strip()
        or not isinstance(correo, str) or not correo.strip()
        or not isinstance(amaterno, str)
    ):
        return jsonify({
            "mensaje": "Nombre, apellido paterno, apellido materno y correo son obligatorios",
            "exito": False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula = %s",
            (matricula,)
        )

        alumno = cursor.fetchone()

        if alumno is None:
            return jsonify({
                "mensaje": "No existe un alumno con esa matrícula",
                "exito": False
            }), 404

        sql = """
            UPDATE alumnos
            SET nombre = %s,
                apaterno = %s,
                amaterno = %s,
                correo = %s
            WHERE matricula = %s
        """

        cursor.execute(sql, (
            nombre.strip(),
            apaterno.strip(),
            amaterno.strip(),
            correo.strip(),
            matricula
        ))

        mysql.connection.commit()

        return jsonify({
            "mensaje": "Alumno modificado correctamente",
            "matricula": matricula,
            "exito": True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()
        current_app.logger.error("Error al modificar alumno: %s", ex)

        return jsonify({
            "mensaje": "Error al modificar el alumno",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# Eliminar un alumno
@alumnos_bp.route("/<string:matricula>", methods=["DELETE"])
def eliminar_alumno(matricula):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula = %s",
            (matricula,)
        )

        alumno = cursor.fetchone()

        if alumno is None:
            return jsonify({
                "mensaje": "No existe un alumno con esa matrícula",
                "exito": False
            }), 404

        cursor.execute(
            "DELETE FROM alumnos WHERE matricula = %s",
            (matricula,)
        )

        mysql.connection.commit()

        return jsonify({
            "mensaje": "Alumno eliminado correctamente",
            "matricula": matricula,
            "exito": True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()
        current_app.logger.error("Error al eliminar alumno: %s", ex)

        return jsonify({
            "mensaje": "Error al eliminar el alumno",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
