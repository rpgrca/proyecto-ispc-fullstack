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

En algunos sistemas (por ejemplo Linux Ubuntu) es _python3_ y _pip3_, en otros _python_ y _pip_. La versión mínima es 3.9. En otros sistemas como las variantes de SUSE python3 es Python 3.6 por lo que hay que instalar primero una versión más moderna, por ejemplo con _sudo zypper install python310-base_ y luego utilizar _python3.10_ en lugar de _python3_.

![image](https://user-images.githubusercontent.com/15602473/201264090-09e4e986-26aa-4809-9f9e-64ade8aaa3e1.png)

### Ejecutar servidor
Para levantar el servidor del back-end desde una consola o shell dentro de dicho directorio:
```
python main.py
```
(o _python3 main.py_ en algunas distribuciones de Linux). El servidor utiliza el puerto 8000. También es posible ejecutarlo de la siguiente manera:
```
uvicorn main:app
```

![image](https://user-images.githubusercontent.com/15602473/201264171-16ecb154-c388-421f-83e5-4328b31ffe4b.png)

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

![image](https://user-images.githubusercontent.com/15602473/201264210-37ab8560-078a-4aaf-923a-3e63ff3a6fa2.png)

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
- [Diagramas de casos de uso](https://github.com/rpgrca/proyecto-ispc-fullstack/wiki/Diagrama-de-casos-de-uso)

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
