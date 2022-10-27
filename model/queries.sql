-- Lista de queries a utilizar
insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 2);

insert into Subastas (fecha, titulo, descripcion, imagen)
values
(%s, %s, %s, %s);

insert into Lotes (precio_base, orden, id_articulo, id_subasta)
values
(%s, %s, %s, %s);