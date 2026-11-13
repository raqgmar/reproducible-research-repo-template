import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from uuid import uuid4

from src.analysis import estimate, read_values

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "outputs" / "runs"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def tracked_file(relative_path, commit):
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Usa una ruta relativa dentro del repositorio: {path}")
    # Leer del commit garantiza que el hash describe exactamente los bytes usados.
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path.as_posix()}"], cwd=ROOT
    )


def markdown(result):
    return f"""## Resultados

Estimación sobre datos sintéticos. El intervalo usa los percentiles 2,5 y 97,5
de las medias obtenidas por remuestreo con reemplazo.

| Observaciones | Media | Límite inferior | Límite superior |
|---:|---:|---:|---:|
| {result['n']} | {result['mean']:.3f} | {result['lower']:.3f} | {result['upper']:.3f} |
"""


def main():
    parser = argparse.ArgumentParser(description="Ejecuta un experimento registrado.")
    parser.add_argument("config", help="Ruta versionada, relativa al repositorio.")
    args = parser.parse_args()
    try:
        if git("status", "--porcelain"):
            raise ValueError("Hay cambios pendientes. Revísalos y guarda un commit antes de ejecutar.")
        commit = git("rev-parse", "HEAD")
        config = json.loads(tracked_file(args.config, commit))
        seed = config["seed"]
        resamples = config["resamples"]
        if type(seed) is not int:
            raise ValueError("Declara una semilla entera en seed.")
        if type(resamples) is not int or not 100 <= resamples <= 10000:
            raise ValueError("resamples debe ser un entero entre 100 y 10000.")
        edr = config["edr"]
        if not isinstance(edr, str) or not edr.startswith("docs/edr/") or not edr.endswith(".md"):
            raise ValueError("edr debe apuntar a un Markdown dentro de docs/edr/.")
        tracked_file(edr, commit)
        data = tracked_file(config["data"], commit)
        result = estimate(read_values(data), seed, resamples)
        manuscript = tracked_file("paper/manuscrito.md", commit).decode("utf-8")
    except (OSError, ValueError, KeyError, TypeError, csv.Error, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Experimento cancelado: {error}\n")

    timestamp = datetime.now(timezone.utc)
    run_id = f"{timestamp:%Y%m%dT%H%M%SZ}-{uuid4().hex}"
    metadata = {
        "run": run_id,
        "created_utc": timestamp.isoformat(),
        "git_commit": commit,
        "data_sha256": hashlib.sha256(data).hexdigest(),
        "python": platform.python_version(),
        "config_path": args.config,
        "config": config,
    }

    RUNS.mkdir(parents=True, exist_ok=True)
    staging = RUNS / f".{run_id}"
    staging.mkdir()
    try:
        (staging / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        (staging / "metricas.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        metrics = json.loads((staging / "metricas.json").read_text(encoding="utf-8"))
        (staging / "manuscrito.md").write_text(manuscript.replace("<!-- RESULTADOS -->", markdown(metrics)), encoding="utf-8")
        destination = RUNS / run_id
        os.rename(staging, destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    print(destination.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
