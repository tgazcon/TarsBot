# Casos de uso

TARSbot es un sistema de recomendación y exploración de películas que se usa desde una terminal. El único actor es el **usuario**: una persona aficionada al cine que tiene dificultades para decidir qué película ver y no necesita saber cómo funciona el programa por dentro.

Al iniciar, el programa carga el catálogo (30 películas) y arma las estructuras de datos. Después muestra el menú principal y lo repite hasta que el usuario elige Salir. Si se ingresa una opción que no existe, muestra "Opción inválida." y vuelve a pedirla.

```
===== TARSbot =====
1. Buscar película
2. Explorar por género
3. Top 10 películas
4. Películas relacionadas
5. Catálogo completo (A-Z)
6. Explorar categorías
7. Red de películas
8. Salir
```

| Caso de uso | Opción | Qué resuelve | Estructura de datos |
|---|---|---|---|
| CU1 Buscar película | 1 | Consultar los datos de una película por su título | Árbol binario de búsqueda |
| CU2 Explorar por género | 2 | Ver las películas de un género | Lista |
| CU3 Consultar el Top 10 | 3 | Ver las películas mejor valoradas | Heap |
| CU4 Obtener recomendaciones | 4 | Encontrar películas parecidas a una que ya gustó | Heap y árbol binario de búsqueda |
| CU5 Ver el catálogo completo | 5 | Ver todas las películas de la A a la Z | Árbol binario de búsqueda |
| CU6 Explorar categorías | 6 | Recorrer la jerarquía de géneros y subgéneros | Árbol general |
| CU7 Explorar la red de películas | 7 | Ver cómo se conectan las películas entre sí | Grafo, BFS y DFS |
| CU8 Salir | 8 | Terminar el programa | |

En todos los casos que piden un título, no se distinguen mayúsculas de minúsculas.

## CU1. Buscar película

**Objetivo:** consultar la información de una película a partir de su título.

**Flujo:**
1. El usuario elige la opción 1.
2. Ingresa el título.
3. El sistema muestra título, director, año, género (con su subgénero si tiene) y valoración.

**Alternativa:** si el título no existe, el sistema muestra "No se encontró la película."

```
Ingrese el título: Interstellar
Título: Interstellar
Director: Christopher Nolan
Año: 2014
Género: Ciencia ficción / Exploración espacial
Valoración: 8.7
```

## CU2. Explorar por género

**Objetivo:** ver todas las películas de un género.

**Flujo:**
1. El usuario elige la opción 2.
2. Ingresa el género (Acción, Animación, Ciencia ficción, Drama, Fantasía o Terror).
3. El sistema lista los títulos de ese género.

**Alternativa:** si el género no existe, el sistema no muestra ninguna película.

```
Ingrese el género: Ciencia ficción
- Interstellar
- Inception
- The Matrix
- Blade Runner 2049
```

## CU3. Consultar el Top 10

**Objetivo:** ver las diez películas mejor valoradas del catálogo.

**Flujo:**
1. El usuario elige la opción 3.
2. El sistema obtiene las diez de mayor valoración con una heap y las muestra de mayor a menor.

```
======== TOP 10 ========
1. The Shawshank Redemption                 9.3
2. The Godfather                            9.2
3. The Dark Knight                          9.0
...
```

## CU4. Obtener recomendaciones

**Objetivo:** encontrar películas parecidas a una que el usuario ya vio y le gustó.

**Flujo:**
1. El usuario elige la opción 4.
2. Ingresa el título de la película de referencia.
3. El sistema toma las películas que comparten género o director con ella y las ordena con una heap por un puntaje. El puntaje es la valoración más un bonus por parecido: +1,0 por mismo género, +0,5 por mismo subgénero y +1,0 por mismo director.
4. Muestra las cinco de mayor puntaje.

**Alternativa:** si el título no existe, el sistema muestra "No se encontró la película."

```
Ingrese el título: Interstellar

======== TOP 5 PARA INTERSTELLAR ========
1. Inception                                10.8
2. The Dark Knight                          10.0
3. The Matrix                               9.7
4. The Prestige                             9.5
5. Blade Runner 2049                        9.0
```

## CU5. Ver el catálogo completo

**Objetivo:** ver todas las películas ordenadas alfabéticamente.

**Flujo:**
1. El usuario elige la opción 5.
2. El sistema recorre el árbol binario de búsqueda en inorder, que devuelve los títulos ya ordenados, y los muestra con su año de estreno.

```
===== CATÁLOGO (A-Z) =====
- Avengers: Endgame                                    2019
- Blade Runner 2049                                    2017
- Coco                                                 2017
...
```

## CU6. Explorar categorías

**Objetivo:** recorrer la jerarquía de la forma Películas, género y subgénero.

**Flujo:**
1. El usuario elige la opción 6 y se abre un submenú.
2. Elige una de las tres acciones:
   - **1. Ver el árbol de categorías:** muestra la jerarquía completa con la cantidad de películas de cada categoría.
   - **2. Ver las películas de una categoría:** pide el nombre de una categoría (un género o un subgénero) y lista sus películas, incluyendo las de sus subcategorías.
   - **3. ¿En qué categoría está una película?:** pide un título y muestra la ruta de categorías donde está.
3. Con la opción 4 vuelve al menú principal.

**Alternativa:** si la categoría o la película no existen, el sistema muestra "No se encontró la categoría." o "No se encontró la película."

```
Ingrese la categoría: Cyberpunk

Películas > Ciencia ficción > Cyberpunk (2)
- Blade Runner 2049                                    2017
- The Matrix                                           1999
```

## CU7. Explorar la red de películas

**Objetivo:** ver cómo se conectan las películas entre sí. Dos películas están conectadas si comparten género o director, y la conexión es más fuerte cuanto más comparten.

**Flujo:**
1. El usuario elige la opción 7 y se abre un submenú.
2. Elige una de las cuatro acciones:
   - **1. Ver las conexiones de una película:** pide un título y lista las películas conectadas, de la conexión más fuerte a la más débil.
   - **2. Camino entre dos películas:** pide una película de origen y una de destino, y muestra el camino con menos saltos (búsqueda en anchura).
   - **3. Grados de separación (BFS):** pide un título y agrupa todas las películas alcanzables según a cuántos saltos están.
   - **4. Explorar en profundidad (DFS):** pide un título y sigue cada rama de conexiones hasta el final, mostrando también a cuáles películas no se puede llegar.
3. Con la opción 5 vuelve al menú principal.

**Alternativas:**
- Si una película no existe, el sistema muestra "No se encontró la película." (o "No se encontró alguna de las películas." en el camino).
- Si no hay camino entre dos películas, muestra "No hay camino entre esas películas." Por ejemplo, Coco y Toy Story solo se parecen entre sí, así que no se conectan con el resto.

```
Película de origen: The Matrix
Película de destino: Gladiator
The Matrix -> Inception -> The Dark Knight -> Gladiator
(3 saltos)
```

## CU8. Salir

**Objetivo:** terminar el programa.

**Flujo:** el usuario elige la opción 8 y el sistema muestra "Fin de TarsBot".
