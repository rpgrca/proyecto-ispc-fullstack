class Usuario:
    def __init__(self, usuario, clave):
        self.__usuario = usuario
        self.__clave = clave

    def __str__(self):
        return self.__usuario


class Usuarios:
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        pass
    
    def existe(self, usuario: str) -> bool:
        pass
    
    def buscar(self, usuario: str, clave: str) -> Usuario:
        pass
    
    def existe_con_mail(self, email: str) -> bool:
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

    def buscar_por_email(self, email: str) -> bool:
        filtered_users = list(filter(lambda u: u['email'] == email, self.__usuarios.values()))
        return len(filtered_users) > 0

    def encriptar(self, clave: str):
        return clave