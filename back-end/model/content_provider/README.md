# Proyecto Full-Stack ISPC

## Content Provider

En este directorio se encuentran las representaciones de los repositorios
soportados por el sistema.

El repositorio de MySQL implementa las abstracciones de los modelos
sobre una base de datos MySQL: transforma cada llamada a un método en
una query y retorna serializando utilizando una lambda.

También existe una representación temporal, en memoria, utilizando listas
y diccionarios. Esta forma es ideal para las pruebas unitarias ya que
responden de manera automática, pueden inicializarse con distintos
valores para simular bases usadas y no necesitan de tener instalada una
base de datos real en el sistema.

Utilizando los modelos y estos repositorios los servicios pueden pedirle
a un modelo que cree un elemento y el _content provider_ lo creará en el
soporte seleccionado y retornará un modelo de manera transparente, sin
que los controladores, los servicios o los modelos mismos sepan en dónde
están impactando.

Es posible implementar otros _content providers_ (por ejemplo, archivo
CSV, archivo JSON, Shelve, SQLite o incluso bases de datos no sql como
MongoDB o ZODB).
