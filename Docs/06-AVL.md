# El árbol también puede enfermarse: BST vs AVL

El árbol de la versión 2 de TARSbot es un árbol binario de búsqueda (BST) que se arma ordenando las películas por título e insertando siempre la del medio. Eso lo deja equilibrado, pero solo porque lo construimos con cuidado. Un BST común no se reequilibra solo: la forma que toma depende del orden en que llegan los datos.

Si los títulos se insertan ya ordenados (por ejemplo alfabéticamente), cada título nuevo es mayor que todos los anteriores y siempre se cuelga a la derecha del último. El árbol deja de ser un árbol y pasa a ser una lista enlazada: la altura es n y buscar cuesta O(n), igual que la búsqueda secuencial.

## solución: AVL

Un árbol AVL es un BST que, después de cada inserción, controla el factor de balance de cada nodo: altura del subárbol izquierdo menos altura del derecho. Si un nodo llega a +2 o -2, lo corrige con rotaciones equilibrando el arbol. Así la diferencia de alturas entre los dos hijos de cualquier nodo nunca supera 1.

Hay cuatro casos de desbalance, que se resuelven con una o dos rotaciones:

| Caso                  | Cuándo pasa                                               | Corrección                                            |

| Izquierda-Izquierda   | Se insertó en el subárbol izquierdo del hijo izquierdo    | Rotación simple a la derecha                          |
| Derecha-Derecha       | Se insertó en el subárbol derecho del hijo derecho        | Rotación simple a la izquierda                        |
| Izquierda-Derecha     | Se insertó en el subárbol derecho del hijo izquierdo      | Rotación izquierda del hijo y luego derecha del nodo  |
| Derecha-Izquierda     | Se insertó en el subárbol izquierdo del hijo derecho      | Rotación derecha del hijo y luego izquierda del nodo  |

Una rotación solo cambia unos pocos punteros (O(1)) y conserva el orden de los títulos, por eso el recorrido inorder sigue devolviendo todo ordenado. Cada nodo guarda su altura, así que calcular el balance también es O(1).

## Experimentos

```bash
python prueba_avl.py
```

### 1. Títulos sintéticos en distinto orden

Se insertaron n títulos del estilo `Pelicula 00001` en orden ascendente, descendente y aleatorio, en un BST común y en un AVL. En los órdenes ascendente y descendente la búsqueda es del último título insertado; en el aleatorio, de uno del medio. Cada búsqueda se repitió 200 veces y se tomó el promedio.

| n     | Orden         | Altura BST | Altura AVL | Armado BST | Armado AVL | Búsqueda BST | Búsqueda AVL | Rotaciones AVL |

| 100   | ascendente    | 100        | 7  | 0,0005 s  | 0,0004 s | 10,87 µs  | 0,75 µs | 93   |
| 100   | descendente   | 100        | 7  | 0,0004 s  | 0,0003 s | 9,14 µs   | 0,73 µs | 93   |
| 100   | aleatorio     | 11         | 8  | 0,0001 s  | 0,0003 s | 0,62 µs   | 0,73 µs | 65   |
| 1.000 | ascendente    | 1000       | 10 | 0,0394 s  | 0,0043 s | 86,23 µs  | 1,01 µs | 990  |
| 1.000 | descendente   | 1000       | 10 | 0,0408 s  | 0,0045 s | 90,39 µs  | 1,03 µs | 990  |
| 1.000 | aleatorio     | 21         | 12 | 0,0012 s  | 0,0044 s | 0,78 µs   | 1,05 µs | 689  |
| 5.000 | ascendente    | 5000       | 13 | 0,9901 s  | 0,0264 s | 432,17 µs | 1,28 µs | 4987 |
| 5.000 | descendente   | 5000       | 13 | 0,9837 s  | 0,0268 s | 439,90 µs | 1,23 µs | 4987 |
| 5.000 | aleatorio     | 29         | 15 | 0,0075 s  | 0,0276 s | 1,27 µs   | 1,28 µs | 3379 |

Queremos destacar que los tiempos depende de cada maquina igualmente, debemos hacer foco a como evolucionan los tiempos.

### 2. El catálogo real

Las 30 películas de `datos/peliculas.json` insertadas en orden alfabético:

| Árbol | Altura | Pasos máximos para buscar |
|---|---:|---:|
| BST común | 30 | 30 |
| AVL | 5 | 5 |

La altura mínima posible para 30 nodos es 5, así que el AVL lo dejó perfecto. Para lograrlo hizo 25 rotaciones.

- Con datos ordenados el BST se degenera. La altura es igual a n (100, 1.000, 5.000) y la búsqueda crece de forma lineal: de 10 µs con 100 películas a 432 µs con 5.000, unas 40 veces más para 50 veces más datos. Es el comportamiento O(n).

- El AVL no se ve afectado por el orden de entrada. Con ascendente, descendente o aleatorio queda con alturas parecidas (7, 10, 13 para 100, 1.000 y 5.000 nodos). La búsqueda apenas cambia de 0,75 µs a 1,28 µs mientras los datos se multiplican por 50. Es el comportamiento O(log n).

- Con datos aleatorios el BST común anda bien. Su altura es chica y es incluso un poco más rápido de armar, porque no gasta tiempo en rotaciones. El AVL queda algo más bajo en altura pero la diferencia en búsqueda es mínima. El balance importa cuando no controlamos el orden de los datos.

## Por qué importa el balance

La búsqueda en un BST cuesta como mucho tanto como su altura h. Todo depende de cuánto vale h respecto de n:

| Árbol | Altura | Búsqueda |
|---|---|---|
| BST degenerado (lista) | n | O(n) |
| BST equilibrado | log₂ n | O(log n) |
| AVL | como máximo 1,44 · log₂(n + 2) | O(log n) garantizado |

Con un millón de películas, O(n) son hasta un millón de pasos y O(log n) son alrededor de 20. El BST común da O(log n) solo con suerte (datos en orden aleatorio) o si se construye con cuidado, como hacemos hoy con la mitad del arreglo ordenado. El AVL lo garantiza siempre, sin importar el orden de inserción, a cambio de guardar una altura por nodo y de hacer rotaciones, que son O(1) y a lo sumo dos por inserción. La inserción pasa a ser O(log n) en el peor caso, en vez de O(n).

## Conclusión técnica

Cuando el catálogo se carga por completo y no cambia, basta con construir el BST equilibrado desde la lista ordenada, como hace la versión 2, pero si en cambio se van agregando películas una por una, conviene usar un AVL: el costo extra de las rotaciones es chico y evita que la estructura degrade a una lista, que es exactamente el problema que el árbol tiende a resolver.

## Pruebas

```bash
python -m unittest -v
```
(En el desarrollo de este AVL nos apoyamos es un ejemplo de StackOverFlow y nos apoyamos un poco con IA ya para no retrasarnos.)

