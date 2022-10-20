# usuarios.py
#
# crear(usuario, nombre, apellido, email, clave, nacimiento, tipo)

class Usuario:
    def __init__(self, usuario, clave):
        self.__usuario = usuario
        self.__clave = clave

    def __str__(self):
        return self.__usuario


class Usuarios:
    __usuarios = {
        "Roberto": { "clave": "123456", "email": "roberto.carlos.alfonso@gmail.com" },
        "Martin": { "clave": "654321", "email": "martin@gmail.com" },
        "Julia": { "clave": "109283", "email": "julia@gmail.com" },
        "Estela": { "clave": "777777", "email": "estela@gmail.com" }
    }

    def existe(self, usuario):
        return usuario in Usuarios.__usuarios

    def buscar(self, usuario: str, clave: str):
        if usuario in Usuarios.__usuarios:
            if Usuarios.__usuarios[usuario]['clave'] == self.encriptar(clave):
                return Usuario(usuario, clave)

        return None

    def buscar_por_email(self, email: str):
        usuario = filter(lambda u: u['email'] == email, Usuarios.__usuarios)

    def encriptar(self, clave: str):
        return clave
