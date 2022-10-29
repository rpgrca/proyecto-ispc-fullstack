import mysql.connector
from mysql.connector import Error, errorcode
from datetime import date
from model.database import BaseDeDatos
from model.lotes import Lote, Lotes
from model.pujas import Puja, Pujas
from model.tipo_usuario import TipoDeUsuario
from model.usuarios import Consignatario, Pujador, Usuario, Usuarios
from model.subastas import Subasta, Subastas
from model.articulos import Articulo, Articulos


class MysqlDatabase:
    def __init__(self, connection_string: list[str]):
        self.name = "bidon_subastas"
        self.extra_data = ["localhost", "root", "1234", "bidon_subastas"]
        self.configurar(connection_string)
        self.open()

    def configurar(self, connection_string: list[str]):
        self.__host = connection_string[0] if connection_string and connection_string[0] else self.extra_data[0]
        self.__user = connection_string[1] if connection_string and connection_string[1] else self.extra_data[1]
        self.__password = connection_string[2] if connection_string and connection_string[2] else self.extra_data[2]
        self.__database = connection_string[3] if connection_string and connection_string[3] else self.extra_data[3]
        self.extra_data = [self.__host, self.__user, self.__password, self.__database]

    def open(self):
        if not self.__connection:
            try:
                self.__connection = mysql.connector.connect(user=self.__user, password=self.__password, host=self.__host,
                                                            database=self.__database, connection_timeout=5)
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

    def contar(self, sql: str, valores=()) -> int:
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql, valores)
            self.__connection.commit()
            record = cursor.fetchone()
            if record is not None:
                return record[0]
        except:
            pass
        
        return 0

    def obtener_uno(self, sql: str, valores=(), creator=lambda r: None):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql, valores)
            self.__connection.commit()
            record = cursor.fetchone()
            if record is not None:
                return creator(record)
        except:
            pass

        return None

    def obtener_muchos(self, sql: str, valores=(), creador=lambda r: None):
        try:
            resultado = []
            cursor = self.__connection.cursor()
            cursor.execute(sql, valores)
            self.__connection.commit()
            records = cursor.fetchall()
            for record in records:
                resultado.append(creador(record))

            return resultado
        except:
            pass

        return []

    def insertar(self, sql: str, valores=(), creator=lambda i, v: None):
        try:
            cursor = self.__connection.cursor()
            sql = "INSERT INTO Subastas VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, valores)
            self.__connection.commit()
            return creator(cursor.lastrowid, valores)
        except:
            pass

        return None

    def obtener_conexion(self):
        return self.__connection


class TablaSubastas(Subastas):
    BUSCAR_SUBASTA = "SELECT id, titulo, descripcion, imagen, fecha FROM Subastas WHERE id = %s"
    CREAR_SUBASTA = "INSERT INTO Subastas VALUES (%s,%s,%s,%s)"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        return self.__db.insertar(self.CREAR_SUBASTA, (titulo, descripcion, imagen, fecha),
                                  lambda i, v: Subasta(i, v[0], v[1], v[2], v[3]))

    def buscar_por_uid(self, uid: int) -> Subasta:
        return self.__db.obtener_uno(self.BUSCAR_SUBASTA, (uid),
                                     lambda r: Subasta(r[0], r[1], r[2], r[3], r[4]))


class TablaArticulos(Articulos):
    CREAR_ARTICULO = "INSERT INTO Articulos" # FIXME
    BUSCAR_ARTICULO = "SELECT id FROM Articulos" # FIXME
    BUSCAR_POR_CONSIGNATARIO = "SELECT id FROM Articulos WHERE consignatario_id = %s"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, uid: int):
        return self.__db.insertar(self.CREAR_ARTICULO, (uid), lambda i, v: Articulo(i))

    def buscar_por_uid(self, uid: int) -> Articulo:
        return self.__db.obtener_uno(self.BUSCAR_ARTICULO, (uid), lambda r: Articulo(r[0]))

    def listar_articulos_propiedad_de(self, consignatario: Consignatario) -> list[Articulo]:
        return self.__db.obtener_muchos(self.BUSCAR_POR_CONSIGNATARIO, (consignatario.obtener_uid()),
                                        lambda r: Articulo(r[0]))



class TablaUsuarios(Usuarios):
    EXISTE_USUARIO_SQL = "SELECT COUNT(id) FROM Usuarios WHERE usuario LIKE %s"
    EXISTE_USUARIO_CON_MAIL_SQL = "SELECT COUNT(id) FROM Usuarios WHERE email LIKE %s"
    OBTENER_USUARIO = "SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo FROM Usuarios " \
                      "WHERE usuario = %s AND clave = %s"
    OBTENER_USUARIO_LOGIN = "SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo FROM Usuarios " \
                            "WHERE usuario = %s"
    CREAR_USUARIO = "INSERT INTO Usuarios(nombre, apellido, email, usuario, clave, nacimiento, tipo) " \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s)"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        self.__db.insertar(self.CREAR_USUARIO, (nombre, apellido, email, usuario, clave, nacimiento, tipo))

    def existe(self, usuario: str) -> bool:
        return self.__db.contar(self.EXISTE_USUARIO_SQL, (usuario)) > 0

    def buscar(self, usuario: str, clave: str) -> Usuario:
        return self.__db.obtener_uno(self.OBTENER_USUARIO, (usuario, clave),
                                     lambda r: Usuario(r[0], r[1], r[2], r[3], r[4], r[1], r[6], r[7]))

    def buscar_por_email(self, email: str) -> Usuario:
        return self.__db.obtener_uno(self.OBTENER_USUARIO_LOGIN, (email),
                                     lambda r: Usuario(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

    def existe_con_mail(self, email: str) -> bool:
        return self.__db.contar(self.EXISTE_USUARIO_CON_MAIL_SQL, (email)) > 0


class TablaLotes(Lotes):
    LOTES_POR_SUBASTA = "SELECT COUNT(id) FROM Lotes WHERE subasta_id = %s"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, subasta: Subasta, articulo: Articulo, base: int, orden: int) -> None:
        pass

    def contar_lotes(self, subasta: Subasta) -> int:
        return self.__db.contar(self.LOTES_POR_SUBASTA, subasta.obtener_uid())

    def obtener(self, subasta: Subasta, orden: int) -> Lote:
        pass

    def buscar_por_uid(self, lote_uid: int) -> Lote:
        pass


class TablaPujas(Pujas):
    CREAR_PUJA = "INSERT INTO Pujas" # FIXME
    BUSCAR_PUJA = "SELECT id, monto, pujador_id, lote_id" # FIXME

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, monto: int, pujador: Pujador, lote: Lote):
        self.__db.insertar(self.CREAR_PUJA, (monto, pujador.obtener_uid(), lote.obtener_uid()))

    def buscar_por_monto(self, monto: int) -> Puja:
        pass

    def buscar_ultima_puja(self, lote: Lote) -> Puja:
        pass

    def buscar_por_uid(self, uid: int) -> Puja:
        return self.__db.obtener_uno(self.BUSCAR_PUJA, (uid), lambda r: Puja(r[0], r[1], Pujador(r[2]), Lote(r[3])))

    def buscar_por_lote(self, lote: Lote) -> list[Puja]:
        pass


class CreadorDeBasesDeDatosMySql:
    def __init__(self):
        self.__db = MysqlDatabase()
        self.__usuarios = TablaUsuarios(self.__db)
        self.__subastas = TablaSubastas(self.__db)
        self.__articulos = TablaArticulos(self.__db)
        self.__lotes = TablaLotes(self.__db)
        self.__pujas = TablaPujas(self.__db)

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos, self.__lotes, self.__pujas)
