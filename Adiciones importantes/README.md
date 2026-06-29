# Micron (Micron-Interpreter)

Micron es un intérprete pequeño escrito en Python. Esta carpeta contiene archivos iniciales y sugerencias para mejorar la presentación y la conservación del proyecto. Mueve o integra estos archivos a la raíz cuando estés listo.

## Estado
- Licencia: MIT

## Requisitos
- Python 3.8

> Nota: la librería `os` forma parte de la biblioteca estándar de Python y NO necesita instalarse con pip.

## Instalación (local)
```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r "Adiciones importantes/requirements.txt"
pip install -e .
```

## Ejemplo de uso
```bash
python -m micron_interpreter ejemplo_input.txt
```

## Tests
```bash
pytest -q
```

## Qué incluye esta carpeta
- README.md (este archivo): explicación mínima y notas.
- .gitignore: sugerencias para ignorar archivos comunes.
- requirements.txt: dependencias (actualmente vacía porque solo se usa stdlib).
- .github/workflows/ci.yml: workflow de ejemplo para ejecutar tests en Python 3.8.

## Contribuir
Si quieres, puedo añadir CONTRIBUTING.md, plantillas de issues/PR y ejemplos en `examples/`. Dime si deseas que los cree aquí también.