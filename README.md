[![contrib][contrib-img]][contrib-url]
[![commit][commit-img]][commit-url]
[![discuss][discuss-img]][discuss-url]
[![issues][issues-img]][issues-url]
[![Python package][pipeline-img]][pipeline-url]
[![codecov][codecov-img]][codecov-url]

# Proyecto Full-Stack ISPC

## Instalación
Instalar las dependencias (fastapi, pytest, etc) desde el directorio *back-end:*
```
python -m pip install -r requirements.txt
```

ó

```
pip install -r requirements.txt
```

En algunos sistemas (por ejemplo Linux Ubuntu) es _python3_ y _pip3_, en otros _python_ y _pip_. La versión mínima es 3.9.

### Ejecutar servidor
Para levantar el servidor del back-end desde una consola o shell dentro de dicho directorio:
```
python main.py
```
El servidor utiliza el puerto 8000. También es posible ejecutarlo de la siguiente manera:
```
uvicorn main:app
```

![image](https://user-images.githubusercontent.com/15602473/197442544-6658bf45-fadf-4aae-8e76-3dddb0835cb9.png)

Si se configura para ejecutar en MySQL creará la base de datos y las tablas necesarias si no existen.

### Ejecutar pruebas unitarias
Para ejecutar las pruebas unitarias desde una consola o shell desde dentro del directorio *back-end:*
```
pytest main_tests.py
```

Esto ejecutará todas las pruebas unitarias que se encuentren dentro del suite (que incluyen todas las del directorio _tests_). El pipeline utiliza una línea un poco más larga que también se puede utilizar manualmente:

```
pytest main_tests.py --cov-config=coverage.ini --doctest-modules --junitxml=main.coverage.xml --cov-append --cov . --cov-report xml --cov-report html
```

lo que genera un archivo *coverage.xml* con la información de cobertura y un archivo *main.coverage.xml* con información de pruebas ejecutadas en formato Junit.

![image](https://user-images.githubusercontent.com/15602473/197442599-4c2e61cc-db61-4c3a-9f20-0617e2b67513.png)

Para ejecutar las pruebas unitarias de a un módulo hay que adjuntar el PATH de los módulos por delante de la línea de comando, por ejemplo para ejecutar las pruebas del controlador de *usuario*:

```
PYTHONPATH=$PYTHONPATH:controller pytest tests/usuario_tests.py
```

![image](https://user-images.githubusercontent.com/15602473/199630504-dc9ad666-bca2-4f2b-a65c-bf34a2dfb664.png)

### Ejecutar pruebas de integración con Postman

En la sección de documentación se adjunta un archivo con pruebas de Postman para realizar. Las pruebas se realizan sobre una base vacía de MySQL.

![image](https://user-images.githubusercontent.com/15602473/199632889-6e69fe97-7183-48de-9362-689a7cbdd052.png)

## Información para el Sprint 1
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
