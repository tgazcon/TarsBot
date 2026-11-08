# Que el sistema elija primero: cola de prioridad con heap

El bonus de las recomendaciones (`puntaje_recomendacion` en [servicios/catalogo.py](../servicios/catalogo.py)):

Se eligió combinar factores porque la valoración sola recomendaría siempre las mismas películas muy valoradas, sin importar cuál le gustó al usuario. Con el bonus, una película de la misma saga o del mismo director sube en el ranking aunque tenga menos rating. Los pesos son una decisión de diseño y se cambian en un solo lugar (`PESO_GENERO`, `PESO_SUBGENERO` y `PESO_DIRECTOR`).

Las candidatas son las películas relacionadas (mismo género o mismo director que la elegida). El puntaje puede pasar de 10 porque suma el bonus a la valoración.

## La heap

Una heap binaria de máximos es un árbol binario completo guardado en una lista donde cada nodo tiene más prioridad que sus hijos, así el máximo siempre está en la posición 0. Para el nodo `i`, el padre está en `(i - 1) // 2` y los hijos en `2i + 1` y `2i + 2`, por lo que no hacen falta punteros.

Cuando dos películas tienen la misma prioridad sale primero la que entró antes, así los empates tienen un orden estable y predecible.

## Top-N

top_n construye la heap con todas las películas y extrae las N primeras.

## Por qué una heap y no ordenar todo cada vez

- Ordenar hace más trabajo del necesario. Ordenar todo el catálogo cuesta O(n log n) y sirve para obtener las 5 mejores, cuando el resto no se muestra. La heap paga O(n) una vez y después solo O(log n) por cada película que realmente se pide. Con un millón de películas y un Top 10, son alrededor de un millón de pasos más 200, contra unos veinte millones.

- El ranking de recomendaciones es distinto para cada película. La prioridad depende de cuál eligió el usuario, así que no existe una única lista ordenada que se pueda guardar y reutilizar: habría que reordenar en cada consulta. Con la heap cada consulta se arma sobre las candidatas y se paga solo lo que se muestra.

- El ranking es dinámico. Si entra una película nueva o cambia una valoración, la heap se actualiza insertando en O(log n). Una lista ordenada hay que reordenarla entera, O(n log n), cada vez.

## Pruebas

```bash
python -m unittest -v
```

[tests/test_heap.py](../tests/test_heap.py) verifica que la heap extrae de mayor a menor, el desempate por orden de entrada, la construcción desde una lista, el caso vacío, que el Top 10 coincide con ordenar la lista, y que el ranking de recomendaciones está ordenado y no incluye a la película elegida.
