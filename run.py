from flask import Flask, request
from app.database import init_app
from app.views import *
from app.models import Registro
from flask_cors import CORS


app = Flask(__name__)

init_app(app) #le pasamos la app a "init app"
#permitir solicitudes desde cualquier origen
CORS(app)

#Devuelve la lista de categorias de la web
app.route("/apis/categorias", methods = ["GET"])(getCategorias)


#Devuelve los nombres de las recetas de cada categoría para la pantalla principal
#Se le pasa el ID de la categoria
app.route("/apis/categoriasr", methods = ["POST"])(GetRecetasCategoria)
    
#Devuelve la receta seleccionada a partir del return de la lista anterior
#Se le pasa el ID de la categoría
app.route("/apis/receta", methods = ["POST"])(GetReceta)

#Intenta registrar el usuario y devuelve el resultado
app.route("/apis/usuario/registro", methods = ["POST"])(Registrarse)

#Intenta hacer Login del usuario y devuelve el resultado
app.route("/apis/usuario/login", methods = ["POST"])(iniciarSesion)

#Actualiza el usuario y devuelve el resultado
app.route("/apis/usuario/update", methods = ["POST"])(UpdateUsuario)

app.route("/apis/favoritos/get", methods = ["POST"])(GetFavoritos)

app.route("/apis/favoritos", methods = ["POST"])(AddFavorito)

app.route("/apis/favoritos", methods = ["DELETE"])(DelFavorito)





 
# app.route("/apis/sesion", methods = ["POST"])(iniciarSesion)

# @app.route("/apis/registro", methods = ["POST"])
# def Registrar():
#     data = request.json
#     return Registrarse(data)
    
if __name__ == "__main__":
    app.run(debug = True)
    