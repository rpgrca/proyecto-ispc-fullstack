class Usuario:
    def __init__(self, usuario, clave):
        self.__usuario = usuario
        self.__clave = clave

    def __str__(self):
        return self.__usuario


class Usuarios:
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        pass
    
    def existe(self, usuario: str):
        pass
    
    def buscar(self, usuario: str, clave: str):
        pass
    
    def buscar_por_email(self, email: str):
        pass
    
    def encriptar(self, clave: str):
        pass


class UsuariosImplementadoConDiccionario(Usuarios):
    def __init__(self, usuarios):
        self.__usuarios = usuarios
        
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        self.__usuarios[usuario] = { "clave": clave, "email": email }

    def existe(self, usuario: str):
        return usuario in self.__usuarios

    def buscar(self, usuario: str, clave: str):
        if usuario in self.__usuarios:
            if self.__usuarios[usuario]['clave'] == self.encriptar(clave):
                return Usuario(usuario, clave)

        return None

    def buscar_por_email(self, email: str):
        usuario = filter(lambda u: u['email'] == email, Usuarios.__usuarios)

    def encriptar(self, clave: str):
        return clave