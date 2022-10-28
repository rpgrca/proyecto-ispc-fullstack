select count(u.NOMBRE) as cantidad
from USUARIOS u
where u.EMAIL is not null

