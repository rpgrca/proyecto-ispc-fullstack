-- Lista de queries a utilizar

-- Agregar un usuario
insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 2);

-- Agregar una subasta
insert into Subastas (fecha, titulo, descripcion, imagen)
values
(%s, %s, %s, %s);

-- traer información de un usuario dado
select * from Usuarios
%s where id = %s;