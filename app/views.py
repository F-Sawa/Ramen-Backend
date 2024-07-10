from flask import jsonify, request
from app.models import Usuario
from app.models import Registro
from app.models import Receta
from app.models import LReceta
from app.models import Categoria



def getCategorias():
    listaCategorias = Categoria.getCategorias()
    lista_C=[Categoria.Serializar(categ) for categ in listaCategorias]
    return jsonify(lista_C),201

def GetRecetasCategoria():
    data = request.json
    id_categoria = data['id_categoria']
    listR=Categoria.GetRecetas(id_categoria)
    list_rpars=[LReceta.serialize(receta) for receta in listR]
    return jsonify(list_rpars)

def GetReceta():
    data = request.json
    id_receta = data['id_receta']
    res_Receta = Receta.getReceta(id_receta)
    SReceta=Receta.serialize(res_Receta)
    return jsonify(SReceta)

def Registrarse():
    data = request.json
    Usuario = data['usuario']
    Passw = data['passw']
    Correo = data['correo']
    resultado = Registro.Registrar(Usuario, Passw, Correo)
    if resultado.Resultado== True:
        return jsonify({'resultado':'0','message':resultado.Mensaje}),201
    else:
        return jsonify({'resultado':'-1','message':resultado.Mensaje}),201

def iniciarSesion():
    data = request.json
    usuario = data['usuario']
    passw = data['passw']
    resultado = Usuario.IniciarSesion(usuario,passw)
    if len(resultado) == 0:
        #Sesion no iniciada
        return jsonify( {"resultado":"-1", "message":"Error en usuario o contraseña", "id":"-1"})
    else:
        return jsonify (Usuario.serialize(resultado[0]))
    
def UpdateUsuario():
    data = request.json
    IDusr = data['IdUsuario']
    Correo = data['Correo']
    resultado = Usuario.UpdUsuario(IDusr, Correo)
    return jsonify({"resultado":"0","message":"Usuario actualizado con exito"})

def GetFavoritos():
    data = request.json
    IDusr = data['IdUsuario']
    favoritos= Receta.getFavoritos(IDusr)
    list_favsr=[Receta.serialize(favorito) for favorito in favoritos]
    return jsonify(list_favsr)

def AddFavorito():
    data = request.json
    IDusr = data['IdUsuario']
    IDcoctel = data['IdReceta']
    Receta.AgrFavorito(IDusr, IDcoctel)
    return jsonify({"resultado":"0","message":"Favorito agregado con exito"})


def DelFavorito():
    data = request.json
    id_receta = data['IdReceta']
    id_usuario = data['IdUsuario']
    Receta.DeleteFavorito(id_receta, id_usuario)
    return jsonify({"resultado":"0","message":"Favorito eliminado con exito"})

