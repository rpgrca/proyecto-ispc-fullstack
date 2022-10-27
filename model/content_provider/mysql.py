import mysql.connector
from mysql.connector import Error, errorcode
from datetime import date
from model.database import BaseDeDatos
from model.tipo_usuario import TipoDeUsuario
from model.usuarios import Usuario, Usuarios
from model.subastas import Subasta, Subastas
from model.articulos import Articulo, Articulos

class MysqlDatabase:
    def __init__(self, connection_string: list[str]):
        self.name = "bidon_subastas"
        self.extra_data = ["localhost", "root", "1234", "bidon_subastas"]
        self.refresh(connection_string)
        self.open()

    def refresh(self, connection_string: list[str]):
        self.__host = connection_string[0] if connection_string and connection_string[0] else self.extra_data[0]
        self.__user = connection_string[1] if connection_string and connection_string[1] else self.extra_data[1]
        self.__password = connection_string[2] if connection_string and connection_string[2] else self.extra_data[2]
        self.__database = connection_string[3] if connection_string and connection_string[3] else self.extra_data[3]
        self.extra_data = [self.__host, self.__user, self.__password, self.__database]

    def open(self):
        if not self.__connection:
            try:
                self.__connection = mysql.connector.connect(user=self.__user, password=self.__password, host=self.__host, database=self.__database, connection_timeout=5)
            except Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    raise ValueError("Error en el usuario o password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.__connection = mysql.connector.connect(user=self.__user, password=self.__password, host=self.__host)
                    cursor = self.__connection.cursor()
                    cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.__database)
                    cursor.execute("USE " + self.__database)
                    cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios ("
                                   "id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,"
                                   "nombre varchar(25) not null,"
                                   "apellido varchar(25) not null,"
                                   "email varchar(128) not null,"
                                   "usuario varchar(20) not null,"
                                   "clave varchar(20) not null,"
                                   "nacimiento date not null,"
                                   "tipo_usuario int not null,"
                                   ") ENGINE=InnoDB")
                    cursor.execute("CREATE TABLE IF NOT EXISTS Articulos ("
                                   "id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,"
                                   "titulo varchar(50) NOT NULL,"
                                   "description VARCHAR(512) NOT NULL,"
                                   "valuacion int not null,"
                                   "id_consignatario int not null,"
                                   "CONSTRAINT fk_id_consignatario FOREIGN KEY(id_consignatario) REFERENCES Usuarios(id)"
                                   ") ENGINE=InnoDB")
                    cursor.execute("CREATE TABLE IF NOT EXISTS Subastas ("
                                   "id int not null unique auto_increment primary key,"
                                   "fecha date not null,"
                                   "titulo varchar(50) not null,"
                                   "description varchar(50) not null,"
                                   "imagen varchar(256) not null"
                                   ") ENGINE=InnoDB")
                    cursor.execute("CREATE TABLE IF NOT EXISTS Lotes ("
                                   "id int not null unique auto_increment primary key,"
                                   "precio_base int not null,"
                                   "orden int not null,"
                                   "id_articulo int not null,"
                                   "id_subasta int not null,"
                                   "constraint fk_id_articulo foreign key (id_articulo) references Articulo (id),"
                                   "constraint fk_id_subasta foreign key (id_subasta) references Subastas (id)"
                                   ") ENGINE=InnoDB")
                    cursor.execute("CREATE TABLE IF NOT EXISTS Pujas ("
                                  "id int not null unique auto_increment primary key,"
                                  "monto int not null,"
                                  "id_pujador int not null,"
                                  "id_lote int not null,"
                                  "constraint fk_id_pujador foreign key (id_pujador) references Usuarios(id),"
                                  "constraint fk_id_lote foreign key (id_lote) references Lotes(id)"
                                  ") ENGINE=InnoDB")
                    cursor.execute("CREATE TABLE IF NOT EXISTS Ventas ("
                                   "id int not null unique auto_increment primary key,"
                                   "precio_final float not null,"
                                   "comision float not null,"
                                   "pago_consignatario float not null,"
                                   "id_puja int not null,"
                                   "constraint fk_id_puja foreign key(id_puja) references Pujas (id)"
                                   ") ENGINE=InnoDB")
                    self.__connection.commit()
                    cursor.close()
                else:
                    raise ValueError(err)

    def obtener_conexion(self):
        return self.__connection


class TablaSubastas(Subastas):
    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        pass

    def buscar_por_uid(self, uid: int) -> Subasta:
        pass

    def contar_lotes(self) -> int:
        pass


class TablaArticulos(Articulos):
    def agregar(self, articulo_uid: int):
        pass

    def buscar_por_uid(self, articulo_uid: int) -> Articulo:
        pass


class TablaUsuarios(Usuarios):
    EXISTE_USUARIO_SQL = "SELECT COUNT(id) FROM Usuarios WHERE usuario LIKE %s"
    EXISTE_USUARIO_CON_MAIL_SQL = "SELECT COUNT(id) FROM Usuarios WHERE email LIKE %s"

    def __init__(self, connection):
        self.__connection = connection

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        pass

    def existe(self, usuario: str) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute(self.EXISTE_USUARIO_SQL, (usuario))
        self.__connection.commit()
        valor = cursor().fetchone()[0] > 0
        cursor.close()
        return valor

    def buscar(self, usuario: str, clave: str) -> Usuario:
        pass

    def buscar_por_email(self, email: str, clave: str) -> Usuario:
        pass

    def existe_con_mail(self, email: str) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute(self.EXISTE_USUARIO_CON_MAIL_SQL, (email))
        self.__connection.commit()
        valor = cursor().fetchone()[0] > 0
        cursor.close()
        return valor


class CreadorDeBasesDeDatosMySql:
    def __init__(self):
        self.__connection = MysqlDatabase()
        self.__usuarios = TablaUsuarios(self.__connection.obtener_conexion())
        self.__subastas = TablaSubastas(self.__connection.obtener_conexion())
        self.__articulos = TablaArticulos(self.__connection.obtener_conexion())

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos)
