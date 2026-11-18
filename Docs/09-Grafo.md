# grafo de películas

Las películas se relacionan entre sí (comparten género, subgénero o director), y esa relación se modela mejor como una red que como una lista o un árbol.

Los pesos son los mismos de las recomendaciones de la versión 4 (función `afinidad` en [servicios/catalogo.py](../servicios/catalogo.py)). Por ejemplo, Inception e Interstellar son de ciencia ficción y del mismo director, así que la arista pesa 2,0. Inception y The Matrix solo comparten género y pesa 1,0.

- No dirigido: que Inception se parezca a Interstellar es lo mismo que decir que Interstellar se parece a Inception. La relación es simétrica, así que una sola arista alcanza para los dos sentidos.
- Pesado: no todas las relaciones valen lo mismo. Dos películas del mismo género y director están más cerca que dos que solo comparten género, y el peso permite ordenar las conexiones de la más fuerte a la más débil.
- Lista de adyacencia: cada película guarda solo sus vecinos y el peso de cada conexión. La memoria es O(V + E) y listar los vecinos cuesta lo que vale su grado, que es lo que más se consulta (conexiones y caminos).

La densidad esperada del grafo es baja a media. Con las 30 películas hay 118 aristas de las 435 posibles, un 27%. En un catálogo más grande con más géneros, subgéneros y directores, la densidad baja todavía más, porque cada película se parece a una parte cada vez más chica del total. Una matriz de adyacencia usaría V² celdas (900 hoy, un millón con 1.000 películas) y para listar los vecinos de una película habría que recorrer una fila entera. La matriz solo conviene en un grafo denso o cuando se pregunta mucho si dos vértices puntuales están conectados, y acá no es el caso.

## Operaciones

V es la cantidad de películas y E la de conexiones.

| Operación                           |      Qué hace                        |   Costo              |
|                                  ---|                                   ---|                   ---|
| `agregar_vertice`, `agregar_arista` | Agrega una película o una conexión   |    O(1)              |
| `vecinos(titulo)` | Películas conectadas, de mayor a menor peso            | O(grado log grado)   |
| `camino_mas_corto(origen, destino)` | Camino con menos saltos, con búsqueda en anchura | O(V + E) |

`crear_grafo` compara todos los pares de películas, O(n²). Con 30 películas son 435 comparaciones; para un catálogo grande habría que agrupar antes por género y por director.

## Ejemplos de consultas

Las dos consultas están en la opción 7 del menú, **Red de películas**.

Conexiones de una película:

```
Conexiones de Inception (5)
- Interstellar                                         2.0
- Blade Runner 2049                                    1.0
- The Dark Knight                                      1.0
- The Matrix                                           1.0
- The Prestige                                         1.0
```

Camino entre dos películas, que no comparten nada de forma directa:

```
The Matrix -> Interstellar -> The Dark Knight -> Gladiator
(3 saltos)
```

Matrix e Interstellar son de ciencia ficción, Interstellar y The Dark Knight son del mismo director (Nolan), y The Dark Knight y Gladiator son de acción.

Con Coco y Toy Story pasa algo distinto: solo se parecen entre sí, así que forman un grupo aislado.

```
Coco -> Toy Story
(1 salto)

Coco -> The Matrix: No hay camino entre esas películas.
```

Lo mismo le pasa a las dos películas de El Señor de los Anillos. Esto es algo que la lista de películas relacionadas no mostraba y que el grafo deja ver.

## Pruebas

```bash
python -m unittest -v
```

[tests/test_grafo.py](../tests/test_grafo.py) usa el grafo de ejemplo de la consigna (Matrix, Inception, Terminator, Interstellar y Alien) para verificar que no es dirigido, el camino más corto y los casos sin camino, y con el catálogo real verifica que el peso es la afinidad.
