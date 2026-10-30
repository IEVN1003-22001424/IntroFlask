from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def fila_a_diccionario(cursor, fila):
    columnas= [columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

@maestros_bp.route("/", methods=['GET'])
def lista_maestros():
    try:
        cursor = mysql.connection.cursor()
        sql="select * from maestros"
        cursor.execute(sql)
        datos = cursor.fetchall()
        maestros=[]

        for fila in datos:
            maestro={"idmaestro":fila[0], "nombre":fila[1],
                    "apaterno":fila[2], "amaterno":fila[3],
                    "correo":fila[4]}
            maestros.append(maestro)

        return jsonify({'maestros':maestros,'mensaje':"Lista de Maestros",'exito':True})
    except Exception as ex:
        return jsonify({"mensage": "error{}".format(ex), 'exito':False})