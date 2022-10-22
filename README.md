[![contrib][contrib-img]][contrib-url]
[![commit][commit-img]][commit-url]
[![discuss][discuss-img]][discuss-url]
[![issues][issues-img]][issues-url]
[![Python package][pipeline-img]][pipeline-url]
[![codecov][codecov-img]][codecov-url]

## Proyecto Full-Stack ISPC

Información para el Sprint 1:

### Front-end

index.html realiza una navegación como visitante sin identificarse.
Contamos con las ventanas internas de la aplicación, sin embargo al no
poder autenticarse no es posible reemplazar los encabezados con las
páginas correctas. Sin embargo pueden levantar las páginas internas
individualmente para revisarlas aunque clickear en el encabezado pueda
redirigirlos a la navegación como invitado.

Las imágenes no son nuestras, las descripciones fueron basadas en otras
descripciones ya disponibles en internet.

### Diagramas para back-end

- [Diagrama de colaboración entre clases](https://github.com/rpgrca/proyecto-ispc-fullstack/wiki/Diagrama-de-colaboraci%C3%B3n-entre-clases)
- [Diagrama de clases](https://github.com/rpgrca/proyecto-ispc-fullstack/wiki/Diagrama-de-clases)
- [Diagrama relacional](https://github.com/rpgrca/proyecto-ispc-fullstack/wiki/Diagrama-relacional)
- [Diagrama entidad relación](https://github.com/rpgrca/proyecto-ispc-fullstack/wiki/Diagrama-entidad-relaci%C3%B3n)

### Notas

- Nosotros utilizamos sitio como base para el html, cuando se nos
informó que debíamos tener un directorio llamado view en su lugar lo
renombramos lo que ocasionó que el historial del directorio se volviese
inaccesible. Sin embargo es posible revisar el historial de cada uno de
los archivos html para ver los autores de las versiones más antiguas.

- Tuvimos un problema de merging de un commit y sobreescribió algunos
historiales con un commit erróneo. Afectó principalmente a los archivos
Python, si se revisa el historial el commit de la creación fue
reemplazado por un commit de un renombre como si todos los archivos
hubiesen sido creados a partir del mismo archivo. No sabemos cómo pasó.

- No tenemos una distribución uno a uno entre páginas web en la vista y
modelos o controladores. Existen páginas que reusarán controladores,
habrán páginas que no tendrán controladores ni modelos asociados (como
las de Quiénes somos o la de Cómo funciona), existen controladores que
utilizarán distintos modelos y otros que utilizarán los mismos.

[commit-img]: https://img.shields.io/github/commit-activity/w/rpgrca/proyecto-ispc-fullstack/dev
[commit-url]: https://github.com/rpgrca/proyecto-ispc-fullstack/graphs/code-frequency
[contrib-img]: https://img.shields.io/github/contributors/rpgrca/proyecto-ispc-fullstack
[contrib-url]: https://github.com/rpgrca/proyecto-ispc-fullstack/graphs/contributors
[issues-img]: https://img.shields.io/github/issues/rpgrca/proyecto-ispc-fullstack
[issues-url]: https://github.com/rpgrca/proyecto-ispc-fullstack/issues
[discuss-img]: https://img.shields.io/github/discussions/rpgrca/proyecto-ispc-fullstack
[discuss-url]: https://github.com/rpgrca/proyecto-ispc-fullstack/discussions
[pipeline-img]: https://github.com/rpgrca/proyecto-ispc-fullstack/actions/workflows/python.yml/badge.svg
[pipeline-url]: https://github.com/rpgrca/proyecto-ispc-fullstack/actions/workflows/python.yml
[codecov-img]: https://codecov.io/gh/rpgrca/proyecto-ispc-fullstack/branch/dev/graph/badge.svg?token=b8dMxouJmA
[codecov-url]: https://codecov.io/gh/rpgrca/proyecto-ispc-fullstack
