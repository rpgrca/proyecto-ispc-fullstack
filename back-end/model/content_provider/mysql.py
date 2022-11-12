from typing import Any
import mysql.connector
from mysql.connector import Error, errorcode
from datetime import date
from model.database import BaseDeDatos
from model.lotes import Lote, Lotes
from model.pujas import Puja, Pujas
from model.tipo_usuario import TipoDeUsuario
from model.usuarios import Consignatario, Martillero, Pujador, Usuario, Usuarios
from model.subastas import Subasta, Subastas
from model.articulos import Articulo, Articulos
from model.libro_diario import Venta, LibroDiario


class MysqlDatabase:
    def __init__(self, connection_string: list[str]):
        self.__conexion = None
        self.__default = ["localhost", "root", "1234", "bidon_subastas"]
        self._configurar(connection_string)
        self._open()

    def _configurar(self, connection_string: list[str]):
        self.__host = connection_string[0] if connection_string and connection_string[0] else self.__default[0]
        self.__user = connection_string[1] if connection_string and connection_string[1] else self.__default[1]
        self.__password = connection_string[2] if connection_string and connection_string[2] else self.__default[2]
        self.__database = connection_string[3] if connection_string and connection_string[3] else self.__default[3]
        self.__default = [self.__host, self.__user, self.__password, self.__database]

    def _open(self):
        if not self.__conexion:
            try:
                self.__conexion = mysql.connector.connect(user=self.__user, password=self.__password, host=self.__host,
                                                          database=self.__database, connection_timeout=5)
            except Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    raise ValueError("Error en el usuario o password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.__conexion = mysql.connector.connect(user=self.__user, password=self.__password, host=self.__host)
                    cursor = self.__conexion.cursor()
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
                                   "tipo_usuario int not null"
                                   ") ENGINE=InnoDB")
                    self.__conexion.commit()
                    cursor.close()

                    cursor = self.__conexion.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Articulos ("
                                   "id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,"
                                   "titulo varchar(50) NOT NULL,"
                                   "descripcion VARCHAR(512) NOT NULL,"
                                   "valuacion int not null,"
                                   "id_consignatario int not null,"
                                   "CONSTRAINT fk_id_consignatario FOREIGN KEY(id_consignatario) REFERENCES Usuarios(id)"
                                   ") ENGINE=InnoDB")
                    self.__conexion.commit()
                    cursor.close()

                    cursor = self.__conexion.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Subastas ("
                                   "id int not null unique auto_increment primary key,"
                                   "fecha date not null,"
                                   "titulo varchar(50) not null,"
                                   "descripcion varchar(50) not null,"
                                   "imagen varchar(256) not null"
                                   ") ENGINE=InnoDB")
                    self.__conexion.commit()
                    cursor.close()

                    cursor = self.__conexion.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Lotes ("
                                   "id int not null unique auto_increment primary key,"
                                   "precio_base int not null,"
                                   "orden int not null,"
                                   "id_articulo int not null,"
                                   "id_subasta int not null,"
                                   "constraint fk_id_articulo foreign key (id_articulo) references Articulos (id),"
                                   "constraint fk_id_subasta foreign key (id_subasta) references Subastas (id)"
                                   ") ENGINE=InnoDB")
                    self.__conexion.commit()
                    cursor.close()

                    cursor = self.__conexion.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Pujas ("
                                   "id int not null unique auto_increment primary key,"
                                   "monto int not null,"
                                   "id_pujador int not null,"
                                   "id_lote int not null,"
                                   "constraint fk_id_pujador foreign key (id_pujador) references Usuarios(id),"
                                   "constraint fk_id_lote foreign key (id_lote) references Lotes(id)"
                                   ") ENGINE=InnoDB")
                    self.__conexion.commit()
                    cursor.close()

                    cursor = self.__conexion.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS Ventas ("
                                   "id int not null unique auto_increment primary key,"
                                   "precio_final float not null,"
                                   "comision float not null,"
                                   "pago_consignatario float not null,"
                                   "id_puja int not null,"
                                   "constraint fk_id_puja foreign key(id_puja) references Pujas (id)"
                                   ") ENGINE=InnoDB")
                    self.__conexion.commit()
                    cursor.close()
                else:
                    raise ValueError(err)

    def obtener_cursor(self):
        return self.__conexion.cursor(buffered=True)

    def contar(self, sql: str, valores=()) -> int:
        try:
            cursor = self.obtener_cursor()
            cursor.execute(sql, valores)
            self.__conexion.commit()
            record = cursor.fetchone()
            if record is not None:
                return record[0]
        except Exception as err:
            raise err

    def obtener_uno(self, sql: str, valores=(), creator=lambda r: None) -> Any:
        try:
            cursor = self.obtener_cursor()
            cursor.execute(sql, valores)
            self.__conexion.commit()
            record = cursor.fetchone()
            if record is not None:
                return creator(record)
        except Exception as err:
            raise err

    def obtener_muchos(self, sql: str, valores=(), creador=lambda r: None) -> list[Any]:
        try:
            resultado = []
            cursor = self.obtener_cursor()
            cursor.execute(sql, valores)
            self.__conexion.commit()
            records = cursor.fetchall()
            for record in records:
                resultado.append(creador(record))

            return resultado
        except Exception as err:
            raise err

    def insertar(self, sql: str, valores=(), creator=lambda i, v: None) -> Any:
        try:
            cursor = self.obtener_cursor()
            cursor.execute(sql, valores)
            self.__conexion.commit()
            return creator(cursor.lastrowid, valores)
        except Exception as err:
            raise err

    def actualizar(self, sql: str, valores=()) -> None:
        try:
            cursor = self.obtener_cursor()
            cursor.execute(sql, valores)
            self.__conexion.commit()
        except Exception as err:
            raise err

    def borrar(self, sql: str, valores=()) -> None:
        try:
            cursor = self.obtener_cursor()
            cursor.execute(sql, valores)
            self.__conexion.commit()
        except Exception as err:
            raise err


class TablaSubastas(Subastas):
    BUSCAR_SUBASTA = "SELECT id, titulo, descripcion, imagen, fecha FROM Subastas WHERE id = %s"
    CREAR_SUBASTA = "INSERT INTO Subastas(titulo, descripcion, imagen, fecha) VALUES (%s,%s,%s,%s)"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        return self.__db.insertar(self.CREAR_SUBASTA, (titulo, descripcion, imagen, fecha),
                                  lambda i, v: Subasta(i, v[0], v[1], v[2], v[3]))

    def buscar_por_uid(self, uid: int) -> Subasta:
        return self.__db.obtener_uno(self.BUSCAR_SUBASTA, (uid,),
                                     lambda r: Subasta(r[0], r[1], r[2], r[3], r[4]))


class TablaArticulos(Articulos):
    CREAR_ARTICULO = "INSERT INTO Articulos(titulo, descripcion, valuacion, id_consignatario) VALUES (%s,%s,%s,%s)"
    BUSCAR_ARTICULO = """
    SELECT Articulos.id, titulo, descripcion, valuacion, id_consignatario, nombre, apellido, email, usuario, clave, nacimiento
      FROM Articulos, Usuarios
      WHERE Articulos.id = %s
        AND id_consignatario = Usuarios.id"""
    BUSCAR_POR_CONSIGNATARIO = "SELECT id, titulo, descripcion, valuacion FROM Articulos WHERE id_consignatario = %s"
    CONTAR_ARTICULOS = "SELECT COUNT(id) FROM Articulos"
    LISTAR_ARTICULOS = """
    SELECT id, titulo, descripcion, valuacion, id_consignatario, nombre, apellido, email, usuario, clave, nacimiento,
           tipo_usuario
      FROM Articulos, Usuarios
     WHERE id_consignatario = Usuarios.id
    """
    BORRAR_ARTICULO = "DELETE FROM Articulos WHERE id = %s"
    ACTUALIZAR_ARTICULO = """
    UPDATE Articulos
       SET titulo = %s, descripcion= %s, valuacion = %s, id_consignatario = %s
     WHERE id = %s
    """

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def crear(self, titulo: str, descripcion: str, valuacion: int, consignatario: Consignatario) -> Articulo:
        return self.__db.insertar(self.CREAR_ARTICULO, (titulo, descripcion, valuacion, consignatario.obtener_uid()),
                                  lambda i, r: Articulo(i, r[0], r[1], r[2], r[3]))

    def buscar_por_uid(self, uid: int) -> Articulo:
        return self.__db.obtener_uno(self.BUSCAR_ARTICULO, (uid,), lambda r: Articulo(r[0], r[1], r[2], r[3],
                                     Consignatario(r[4], r[5], r[6], r[7], r[8], r[9], r[10])))

    def listar_articulos_propiedad_de(self, consignatario: Consignatario) -> list[Articulo]:
        return self.__db.obtener_muchos(self.BUSCAR_POR_CONSIGNATARIO, (consignatario.obtener_uid(),),
                                        lambda r: Articulo(r[0], r[1], r[2], r[3], consignatario))

    def contar(self) -> int:
        return self.__db.contar(self.CONTAR_ARTICULOS)

    def listar(self) -> list[Articulo]:
        return self.__db.obtener_muchos(self.LISTAR_ARTICULOS, (), lambda r: Articulo(r[0], r[1], r[2], r[3],
                                        Usuarios.crear(r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11])))

    def borrar(self, uid: int) -> None:
        self.__db.borrar(self.BORRAR_ARTICULO, (uid,))

    def actualizar(self, articulo: Articulo, titulo: str, descripcion: str, valuacion: int,
                   consignatario: Consignatario) -> None:
        self.__db.actualizar(self.ACTUALIZAR_ARTICULO, (titulo, descripcion, valuacion, consignatario.obtener_uid(),
                                                        articulo.obtener_uid()))


class TablaUsuarios(Usuarios):
    EXISTE_USUARIO_SQL = "SELECT COUNT(id) FROM Usuarios WHERE usuario LIKE %s"
    EXISTE_USUARIO_CON_MAIL_SQL = "SELECT COUNT(id) FROM Usuarios WHERE email LIKE %s"
    OBTENER_USUARIO = """
        SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario
          FROM Usuarios
         WHERE usuario = %s AND clave = %s"""
    OBTENER_USUARIO_POR_EMAIL = """
        SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario
          FROM Usuarios
         WHERE email LIKE %s"""
    CREAR_USUARIO = """
        INSERT INTO Usuarios(nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
             VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    BUSCAR_USUARIO_POR_ID_Y_TIPO = """
        SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario
          FROM Usuarios
         WHERE id = %s AND tipo_usuario = %s"""
    BUSCAR_USUARIO_POR_ID = """
        SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario
          FROM Usuarios
         WHERE id = %s"""
    BUSCAR_MARTILLERO = """
        SELECT id, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario
          FROM Usuarios
         WHERE tipo_usuario = 1"""
    ACTUALIZAR_USUARIO = "UPDATE Usuarios SET usuario = %s, email = %s, clave = %s WHERE id = %s"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        self.__db.insertar(self.CREAR_USUARIO, (nombre, apellido, email, usuario, clave, nacimiento, tipo.value))

    def existe(self, usuario: str) -> bool:
        return self.__db.contar(self.EXISTE_USUARIO_SQL, (usuario,)) > 0

    def buscar(self, usuario: str, clave: str) -> Usuario:
        return self.__db.obtener_uno(self.OBTENER_USUARIO, (usuario, clave),
                                     lambda r: Usuarios.crear(r[0], r[1], r[2], r[3], r[4], r[1], r[6], r[7]))

    def buscar_por_email(self, email: str) -> Usuario:
        return self.__db.obtener_uno(self.OBTENER_USUARIO_POR_EMAIL, (email,),
                                     lambda r: Usuarios.crear(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    def existe_con_mail(self, email: str) -> bool:
        return self.__db.contar(self.EXISTE_USUARIO_CON_MAIL_SQL, (email,)) > 0

    def buscar_pujador_por_uid(self, uid: int) -> Pujador:
        return self.__db.obtener_uno(self.BUSCAR_USUARIO_POR_ID_Y_TIPO, (uid, TipoDeUsuario.Pujador.value),
                                     lambda r: Usuarios.crear(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    def buscar_consignatario_por_uid(self, uid: int) -> Consignatario:
        return self.__db.obtener_uno(self.BUSCAR_USUARIO_POR_ID_Y_TIPO, (uid, TipoDeUsuario.Consignatario.value),
                                     lambda r: Usuarios.crear(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    def buscar_usuario_por_uid(self, uid: int) -> Usuario:
        return self.__db.obtener_uno(self.BUSCAR_USUARIO_POR_ID, (uid,),
                                     lambda r: Usuarios.crear(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    def buscar_martillero(self) -> Martillero:
        return self.__db.obtener_uno(self.BUSCAR_MARTILLERO, (),
                                     lambda r: Usuarios.crear(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    def actualizar(self, cuenta: Usuario, usuario: str, email: str, clave: str) -> None:
        self.__db.actualizar(self.ACTUALIZAR_USUARIO, (usuario, email, clave, cuenta.obtener_uid()))


class TablaLotes(Lotes):
    CONTAR_LOTES_POR_SUBASTA = "SELECT COUNT(id) FROM Lotes WHERE id_subasta = %s"
    CREAR_LOTE = "INSERT INTO Lotes(id_subasta, id_articulo, precio_base, orden) VALUES(%s,%s,%s,%s)"
    LOTES_POR_SUBASTA = """
        SELECT Lotes.id, id_articulo, titulo, descripcion, valuacion, id_consignatario, nombre, apellido,
               email, usuario, clave, nacimiento, tipo_usuario, precio_base, orden
          FROM Lotes, Articulos, Usuarios
         WHERE id_subasta = %s
           AND Usuarios.id = id_consignatario
           AND Articulos.id = id_articulo"""
    LOTE_DE_SUBASTA = """
        SELECT Lotes.id, id_articulo, titulo, descripcion, valuacion, id_consignatario, nombre, apellido,
               email, usuario, clave, nacimiento, tipo_usuario, precio_base, orden
          FROM Lotes, Articulos, Usuarios
         WHERE id_subasta = %s
           AND orden = %s
           AND Usuarios.id = id_consignatario
           AND Articulos.id = id_articulo"""
    BUSCAR_LOTE = """
        SELECT Lotes.id, id_subasta, s.titulo, s.descripcion, s.imagen, s.fecha, id_articulo, a.titulo,
               a.descripcion, valuacion, id_consignatario, nombre, apellido, email, usuario, clave, nacimiento,
               tipo_usuario, precio_base, orden
          FROM Lotes, Articulos a, Usuarios, Subastas s
         WHERE Lotes.id = %s
           AND s.id = id_subasta
           AND Usuarios.id = id_consignatario
           AND id_articulo = a.id"""

    EXISTE_CON_ARTICULO = "SELECT COUNT(*) FROM Lotes WHERE id_articulo = %s"

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, subasta: Subasta, articulo: Articulo, base: int, orden: int) -> None:
        self.__db.insertar(self.CREAR_LOTE, (subasta.obtener_uid(), articulo.obtener_uid(), base, orden))

    def contar_lotes(self, subasta: Subasta) -> int:
        return self.__db.contar(self.CONTAR_LOTES_POR_SUBASTA, (subasta.obtener_uid(),))

    def obtener(self, subasta: Subasta, orden: int) -> Lote:
        return self.__db.obtener_uno(self.LOTE_DE_SUBASTA, (subasta.obtener_uid(), orden),
                                     lambda r: Lote(r[0], subasta, Articulo(r[1], r[2], r[3], r[4],
                                                    Usuarios.crear(r[5], r[6], r[7], r[8], r[9], r[10], r[11],
                                                    r[12])), r[13], r[14]))

    def buscar_por_uid(self, lote_uid: int) -> Lote:
        return self.__db.obtener_uno(self.BUSCAR_LOTE, (lote_uid,),
                                     lambda r: Lote(r[0], Subasta(r[1], r[2], r[3], r[4], r[5]), Articulo(r[6], r[7], r[8],
                                                    r[9], Usuarios.crear(r[10], r[11], r[12], r[13], r[14], r[15],
                                                    r[16], r[17])), r[18], r[19]))

    def listar(self, subasta: Subasta) -> list[Lote]:
        return self.__db.obtener_muchos(self.LOTES_POR_SUBASTA, (subasta.obtener_uid(),),
                                        lambda r: Lote(r[0], subasta, Articulo(r[1], r[2], r[3], r[4],
                                                       Usuarios.crear(r[5], r[6], r[7], r[8], r[9], r[10], r[11],
                                                       r[12])), r[13], r[14]))

    def existe_con_articulo(self, articulo: Articulo) -> bool:
        return self.__db.contar(self.EXISTE_CON_ARTICULO, (articulo.obtener_uid(),)) > 0


class TablaPujas(Pujas):
    CREAR_PUJA = "INSERT INTO Pujas(id_pujador, id_lote, monto) VALUES (%s,%s,%s)"
    BUSCAR_PUJA = "SELECT id, id_pujador, id_lote, monto FROM Pujas WHERE id = %s"
    BUSCAR_POR_LOTE = """
        SELECT Pujas.id, id_pujador, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario, monto
          FROM Pujas, Usuarios
         WHERE id_lote = %s
           AND id_pujador = Usuarios.id
      ORDER BY Pujas.id ASC"""
    BUSCAR_ULTIMA_PUJA = """
        SELECT Pujas.id, id_pujador, nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario, monto
          FROM Pujas, Usuarios
         WHERE id_lote = %s
           AND id_pujador = Usuarios.id
      ORDER BY Pujas.id DESC
         LIMIT 1
    """

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def agregar(self, pujador: Pujador, lote: Lote, monto: int):
        self.__db.insertar(self.CREAR_PUJA, (pujador.obtener_uid(), lote.obtener_uid(), monto))

    def buscar_ultima_puja(self, lote: Lote) -> Puja:
        return self.__db.obtener_uno(self.BUSCAR_ULTIMA_PUJA, (lote.obtener_uid(),),
                                     lambda r: Puja(r[0], Usuarios.crear(r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                                                                         r[8]), lote, r[9]))

    def buscar_por_uid(self, uid: int) -> Puja:
        return self.__db.obtener_uno(self.BUSCAR_PUJA, (uid,), lambda r: Puja(r[0], r[1], Pujador(r[2]), Lote(r[3])))

    def buscar_por_lote(self, lote: Lote) -> list[Puja]:
        return self.__db.obtener_muchos(self.BUSCAR_POR_LOTE, (lote.obtener_uid(),),
                                        lambda r: Puja(r[0], Usuarios.crear(r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                                                                            r[8]), lote, r[9]))


class TablaVentas(LibroDiario):
    CREAR_VENTA = "INSERT INTO Ventas(id_puja, precio_final, comision, pago_consignatario) VALUES (%s,%s,%s,%s)"
    BUSCAR_VENTA_CON_DATOS = """
            SELECT v.id, p.id, p.id_pujador, u.nombre, u.apellido, u.email, u.usuario, u.clave,
                   u.nacimiento, u.tipo_usuario, v.precio_final, v.comision, v.pago_consignatario
              FROM Ventas v
        INNER JOIN Pujas p on p.id = id_puja
        INNER JOIN Usuarios u on u.id = p.id_pujador
             WHERE v.id = %s"""
    LISTAR_COMPRAS = """
            SELECT v.id, p.id, p.id_pujador, u.nombre, u.apellido, u.email, u.usuario, u.clave,
                   u.nacimiento, u.tipo_usuario, v.precio_final, v.comision, v.pago_consignatario
              FROM Usuarios u
        INNER JOIN Pujas p ON u.id = p.id_pujador
        INNER JOIN Ventas v ON p.id = v.id_puja
             WHERE u.id = %s"""

    def __init__(self, db: MysqlDatabase):
        self.__db = db

    def crear(self, puja: Puja, precio_final: float, comision: float, pago_a_consignatario: float) -> Venta:
        return self.__db.insertar(self.CREAR_VENTA, (puja.obtener_lote().obtener_uid(), precio_final, comision,
                                  pago_a_consignatario), lambda i, r: Venta(i, r[0], r[1], r[2], r[3]))

    def buscar_por_uid(self, uid: int) -> Venta:
        return self.__db.obtener_uno(self.BUSCAR_VENTA_CON_DATOS, (uid,), lambda r: Venta(r[0], Puja(r[1], r[2], r[3], r[4]),
                                     r[5], r[6], r[7]))

    def listar_compras_de(self, pujador: Pujador) -> list[Venta]:
        return self.__db.obtener_muchos(self.LISTAR_COMPRAS, (pujador.obtener_uid(),),
                                        lambda r: Venta(r[0], Puja(r[1], r[2], r[3], r[4]), r[5], r[6], r[7]))


class CreadorDeBasesDeDatosMySql:
    def __init__(self, connection_string: list[str]):
        self.__db = MysqlDatabase(connection_string)
        self.__usuarios = TablaUsuarios(self.__db)
        self.__subastas = TablaSubastas(self.__db)
        self.__articulos = TablaArticulos(self.__db)
        self.__lotes = TablaLotes(self.__db)
        self.__pujas = TablaPujas(self.__db)
        self.__ventas = TablaVentas(self.__db)

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos, self.__lotes, self.__pujas, self.__ventas)
