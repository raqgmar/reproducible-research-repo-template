# Remuestreo con reemplazo

Para cada réplica extraemos tantas observaciones como contiene el conjunto
original, con reemplazo, y calculamos la media. Después ordenamos las medias
y seleccionamos dos posiciones cercanas a los percentiles 2,5 y 97,5.

- Implementación: [estimate en src/analysis.py](../src/analysis.py)
- Diseño del ejercicio: [[0001-media]]
