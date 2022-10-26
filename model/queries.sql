-- Lista de queries a utilizar
insert into Usuarios (nombre, apellido, email, usuario, clave, nacimiento, tipo_usuario)
values
(%s, %s, %s, %s, %s, %s, 2);