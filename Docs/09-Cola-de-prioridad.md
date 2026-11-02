# Que el sistema elija primero: cola de prioridad con heap

## Qué se resuelve

TARSbot necesita rankings: el Top 10 del catálogo y las mejores recomendaciones a partir de una película. En los dos casos hace falta lo mismo: obtener los N elementos de mayor prioridad. Para eso se implementó una **heap binaria de máximos** a mano ([servicios/heap.py](../servicios/heap.py)).

## Función de prioridad

La prioridad cambia según lo que se pregunta:

| Consulta | Prioridad |
|---|---|
| Top 10 del catálogo | La valoración |
| Recomendaciones para una película | La valoración más un bonus por parecido con la película elegida |

El bonus de las recomendaciones (`puntaje_recomendacion` en [servicios/catalogo.py](../servicios/catalogo.py)):

| Factor | Bonus |
|---|---:|
| Mismo género | +1,0 |
| Mismo subgénero | +0,5 |
| Mismo director | +1,0 |

Se eligió combinar factores porque la valoración sola recomendaría siempre las mismas películas muy valoradas, sin importar cuál le gustó al usuario. Con el bonus, una película de la misma saga o del mismo director sube en el ranking aunque tenga menos rating. Los pesos son una decisión de diseño y se cambian en un solo lugar (`PESO_GENERO`, `PESO_SUBGENERO` y `PESO_DIRECTOR`).

Las candidatas son las películas relacionadas (mismo género o mismo director que la elegida). El puntaje puede pasar de 10 porque suma el bonus a la valoración.

## La heap

Una heap binaria de máximos es un árbol binario completo guardado en una lista donde cada nodo tiene más prioridad que sus hijos, así el máximo siempre está en la posición 0. Para el nodo `i`, el padre está en `(i - 1) // 2` y los hijos en `2i + 1` y `2i + 2`, por lo que no hacen falta punteros.

| Operación | Cómo funciona | Costo |
|---|---|---|
| `insertar` | Se agrega al final y se sube intercambiando con el padre mientras tenga más prioridad | O(log n) |
| `ver_maximo` | Devuelve la posición 0 | O(1) |
| `extraer_maximo` | Se saca la raíz, se pone el último en su lugar y se baja intercambiando con el hijo mayor | O(log n) |
| `construir` | Se llena la lista y se baja cada nodo interno de abajo hacia arriba | O(n) |

Cuando dos películas tienen la misma prioridad sale primero la que entró antes, así los empates tienen un orden estable y predecible.

## Top-N

`top_n` ([servicios/catalogo.py](../servicios/catalogo.py)) construye la heap con todas las películas y extrae las N primeras. Cuesta **O(n + N log n)**. Con el Top 10 y las recomendaciones de la terminal, N es 10 y 5.

## Por qué una heap y no ordenar todo cada vez

- **Ordenar hace más trabajo del necesario.** Ordenar todo el catálogo cuesta O(n log n) y sirve para obtener las 5 mejores, cuando el resto no se muestra. La heap paga O(n) una vez y después solo O(log n) por cada película que realmente se pide. Con un millón de películas y un Top 10, son alrededor de un millón de pasos más 200, contra unos veinte millones.
- **El ranking de recomendaciones es distinto para cada película.** La prioridad depende de cuál eligió el usuario, así que no existe una única lista ordenada que se pueda guardar y reutilizar: habría que reordenar en cada consulta. Con la heap cada consulta se arma sobre las candidatas y se paga solo lo que se muestra.
- **El ranking es dinámico.** Si entra una película nueva o cambia una valoración, la heap se actualiza insertando en O(log n). Una lista ordenada hay que reordenarla entera, O(n log n), cada vez.

Con 30 películas cualquier enfoque es instantáneo, y `sorted` de Python está escrito en C y es muy difícil de superar para tamaños chicos. La ventaja de la heap es cómo escala cuando el catálogo crece o el ranking cambia seguido.

## Ejemplo

Salida de la opción 4 con "Interstellar" (ciencia ficción, Christopher Nolan):

```
======== TOP 5 PARA INTERSTELLAR ========
1. Inception                                10.8
2. The Dark Knight                          10.0
3. The Matrix                               9.7
4. The Prestige                             9.5
5. Blade Runner 2049                        9.0
```

Inception encabeza con 8,8 de valoración más 1,0 por el género y 1,0 por el director. The Dark Knight no es de ciencia ficción pero es del mismo director: 9,0 más 1,0. Para una película sin parecidos, como Coco, solo aparecen las del mismo género.

## Pruebas

```bash
python -m unittest -v
```

[tests/test_heap.py](../tests/test_heap.py) verifica que la heap extrae de mayor a menor, el desempate por orden de entrada, la construcción desde una lista, el caso vacío, que el Top 10 coincide con ordenar la lista, y que el ranking de recomendaciones está ordenado y no incluye a la película elegida.
