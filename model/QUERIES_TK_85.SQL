select a.*
from articulos a
where a.id not in (select l.id_articulo from lotes l group by 1)

