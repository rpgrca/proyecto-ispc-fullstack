# Proyecto Full-Stack ISPC

## Services

Dentro de este directorio se encuentran los servicios con parte de la
lógica de negocio del sistema. Cada uno de estos servicios es llamado
por uno o más controladores a pedido del _front-end_.

Los servicios reciben los datos que envía el _front-end_, los validan
(el front-end posee validaciones pero algunas se vuelven a repetir aquí
ya que un hacker podría contactar al _entry point_ directamente sin
pasar por los formularios del sitio web) y determinan los modelos a
llamar para agregar, modificar, obtener o borrar información. En caso
de ser necesario los servicios pueden retornar algún valor para que el
controlador lo serialice y lo envíe al _front-end_.

Es posible colocar toda la lógica dentro de los controladores, sin
embargo se decidió utilizar un acercamiento similar al que realiza
Angular separando en servicios las posibles acciones que puede realizar.
