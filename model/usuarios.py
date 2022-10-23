from model.tipo_usuario import TipoDeUsuario


class Usuario:
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__usuario = usuario
        self.__clave = clave
        self.__nacimiento = nacimiento
        self.__tipo = tipo

    def __str__(self):
        return self.__usuario
    
    def obtener_clave(self) -> str:
        return self.__clave


class Pujador(Usuario):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)


class Consignatario(Usuario):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)


class Martillero(Usuario):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Martillero)


class Usuarios:
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario) -> None:
        pass
    
    def existe(self, usuario: str) -> bool:
        pass
    
    def buscar(self, usuario: str, clave: str) -> Usuario:
        pass
    
    def buscar_por_email(self, email: str, clave: str) -> Usuario:
        pass
    
    def existe_con_mail(self, email: str) -> bool:
        pass
    
    def encriptar(self, clave: str) -> str:
        pass


class UsuariosFactory:
    @staticmethod
    def crear(nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario):
        if tipo == TipoDeUsuario.Consignatario:
            return Consignatario(nombre, apellido, email, usuario, clave, nacimiento)
        elif tipo == TipoDeUsuario.Pujador:
            return Pujador(nombre, apellido, email, usuario, clave, nacimiento)
        else:
            return Martillero(nombre, apellido, email, usuario, clave, nacimiento)


class UsuariosImplementadoConDiccionario(Usuarios):
    def __init__(self, usuarios):
        self.__usuarios = usuarios
        
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario) -> None:
        self.__usuarios[usuario] = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "usuario": usuario,
            "clave": clave,
            "nacimiento": nacimiento,
            "tipo": tipo.value
        }

    def existe(self, usuario: str) -> bool:
        return usuario in self.__usuarios

    def buscar(self, usuario: str, clave: str) -> Usuario:
        if usuario in self.__usuarios:
            registro = self.__usuarios[usuario]
            if registro["clave"] == clave:
                return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"], registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_por_email(self, email: str) -> Usuario:
        registro = next(filter(lambda u: u["email"] == email, self.__usuarios.values()), None)
        if registro:
            return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"], registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None