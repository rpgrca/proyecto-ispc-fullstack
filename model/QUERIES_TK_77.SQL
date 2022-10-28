select count(u.NOMBRE) as cantidad
from USUARIOS u
where u.NOMBRE is not null
