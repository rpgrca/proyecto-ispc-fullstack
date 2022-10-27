-- Lista de queries a utilizar

-- Agregar un usuario
insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 2);

insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 3);

-- Agregar una subasta
insert into Subastas (fecha, titulo, descripcion, imagen)
values
(%s, %s, %s, %s);

-- traer información de un usuario dado
select * from Usuarios
where id = %s;

insert into Lotes (precio_base, orden, id_articulo, id_subasta)
values
(%s, %s, %s, %s);

-- Crear un registro de venta
insert into Ventas (precio_final, comision, pago_consignatario, id_puja)
values
(%s, %s, %s, %s);