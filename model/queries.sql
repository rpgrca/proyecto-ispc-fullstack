-- Lista de queries a utilizar

-- Agregar un usuario pujador
insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 2);

-- Agregar un usuario consignatario
insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 3);

-- Agregar una subasta
insert into Subastas (fecha, titulo, descripcion, imagen)
values
(%s, %s, %s, %s);

-- PERFIL: traer información de un usuario dado
select * from Usuarios
where id = %s;

-- PERFIL: sobreescribir la información de un usuario dado
UPDATE Usuarios 
SET nombre = %s, apellido = %s, email = %s, usuario = %s, clave = %s, nacimiento = %s  
WHERE id = %s;

-- Crear un registro de Lotes
insert into Lotes (precio_base, orden, id_articulo, id_subasta)
values
(%s, %s, %s, %s);

-- Crear un registro de venta
insert into Ventas (precio_final, comision, pago_consignatario, id_puja)
values
(%s, %s, %s, %s);

-- Crear un registro de puja
insert into Pujas (monto, id_pujador, id_lote)
values
(%s, %s, %s);

-- Crear un registro de artículo
INSERT INTO Articulos (titulo, descripcion, valuacion, id_consignatario)
VALUES (%s, %s, %s, %s);

-- Traer todas las ventas hechas para un comprador dado 
select v.id v_id, precio_final, comision, pago_consignatario
from Usuarios u
inner join Pujas p on u.id = p.id_pujador
inner join Ventas v on p.id = v.id_puja
where u.id = %s

-- Traer último registro de Subastas
select * from Subastas
order by Fecha  desc limit 1;

-- LOGIN: Traer todos los usuarios según nombre de usuario y clave dados
SELECT * FROM Usuarios
WHERE usuario = %s AND clave = %s;

-- Contar cantidad de usuarios con nombre
select count(u.NOMBRE) as cantidad
from USUARIOS u
where u.NOMBRE is not null;

-- insertar usuario
INSERT INTO usuarios (nombre, apellido, email, usuario, clave, nacimineto, tipo_usuario) 
            VALUES ('Juan Pablo','Garcia','jpg@gmail.com','juan22','12_jpg_h21','10-10-2000',1 );

-- contar usuarios con email
select count(u.NOMBRE) as cantidad
from USUARIOS u
where u.EMAIL is not null

-- articulos sin ventas
select a.*
from articulos a
where a.id not in (select l.id_articulo from lotes l group by 1)

-- lotes por una subasta especifica
select l.*
from lotes l
where l.id_subasta=%s

 
