# Proyecto Full-Stack ISPC

## Model

En este directorio se encuentran las clases del sistema que representan
los distintos modelos que participan en el dominio.

Los servicios utilizan los modelos aquí encontrados para interactuar con
el repositorio, ya sea temporal o permanente. Los modelos no saben con
cuál estarán trabajando, utilizan una clase abstracta que funciona como
interface y que les permite, por ejemplo, crear algo o borrar algo.
