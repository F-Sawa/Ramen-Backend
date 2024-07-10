from app.database import getDB
class ingrediente:
    def __init__(self, id, nombre, tipo):
        self.id = id
        self.nombre=nombre
        self.tipo= tipo
        

    def serialize(self):
        return self.nombre
    
    @staticmethod
    def getIngredientes(idReceta, tipo):
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select Id, Nombre from ingredientes where id in (select Nombre from ingredientes where idReceta = " + str(idReceta) +") and Tipo = " + str(tipo) + ";")
        rows = cursor.fetchall()
        ingreds=[]
        for row in rows:
            nuevo_ingr=ingrediente(row[0],row[1], tipo)
            ingreds.append(nuevo_ingr)
        cursor.close()
        return ingreds
    
    def getAllIngredientes():
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select id, nombre from ingredientesCoctel;")
        rows = cursor.fetchall()
        ingreds=[]
        for row in rows:
            nuevo_ingr=Usuario(row[0],row[1])
            ingreds.append(nuevo_ingr)
        cursor.close()
        return ingreds
class LReceta:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
    
    def serialize(self):
        salida = {
            "id": self.id,
            "nombre": self.nombre
        }
        return salida
    
class Categoria:
    def __init__(self, id, nombre, imagen, idFrente, idDorso):
        self.id = id
        self.nombre = nombre
        self.imagen = imagen
        self.idFrente= idFrente
        self.idDorso= idDorso

    
    def Serializar(self):
        datos = {
            "resultado":0,
            "id" : self.id,
            "nombre": self.nombre,
            "imagen": self.imagen,
            "idFrente":self.idFrente,
            "idDorso": self.idDorso
        }
        return datos
    
    
    @staticmethod
    
    def getCategorias():
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select id, Cat, Imagen, idFrente, idDorso from Categorias;")
        rows = cursor.fetchall()
        ncat=[]
        for row in rows:
            nuevo=Categoria(row[0], row[1], row[2], row[3], row[4])
            ncat.append(nuevo)

        cursor.close()
        return ncat
    
    def GetRecetas(id_Categoria):
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select id, Nombre from Recetas where idCategoria = " + str(id_Categoria) + ";")
        rows = cursor.fetchall()
        nrec=[]
        for row in rows:
            nuevo=LReceta(row[0], row[1])
            nrec.append(nuevo)

        cursor.close()
        return nrec
 
        
    
class Receta:
    #id, Nombre, PreparacionR, PreparacionA, idCategoria,NombreR,imagen
    def __init__(self, id, nombre, preparacionR,  preparacionA, idCategoria, NombreR, imagen):
        self.id = id
        self.nombre=nombre
        self.preparacionR=preparacionR
        self.preparacionA=preparacionA
        self.idCategoria=idCategoria
        self.NombreR=NombreR
        self.ingredientesR=[]
        self.ingredientesA=[]
        self.imagen = imagen
        

    def setIngredientes(self):
        self.ingredientesR=ingrediente.getIngredientes(self.id, "1")
        self.ingredientesA=ingrediente.getIngredientes(self.id, "2")

    @staticmethod
   
    def serialize(self):
        listIngredR=[ingrediente.serialize() for ingrediente in self.ingredientesR]
        listIngredA=[ingrediente.serialize() for ingrediente in self.ingredientesA]
        receta = {
            'resultado':0,
            'id' : self.id,
            'nombre':self.nombre,
            'preparacionR':self.preparacionR,
            'preparacionA':self.preparacionA,
            'idCategoria':self.idCategoria,
            'NombreR': self.NombreR,
            'imagen': self.imagen,
            'ingredientesR': listIngredR,
            'ingredientesA': listIngredA
            }
        return receta
    

    def getReceta(id):
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select Nombre, PreparacionR, PreparacionA, idCategoria, NombreR, imagen from recetas where id= " + str(id)+ ";")
        rows = cursor.fetchall()
        lReceta=""
        for row in rows:


            nuevo=Receta(id,row[0],row[1],row[2],row[3],row[4],row[5])
            nuevo.setIngredientes()
            lReceta= nuevo
        cursor.close()
        return lReceta
    
    @staticmethod
    def getFavoritos(idUsr):
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select receta from favoritos where usuario = " + str(idUsr) + ";")
        rows = cursor.fetchall()
        nidreceta=[]
        for row in rows:
            nidreceta.append(row[0])
        cursor.close()
        recetas = []
        for idReceta in nidreceta:
            receta = Receta.getReceta(idReceta)
            recetas.append(receta)

        return recetas


    def AgrFavorito(idUsuario, idReceta):
        db = getDB()
        cursor = db.cursor()
        query="insert into favoritos(usuario, receta) values("+ str(idUsuario) + ", " + str(idReceta) +");"
        cursor.execute(query)
        db.commit()
        return
    
    
    def DeleteFavorito(idReceta, idUsuario):
        db = getDB()
        cursor = db.cursor()
        query="delete from favoritos where receta = " + str(idReceta) + " and usuario=" + str(idUsuario) + " ;"
        cursor.execute(query)
        db.commit()
        return
    
class Usuario:
    #ID	Usuario	Nombre	Preparacion	DeAutor	FechaCreacion	Imagen
    def __init__(self, id,  correo, usuario):
        self.id = id
        self.usuario = usuario
        self.correo=correo

        
    def serialize(self):
        return{
            'resultado': "0",
            'id' : self.id,
            'usuario':self.usuario,
            'correo':self.correo,

        }
    
    def IniciarSesion(usuario, passw):
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select id, mail from usuarios where User = '" + usuario + "' and Pass = '" + passw + "'")
        rows = cursor.fetchall()
        nusuario=[]
        for row in rows:
            nuevo_usr=Usuario(row[0],row[1],usuario)
            nusuario.append(nuevo_usr)
        cursor.close()
        return nusuario
        
    def ExisteUsuario(usr, Passw):
        usr = Usuario.IniciarSesion(usr,Passw)
        if len(usr) > 0:
           return True
            #resultado OK
        else:
           return False
            #resultadoError

    def ExisteCorreo(Correo):
        db = getDB()
        cursor = db.cursor()
        cursor.execute("select id from usuarios where mail = '" + Correo + "' order by id DESC LIMIT 1")
        rows = cursor.fetchall()
        Cantidad=0

        for row in rows:
            Cantidad= int(row[0])

        if Cantidad > 0:
           return True
            #resultado OK
        else:
           return False
            #resultadoError        
    
    def UpdUsuario(idUsr, Correo):
        result = Registro()
        usre= Usuario.ExisteCorreo(Correo)
        if usre==True:
           result.MResultado(False, "Correo Existente", Correo)
           return result

        db = getDB()
        cursor = db.cursor()
        cursor.execute("update usuarios set Mail = '" + Correo +"' where id = " + str(idUsr) + ";")
        db.commit()
        result.Mensaje ="Actualizado correctamente"
        result.Resultado = True
        result.Usuario = Correo
        return result
    
class Registro:
    def __init__(self):
        pass
    def MResultado(self, resultado, mensaje, usuario):
        self.Resultado = resultado
        self.Mensaje = mensaje
        self.Usuario = usuario
        
    @staticmethod
    

    def Registrar(usuario, Passw, Correo):
        result = Registro()
        # ----> Verificaciones previas <-----
        usre = Usuario.ExisteUsuario(usuario, Passw)
        if usre==True:
           result.MResultado(False, "Usuario Existente", usuario)
           return result
        usre = Usuario.ExisteCorreo(Correo)
        if usre==True:
           result.MResultado(False, "Correo Existente", usuario)
           return result
        
        db = getDB()
        cursor = db.cursor()
        query=""
        query = "insert into Usuarios(User, Mail, Pass) values ('"+ usuario +"','" + Correo + "','"+ Passw + "');"

        cursor.execute(query)
        db.commit()
    
        usre = Usuario.ExisteUsuario(usuario, Passw)

        if usre==True:
           result.MResultado(True, "Registro Satisfactorio!", usuario)
        else:
            result.MResultado(False, "Registro Error", usuario)

        return result

