Sistema de recomendación y exploración de películas mediante una interfaz de terminal.

El dominio elegido es sobre películas.

Elegimos este dominio porque las películas poseen numerosas características que permiten establecer relaciones entre ellas, como género, director, actores, año de estreno y valoración.

Además, el dominio resulta adecuado para desarrollar un sistema de recomendaciones, ya que una película puede utilizarse como punto de partida para encontrar otras similares o relacionadas.

Esta característica permitirá que, a medida que avance el proyecto, se puedan incorporar distintos algoritmos para resolver problemas concretos del sistema.

Actualmente, una persona que quiere ver una película puede encontrarse con una gran cantidad de opciones y no saber cuál elegir.(Nos pasa)

TARSbot busca resolver este problema permitiendo buscar películas, explorar categorías, consultar rankings y obtener recomendaciones a partir de una película que ya le haya gustado al usuario.

Por ejempPara la primera versión de TARSbot se proponen las siguientes cinco funcionalidades:

1- Buscar película

Permitir al usuario buscar una película mediante su título y consultar su información básica.

Ejemplo:

Ingrese el título: Interstellar

Película encontrada:
Título: Interstellar
Año: 2014
Género: Ciencia ficción
Rating: 8.7
2-Explorar películas por género

Permitir al usuario seleccionar un género y visualizar las películas correspondientes.

Ejemplo:

Seleccione un género:

1. Ciencia ficción
2. Acción
3. Drama
4. Comedia
5. Terror

Opción: 1

Películas de Ciencia ficción:

- Interstellar
- Inception
- Matrix
- Blade Runner 2049
3. consultar el Top 10

Mostrar las diez películas mejor valoradas del catálogo.

Ejemplo:

======== TOP 10 ========

1. The Shawshank Redemption   9.3
2. The Godfather              9.2
3. The Dark Knight            9.0
4...
5...

Esta funcionalidad permitirá posteriormente incorporar una estructura de prioridad para obtener eficientemente los elementos con mayor valoración.

4. Consultar películas relacionadas

Permitir seleccionar una película y obtener otras películas relacionadas con ella.

Las relaciones podrán basarse en características del dominio, como géneros, actores, director u otros criterios definidos durante el desarrollo.

Ejemplo:

Película seleccionada: Interstellar

Películas relacionadas:
...         