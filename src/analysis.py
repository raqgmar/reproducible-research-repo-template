import csv
import io
import math
import random
from statistics import mean


def read_values(data):
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig")), strict=True)
    if next(reader, None) != ["valor"]:
        raise ValueError("El CSV debe tener una única columna llamada valor.")
    values = []
    for line, row in enumerate(reader, start=2):
        if len(row) != 1:
            raise ValueError(f"Fila {line}: se esperaba un valor.")
        try:
            value = float(row[0])
        except ValueError as error:
            raise ValueError(f"Fila {line}: falta un número válido.") from error
        if not math.isfinite(value) or not 0 <= value <= 10:
            raise ValueError(f"Fila {line}: el valor debe estar entre 0 y 10.")
        values.append(value)
    if len(values) < 2:
        raise ValueError("Se necesitan al menos dos observaciones.")
    return values


def estimate(values, seed, resamples):
    rng = random.Random(seed)
    samples = sorted(mean(rng.choices(values, k=len(values))) for _ in range(resamples))
    last = resamples - 1
    return {
        "n": len(values),
        "mean": mean(values),
        "lower": samples[last * 25 // 1000],
        "upper": samples[last * 975 // 1000],
    }
