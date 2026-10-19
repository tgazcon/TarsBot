¿Qué tan rápido es?

En esta parte del proyecto elegimos como operación crítica la búsqueda de una película por título, ya que es una de las funciones principales de TARSbot. El usuario puede ingresar el nombre de una película y el sistema busca si se encuentra dentro del catálogo.

Para realizar esta búsqueda utilizamos dos estrategias diferentes: la búsqueda secuencial y la búsqueda mediante un árbol binario de búsqueda equilibrado.

La búsqueda secuencial recorre la lista de películas una por una hasta encontrar el título buscado. Si encuentra la película, la devuelve, y si llega al final de la lista sin encontrarla, significa que no está en el catálogo. Es una forma sencilla de realizar la búsqueda, pero cuanto mayor sea la cantidad de películas, más elementos puede tener que recorrer.

En este caso, el mejor caso es Ω(1), porque la película puede estar en la primera posición. El caso promedio es Θ(n), porque normalmente se debe recorrer una parte de la lista. El peor caso es O(n), porque la película puede estar al final o no encontrarse.

La segunda estrategia utiliza un árbol binario de búsqueda. Para construirlo, las películas se ordenan por título y se van colocando de manera equilibrada. Al buscar una película, el programa compara el título y decide si debe continuar por la izquierda o por la derecha. De esta forma no necesita revisar todas las películas una por una.

En un árbol equilibrado, el mejor caso es Ω(1), cuando la película se encuentra directamente en la raíz. El caso promedio es Θ(log n) y el peor caso es O(log n).

Para comparar ambas estrategias realizamos pruebas con 100, 1.000 y 10.000 películas. Los tiempos se midieron utilizando el archivo `prueba_complejidad.py` y la función `time.perf_counter()`.

Los resultados obtenidos fueron:

| Cantidad de películas | Búsqueda secuencial | Búsqueda en árbol |
|---|---:|---:|
| 100 | 0,0095 ms | 0,0033 ms |
| 1.000 | 0,0809 ms | 0,0028 ms |
| 10.000 | 0,8287 ms | 0,0046 ms |

Los tiempos pueden variar dependiendo de la computadora donde se realice la prueba. A partir de los resultados podemos observar que la búsqueda secuencial tarda más a medida que aumenta la cantidad de películas. En cambio, la búsqueda en árbol mantiene tiempos bajos porque puede descartar una gran cantidad de elementos en cada comparación.

Esto también coincide con la complejidad teórica. La búsqueda secuencial tiene una complejidad O(n) en el peor caso, mientras que la búsqueda en un árbol equilibrado tiene una complejidad O(log n).

Las dos estrategias permiten realizar la búsqueda de películas, pero cada una tiene sus características. La búsqueda secuencial es más sencilla y puede ser suficiente para un catálogo pequeño. La búsqueda en árbol necesita una estructura adicional, pero puede ser conveniente cuando el catálogo es más grande y se realizan muchas búsquedas.

Con esta comparación podemos observar que una misma necesidad puede resolverse de diferentes maneras y que la elección de la estrategia puede influir en el tiempo que tarda el programa.

Uso del árbol en la versión 2 de la app

A partir de esta comparación, en la versión 2 de TARSbot el árbol pasó a usarse en la aplicación. Al iniciar, el programa carga las películas y arma el árbol equilibrado una sola vez. Construirlo cuesta O(n log n), pero ese costo se paga al principio y después cada búsqueda cuesta O(log n).

La opción 1 (buscar película) y la opción 4 (películas relacionadas) buscan el título en el árbol en lugar de recorrer la lista.

Además se agregó la opción 5, que muestra el catálogo completo ordenado de la A a la Z. Para eso se usa el recorrido inorder del árbol, que visita el subárbol izquierdo, después el nodo y por último el subárbol derecho. Como el árbol está ordenado por título, este recorrido devuelve las películas ya ordenadas en O(n), sin tener que ordenar la lista cada vez.

El árbol también tiene los recorridos preorder (primero el nodo, después los hijos) y postorder (primero los hijos, después el nodo). El funcionamiento de los tres recorridos y de la búsqueda se verifica con las pruebas automáticas de `tests/test_arbol.py`.
