from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/saludar')
def hello():
    return "HOLA!!"

@app.route('/palindrome/<palabra>')
def es_palidromo(palabra):
    return str(palabra == palabra[::-1])


@app.route('/multiplo/<numero1>/<numero2>')
def es_multiplo(numero1, numero2):
    return str(int(numero1) % int(numero2) == 0)



@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/create_user/<nombre>/<apellido>/<passwd>/<uname>')
def create_user(nombre, apellido, passwd, uname):
    #crear un objeto (instancia de una entidad)
    user = entities.User(
        name = nombre,
        fullname = apellido,
        password = passwd,
        username = uname
    )

    #Guardar el objeto en la capa de persistencia
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "User created!"


@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]
    i = 0
    respuesta2= ""
    for user in users:
        respuesta2 += "Nombre: "+str(user.name)+ "&nbsp;&nbsp;&nbsp;&nbsp;"  +"Apellido: "+str(user.fullname) +"<br>"
        print(i, "NAME:\t", user.name, "\t\t", "APELLIDO:\t", user.fullname)
        i+=1
    return respuesta2



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
