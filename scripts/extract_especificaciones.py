#!/usr/bin/env python3
import re
import json
import glob
import os
from pathlib import Path

def extract_especificaciones_from_file(file_path):
    """
    Abre un JSON, busca el campo 'textoAnotaciones' y extrae
    todos los números de 3 a 5 dígitos tras 'ESPECIFICACION:'.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texto = data.get('textoAnotaciones', '')
    pattern = re.compile(r'ESPECIFICACION:\s*(\d{3,5})')
    return pattern.findall(texto)

def main():
    # Carpeta donde están tus JSON de folios
    carpeta = Path(__file__).parent.parent / "folios"
    print(f"Buscando en carpeta: {carpeta.resolve()}\n")

    if not carpeta.exists():
        print("¡Error! No encuentro la carpeta de folios.")
        return

    # Itera sobre todos los .json
    for file_path in glob.glob(str(carpeta / "*.json")):
        codes = extract_especificaciones_from_file(file_path)
        nombre = Path(file_path).name
        print(f"{nombre} → Códigos encontrados: {codes}")

if __name__ == "__main__":
    main()

