# Investigación reproducible

Este repositorio es un laboratorio de práctica. El primer experimento calcula
una media conocida y genera una tabla de resultados. Necesitas Git y Python
3.13.2, la versión que usa GitHub Actions. El ejemplo usa la biblioteca estándar
de Python. Obsidian, Pandoc y el contenedor son opcionales para la primera práctica.

## 1. Ejecuta las pruebas en tu equipo

Abre una terminal en la carpeta de este README y ejecuta:

```bash
python3 -m unittest discover -s tests -v
```

Deberías ver cuatro pruebas y un `OK`. Una prueba comprueba que la media de los
datos de ejemplo es 6. Otra comprueba que el lector rechaza valores inválidos.

## 2. Recorre el experimento completo

1. Lee la [nota de lectura](literature/remuestreo.md) y el
   [EDR 0001](docs/edr/0001-media.md), el registro de la hipótesis y los
   criterios de éxito y parada.
2. Revisa la [configuración](experiments/ejemplo.json) y ejecuta desde la raíz:

   ```bash
   python3 -m src.run experiments/ejemplo.json
   ```

3. Abre la carpeta que imprime el comando. `metadata.json` guarda el commit,
   la huella SHA-256 de los datos, la versión de Python y la configuración.
   `metricas.json` guarda los números. `manuscrito.md` contiene la tabla
   generada a partir de esos números.
4. Ejecuta el mismo comando de nuevo. Cada ejecución crea su propia carpeta.
   Las métricas y el manuscrito coinciden con la misma versión de Python.
5. Abre la raíz como bóveda de Obsidian. Crea las notas de la
   [bitácora](docs/devlogs/README.md) con las plantillas de `__templates/`,
   enlaza los resultados en el EDR y registra tu conclusión en un nuevo commit.

Guarda los cambios en Git antes de cada ejecución oficial. El comando lee el
CSV, la configuración, el EDR y el manuscrito del commit. Las carpetas de
ejecución quedan fuera de Git. Si una ejecución va a respaldar una publicación,
conserva sus archivos en almacenamiento compartido y guarda su enlace en el runlog.

Si tienes Pandoc, puedes exportar el manuscrito recién generado a HTML:

```bash
run=$(python3 -m src.run experiments/ejemplo.json)
pandoc --defaults=.pandoc/exportacion.yaml "$run/manuscrito.md" -o "$run/manuscrito.html"
```

## 3. Practica GitHub Actions

Crea un repositorio vacío en GitHub y sigue sus instrucciones para subir un
repositorio local existente. Cuando subas `main`, abre **Actions** y entra en
**Pruebas y experimento de ejemplo**. El flujo ejecuta las pruebas y comprueba
que dos ejecuciones producen las mismas métricas y el mismo manuscrito. También
se ejecuta en cada pull request.

Cuando veas el primer resultado verde, practica un fallo deliberado en una rama:

1. Ejecuta `git switch -c practica-ci`.
2. En `tests/test_analysis.py`, cambia solo el valor esperado de la media
   de `6.0` a `7.0`. Ejecuta las pruebas y lee el mensaje que compara los dos valores.
3. Guarda y sube el cambio con `git add tests/test_analysis.py`,
   `git commit -m "Provocar un fallo de prueba"` y
   `git push -u origin practica-ci`. Abre un pull request y consulta el fallo
   en la pestaña **Checks** del pull request.
4. Restaura `6.0`, guarda otro commit y ejecuta `git push`. Comprueba que
   el pull request vuelve a verde.

## 4. Adapta la plantilla a un proyecto real

Empieza con un EDR, una muestra de datos pequeña y una prueba con resultado
conocido. Registra el EDR antes de correr el análisis y enlaza la configuración.
El ejemplo usa JSON para que Python pueda leerla sin instalar un paquete.
Los datos pequeños se guardan en Git y se verifican mediante SHA-256.
La [nota de datos](data/README.md) indica dónde incorporar DVC al necesitarlo.

Antes de publicar, comprueba que una copia nueva supera las pruebas y regenera
la tabla con un solo comando. Revisa que todos los EDR tengan una conclusión
y que las métricas citadas apunten a una ejecución conservada y a su commit.
