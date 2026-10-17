from flask import Flask, render_template

app = Flask(__name__)

#Format sirve para hacer un pre formateo a la norma
#Decoradores o Rutas por medio de ruta

@app.route("/")
def index():
    titulo = "Pagina de Inicio"
    listado = ['Pyton', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("./index.html" , titulo=titulo,listado=listado)


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