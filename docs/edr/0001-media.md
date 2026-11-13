# EDR 0001 — Media de un conjunto sintético

- Estado: prerregistrado
- Configuración: [ejemplo.json](../../experiments/ejemplo.json)
- Lectura: [[remuestreo]]

## Contexto y decisión

Usaremos cinco observaciones sintéticas y calcularemos su media. El remuestreo
con reemplazo permite practicar el registro de una semilla y una métrica derivada.

## Hipótesis y criterio de éxito

La media del conjunto debe ser 6. El intervalo empírico debe contener la media.
Con la semilla 42 y la misma versión de Python, las métricas de dos ejecuciones
deben coincidir byte a byte.

## Criterio de parada

1.000 remuestreos por ejecución. Se harán dos ejecuciones para comprobar
la repetibilidad. Un fallo de validación cancela la ejecución.

## Consecuencias y limitaciones

El ejercicio comprueba el proceso de trabajo con datos construidos. Para
interpretar un intervalo en un estudio real hay que justificar el diseño muestral.

## Ejecuciones, desviaciones y conclusión

Completar al cerrar la práctica.
