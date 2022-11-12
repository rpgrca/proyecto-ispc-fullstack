# Proyecto Full-Stack ISPC

## Controller

Dentro de este directorio se encuentran los controladores secundarios
que son llamados desde el controlador principal, _main.py_ en el
directorio superior.

Los controladores se encargan de desempaquetar la información que viene
del _front-end_ y pasarla a los servicios que se encuentran en el
directorio _services_, y luego empaquetan la respuesta, la serializan a
JSON. No poseen lógica de negocios.
