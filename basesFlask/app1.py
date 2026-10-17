from flask import Flask, render_template, request
import math

app = Flask(__name__)

#Format sirve para hacer un pre formateo a la norma
#Decoradores o Rutas por medio de ruta

@app.route("/")
def index():
    titulo = "Pagina de Inicio"
    listado = ['Pyton', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("./index.html" , titulo=titulo,listado=listado)

@app.route("/distancia", methods=["GET", "POST"])
def distancia():

    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0
    res = 0

    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        n3 = request.form.get('n3')
        n4 = request.form.get('n4')

        res = ((float(n3) - float(n1))**2 + (float(n4) - float(n2))**2)**0.5

    return render_template('distancia.html', n1=n1, n2=n2, n3=n3, n4=n4, res=res)

@app.route("/operasbas", methods=["GET" , "POST"])
def operasbas():
    n1 = 0
    n2 = 0
    res = 0
    operacion = ''
    
    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')

        if request.form.get('operacion') == 'sumar': 
            operacion = 'suma'
            res =float(n1)+ float (n2)
        if request.form.get('operacion') == 'restar': 
            operacion = 'restar'
            res =float(n1)- float (n2)
        if request.form.get('operacion') == 'multiplicar': 
            operacion = 'multiplicar'
            res =float(n1)* float (n2)

    return render_template('operasbas.html', n1=n1,n2=n2, res=res, operacion=operacion)


@app.route("/hola")
def Hola():
    return "<h1> Hola PWA - IEVN1003 </h1>"


@app.route("/numero/<int:n>")
def numero(n):
    return "<h1> Numero {} </h1>".format(n)


@app.route("/user/<string:nom>")
def user(nom):
    return "<h1> Hola User: {} </h1>".format(nom)


@app.route("/user/<int:id>/<string:username>")
def user_id(id, username):
    return "<h1> ID: {} Nombre: {} </h1>".format(id, username)


@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "<h1>La Suma es: {} </h1>".format(n1+n2)


if __name__ == "__main__":
    app.run(debug=True)