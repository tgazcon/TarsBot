# El árbol también puede enfermarse: BST vs AVL

## El problema

El árbol de la versión 2 de TARSbot es un árbol binario de búsqueda (BST) que se arma ordenando las películas por título e insertando siempre la del medio. Eso lo deja equilibrado, pero solo porque lo construimos con cuidado. Un BST común no se reequilibra solo: la forma que toma depende del orden en que llegan los datos.

Si los títulos se insertan ya ordenados (por ejemplo alfabéticamente), cada título nuevo es mayor que todos los anteriores y siempre se cuelga a la derecha del último. El árbol deja de ser un árbol y pasa a ser una lista enlazada: la altura es n y buscar cuesta O(n), igual que la búsqueda secuencial.

## La solución: AVL

Un árbol AVL ([servicios/avl.py](../servicios/avl.py)) es un BST que, después de cada inserción, controla el **factor de balance** de cada nodo: altura del subárbol izquierdo menos altura del derecho. Si algún nodo llega a +2 o -2, lo corrige con rotaciones. Así la diferencia de alturas entre los dos hijos de cualquier nodo nunca supera 1.

Hay cuatro casos de desbalance, que se resuelven con una o dos rotaciones:

| Caso | Cuándo pasa | Corrección |
|---|---|---|
| Izquierda-Izquierda | Se insertó en el subárbol izquierdo del hijo izquierdo | Rotación simple a la derecha |
| Derecha-Derecha | Se insertó en el subárbol derecho del hijo derecho | Rotación simple a la izquierda |
| Izquierda-Derecha | Se insertó en el subárbol derecho del hijo izquierdo | Rotación izquierda del hijo y luego derecha del nodo |
| Derecha-Izquierda | Se insertó en el subárbol izquierdo del hijo derecho | Rotación derecha del hijo y luego izquierda del nodo |

Una rotación solo cambia unos pocos punteros (O(1)) y conserva el orden de los títulos, por eso el recorrido inorder sigue devolviendo todo ordenado. Cada nodo guarda su altura, así que calcular el balance también es O(1).

Ejemplo con el mini caso: insertar `A`, `B`, `C` en un BST da una cadena A → B → C. En el AVL, al insertar `C` el nodo `A` queda con balance -2 (caso Derecha-Derecha), se rota a la izquierda y queda `B` en la raíz con `A` y `C` como hijos.

## Experimentos

Se ejecutan con:

```bash
python prueba_avl.py
```

### 1. Títulos sintéticos en distinto orden

Se insertaron n títulos del estilo `Pelicula 00001` en orden ascendente, descendente y aleatorio, en un BST común y en un AVL. En los órdenes ascendente y descendente la búsqueda es del último título insertado; en el aleatorio, de uno del medio. Cada búsqueda se repitió 200 veces y se tomó el promedio.

| n | Orden | Altura BST | Altura AVL | Armado BST | Armado AVL | Búsqueda BST | Búsqueda AVL | Rotaciones AVL |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 100 | ascendente | 100 | 7 | 0,0005 s | 0,0004 s | 10,87 µs | 0,75 µs | 93 |
| 100 | descendente | 100 | 7 | 0,0004 s | 0,0003 s | 9,14 µs | 0,73 µs | 93 |
| 100 | aleatorio | 11 | 8 | 0,0001 s | 0,0003 s | 0,62 µs | 0,73 µs | 65 |
| 1.000 | ascendente | 1000 | 10 | 0,0394 s | 0,0043 s | 86,23 µs | 1,01 µs | 990 |
| 1.000 | descendente | 1000 | 10 | 0,0408 s | 0,0045 s | 90,39 µs | 1,03 µs | 990 |
| 1.000 | aleatorio | 21 | 12 | 0,0012 s | 0,0044 s | 0,78 µs | 1,05 µs | 689 |
| 5.000 | ascendente | 5000 | 13 | 0,9901 s | 0,0264 s | 432,17 µs | 1,28 µs | 4987 |
| 5.000 | descendente | 5000 | 13 | 0,9837 s | 0,0268 s | 439,90 µs | 1,23 µs | 4987 |
| 5.000 | aleatorio | 29 | 15 | 0,0075 s | 0,0276 s | 1,27 µs | 1,28 µs | 3379 |

Los tiempos dependen de la computadora; lo importante es cómo crecen.

### 2. El catálogo real

Las 30 películas de `datos/peliculas.json` insertadas en orden alfabético (el mini ejemplo de la consigna):

| Árbol | Altura | Pasos máximos para buscar |
|---|---:|---:|
| BST común | 30 | 30 |
| AVL | 5 | 5 |

La altura mínima posible para 30 nodos es 5, así que el AVL lo dejó perfecto. Para lograrlo hizo 25 rotaciones.

## Qué muestran los resultados

- **Con datos ordenados el BST se degenera.** La altura es igual a n (100, 1.000, 5.000) y la búsqueda crece de forma lineal: de 10 µs con 100 películas a 432 µs con 5.000, unas 40 veces más para 50 veces más datos. Es el comportamiento O(n).
- **El AVL no se ve afectado por el orden de entrada.** Con ascendente, descendente o aleatorio queda con alturas parecidas (7, 10, 13 para 100, 1.000 y 5.000 nodos). La búsqueda apenas cambia de 0,75 µs a 1,28 µs mientras los datos se multiplican por 50. Es el comportamiento O(log n).
- **Construir también se resiente.** Insertar n títulos ordenados en un BST cuesta O(n²) porque cada inserción recorre toda la cadena: 0,99 s con 5.000 películas contra 0,026 s del AVL, que cuesta O(n log n).
- **Con datos aleatorios el BST común anda bien.** Su altura es chica (11, 21, 29) y es incluso un poco más rápido de armar, porque no gasta tiempo en rotaciones. El AVL queda algo más bajo en altura teórica pero la diferencia en búsqueda es mínima. El balance importa cuando no controlamos el orden de los datos.

## Por qué importa el balance

La búsqueda en un BST cuesta como mucho tanto como su altura h. Todo depende de cuánto vale h respecto de n:

| Árbol | Altura | Búsqueda |
|---|---|---|
| BST degenerado (lista) | n | O(n) |
| BST equilibrado | log₂ n | O(log n) |
| AVL | como máximo 1,44 · log₂(n + 2) | O(log n) garantizado |

Con un millón de películas, O(n) son hasta un millón de pasos y O(log n) son alrededor de 20. El BST común da O(log n) solo con suerte (datos en orden aleatorio) o si se construye con cuidado, como hacemos hoy con la mitad del arreglo ordenado. El AVL lo garantiza siempre, sin importar el orden de inserción, a cambio de guardar una altura por nodo y de hacer rotaciones, que son O(1) y a lo sumo dos por inserción. La inserción pasa a ser O(log n) en el peor caso, en vez de O(n).

## Conclusión técnica

Cuando el catálogo se carga completo y no cambia, alcanza con construir el BST equilibrado desde la lista ordenada, como hace la versión 2. Si en cambio se van agregando películas una por una, y más aún si pueden llegar ordenadas, conviene usar un AVL: el costo extra de las rotaciones es chico y evita que la estructura degrade a una lista, que es exactamente el problema que el árbol venía a resolver.

## Pruebas

```bash
python -m unittest -v
```

[tests/test_avl.py](../tests/test_avl.py) verifica las cuatro rotaciones sobre ejemplos de tres nodos (forma del árbol y cantidad de rotaciones), que después de insertar 1.000 títulos en orden ascendente, descendente y aleatorio todos los nodos tienen balance entre -1 y 1 y su altura guardada es correcta, que la altura queda por debajo de 1,45 · log₂(n + 2), que el recorrido inorder sale ordenado, y que con el catálogo real el BST llega a altura 30 y el AVL a 5 con los mismos resultados de búsqueda.
