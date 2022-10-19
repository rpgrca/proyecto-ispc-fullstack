# usuarios.py
#
# crear(usuario, nombre, apellido, email, clave, nacimiento, tipo)

class Usuario:
    def __init__(self, usuario, clave):
        self.__usuario = usuario
        self.__clave = clave

class UsuarioInvalido(Usuario):
    pass

class Usuarios:
    __usuarios = {
        "Roberto": "123456",
        "Martin": "654321",
        "Julia": "109283",
        "Estela": "777777"
    }

    def buscar(self, usuario: str, clave: str):
        if usuario in Usuarios.__usuarios:
            if Usuarios.__usuarios[usuario] == clave:
                return Usuario(usuario, clave)

        return UsuarioInvalido()
