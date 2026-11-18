# Explorá la red: BFS y DFS

En la versión 5 armamos el grafo de películas: cada película es un vértice y dos películas están conectadas si se parecen (ver [10-Grafo.md](10-Grafo.md)). En esta versión agregamos los dos recorridos clásicos de grafos, la búsqueda en anchura (BFS) y la búsqueda en profundidad (DFS), y los usamos para responder dos preguntas reales sobre el catálogo. Los dos están en [servicios/grafo.py](../servicios/grafo.py).

## Qué hace cada algoritmo

### BFS: búsqueda en anchura

BFS arranca en una película y recorre el grafo **por niveles**. Primero visita todas las películas conectadas directamente (a 1 salto), después las conectadas a esas (a 2 saltos), y así hasta que no queda nada nuevo.

Para respetar ese orden usa una **cola** (FIFO). Cada película que descubre se pone al final de la cola, y siempre se procesa la que está primera, que es la más vieja. Con un conjunto de visitados se evita meter dos veces la misma película.

```
bfs(origen):
    distancia[origen] = 0
    cola = [origen]
    mientras la cola no esté vacía:
        actual = sacar el primero de la cola
        para cada vecino de actual:
            si vecino no fue visitado:
                distancia[vecino] = distancia[actual] + 1
                padre[vecino] = actual
                agregar vecino al final de la cola
```

Como recorre por niveles, la primera vez que BFS llega a una película lo hace por el camino con **menos saltos**. Por eso `distancia` guarda la distancia mínima a cada película, y `padre` permite reconstruir el camino más corto. El `camino_mas_corto` de la versión 5 ahora usa este mismo BFS.

### DFS: búsqueda en profundidad

DFS también arranca en una película, pero en lugar de avanzar por niveles **sigue una rama hasta el final**. Va de una película a una vecina, de esa a otra vecina, y solo cuando llega a una película sin vecinos nuevos vuelve atrás (backtracking) para probar la siguiente rama.

Para eso usa una **pila** (LIFO). En nuestra implementación la pila es la de las llamadas recursivas: cada llamada a `_dfs` visita una película y se llama a sí misma con el primer vecino no visitado.

```
dfs(actual, profundidad):
    marcar actual como visitado
    anotar (actual, profundidad)
    para cada vecino de actual:
        si vecino no fue visitado:
            dfs(vecino, profundidad + 1)
```

La profundidad que devuelve es el nivel dentro del **árbol de exploración** de DFS, no la distancia mínima. Por ejemplo, desde Matrix, The Dark Knight queda a profundidad 4 en DFS (Matrix → Blade Runner 2049 → Inception → Interstellar → The Dark Knight) aunque está a solo 2 saltos, porque DFS llegó a ella por un camino largo.

### Orden de los vecinos

En los dos recorridos los vecinos se visitan **de la conexión más fuerte a la más débil** (mayor afinidad primero) y, si empatan, por título. Así el resultado no depende del orden en que se cargó el JSON, y en DFS la exploración sigue primero la recomendación más parecida.

## Las dos consultas

Las dos están en la opción 7 del menú, **Red de películas**.

### Consulta con BFS: grados de separación

> ¿Qué tan lejos está cada película de The Matrix?

La opción 3 agrupa todas las películas alcanzables según la cantidad de saltos que las separan del origen (función `grados_de_separacion` en [servicios/catalogo.py](../servicios/catalogo.py)).

```
Grados de separación desde The Matrix

A 1 salto (3):
- Blade Runner 2049
- Inception
- Interstellar

A 2 saltos (2):
- The Dark Knight
- The Prestige

A 3 saltos (16):
- Avengers: Endgame
- Gladiator
- Saving Private Ryan
- ...

A 4 saltos (1):
- Se7en

A 5 saltos (3):
- Get Out
- The Silence of the Lambs
- It
```

**Por qué BFS:** la pregunta es por la distancia mínima en saltos, y eso es justamente lo que BFS calcula. El nivel en el que BFS descubre una película es su distancia al origen. Las del primer nivel son las relacionadas más cercanas a Matrix. Las de niveles más altos son películas que no se parecen a Matrix pero a las que se llega encadenando parecidos. Por ejemplo, Se7en no comparte nada con Matrix y está a 4 saltos.

DFS no sirve para esta consulta: puede llegar a una película por un camino largo y daría una distancia equivocada. Las pruebas verifican que la distancia de cada película coincide con el largo de su camino más corto.

### Consulta con DFS: explorar en profundidad

> Si empiezo por The Matrix y sigo siempre la recomendación más parecida, ¿a dónde llego? ¿Y a qué películas no puedo llegar nunca?

La opción 4 muestra la cadena de recomendaciones como un árbol con sangría y, al final, las películas que quedaron afuera (función `explorar_en_profundidad`).

```
Exploración en profundidad desde The Matrix

The Matrix
   └─ Blade Runner 2049
      └─ Inception
         └─ Interstellar
            └─ The Dark Knight
               └─ Avengers: Endgame
                  └─ Gladiator
                     └─ Saving Private Ryan
                        └─ ...
                                             └─ Se7en
                                                └─ Get Out
                                                   └─ The Silence of the Lambs
                                                      └─ It

Se llega a 25 películas.
No se puede llegar a (4): Coco, The Lord of the Rings: The Fellowship of the Ring, The Lord of the Rings: The Return of the King, Toy Story
```

**Por qué DFS:**
- **Recorrido en forma de cadena:** la pregunta es por un recorrido que sigue una cadena de recomendaciones ("de esta paso a la más parecida, de esa a la más parecida…") y vuelve atrás solo cuando se agota. Ese es exactamente el orden de DFS, y la sangría muestra las ramas y los puntos donde volvió atrás.
- **Lo que no se alcanza:** las películas que DFS nunca visita son las que no tienen ninguna conexión con Matrix, ni directa ni indirecta. Coco y Toy Story forman un grupo propio, igual que las dos de El Señor de los Anillos. Para saber qué se alcanza alcanza cualquiera de los dos recorridos, pero DFS es el más simple de escribir (unas pocas líneas recursivas) y no necesita una cola.

Desde una película aislada la exploración es corta:

```
Exploración en profundidad desde Coco

Coco
   └─ Toy Story

Se llega a 1 película.
No se puede llegar a (28): Avengers: Endgame, Blade Runner 2049, ...
```

## Complejidad

V es la cantidad de películas (vértices) y E la de conexiones (aristas). Con el catálogo actual, V = 30 y E = 118.

| | BFS | DFS |
|---|---|---|
| Tiempo | O(V + E) | O(V + E) |
| Memoria extra | O(V): cola, distancias y padres | O(V): visitados y pila de llamadas |

**Tiempo:** los dos visitan cada película una sola vez gracias al conjunto de visitados, y por cada película revisan su lista de vecinos. Como el grafo es no dirigido, cada arista aparece en la lista de sus dos extremos. En total se revisan 2E vecinos, así que el costo es O(V + E). Esto vale porque el grafo está guardado con **lista de adyacencia**. Con una matriz de adyacencia, encontrar los vecinos de cada película costaría recorrer una fila entera y los dos recorridos serían O(V²).

En nuestra implementación los vecinos se ordenan por afinidad antes de recorrerlos, lo que suma un factor logarítmico: O(V + E log g), donde g es el grado máximo. Con grados de entre 1 y 16 vecinos ese costo es despreciable, y si no importara el orden de visita se podría sacar.

**Memoria:**
- En el peor caso BFS tiene un nivel entero en la cola. Con Matrix el nivel más grande tiene 16 películas.
- DFS tiene en la pila la rama actual. Con Matrix la rama más larga llega a profundidad 21.
- Los dos son O(V) en el peor caso.
- Como DFS es recursivo, en un catálogo de miles de películas podría superar el límite de recursión de Python (unas 1.000 llamadas). En ese caso habría que escribirlo con una pila explícita, sin cambiar la complejidad.

## Diferencias y cuándo conviene cada uno

| | BFS | DFS |
|---|---|---|
| Estructura auxiliar | Cola (FIFO) | Pila (LIFO), en nuestro caso la recursión |
| Orden de visita | Por niveles: todo lo que está a 1 salto, después a 2… | Por ramas: llega al fondo de una rama antes de pasar a la siguiente |
| Camino más corto en saltos | Sí, la primera vez que llega a una película es por el camino más corto | No, puede llegar por un camino largo |
| Forma del recorrido | Ancho y bajo | Angosto y profundo |
| Implementación | Iterativa con cola | Recursiva, muy corta |
| Conviene para | Distancias mínimas, camino más corto, "lo más cercano a…", vecinos hasta cierta distancia | Explorar todo lo alcanzable, componentes conexas, detectar ciclos, seguir cadenas, backtracking |

Con el ejemplo de la consigna se ve la diferencia en el orden. En ese grafo Matrix se conecta con Inception y Terminator, Inception con Interstellar y Terminator con Alien:

```
BFS desde Matrix:  Matrix, Inception, Terminator, Interstellar, Alien
DFS desde Matrix:  Matrix, Inception, Interstellar, Terminator, Alien
```

Los dos visitan las mismas cinco películas. BFS termina el nivel 1 (Inception y Terminator) antes de bajar al 2, mientras que DFS termina la rama de Inception (hasta Interstellar) antes de pasar a Terminator.

**En resumen:**
- Si la pregunta es **"qué tan cerca"**, conviene BFS: la película relacionada más cercana, el camino con menos saltos o las películas a cierta distancia.
- Si la pregunta es **"hasta dónde llego"** o **"por dónde sigue"**, conviene DFS: explorar todo lo alcanzable, encontrar grupos aislados o seguir una cadena.

## Pruebas

```bash
python -m unittest -v
```

[tests/test_grafo.py](../tests/test_grafo.py) verifica:

- El orden exacto de BFS y de DFS sobre el grafo de la consigna. Visitan las mismas películas en distinto orden, y Coco, que está aislada, no aparece.
- Los recorridos desde una película aislada y desde una que no existe.
- Con el catálogo real:
  - El primer nivel de los grados de separación son exactamente los vecinos de Matrix.
  - La distancia de cada película coincide con el largo de su camino más corto.
  - DFS arranca por la conexión más fuerte (Blade Runner 2049).
  - Las películas alcanzadas más las no alcanzadas suman todo el catálogo.
