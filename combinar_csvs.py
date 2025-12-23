# combinar_AR.py
#
# Combina en un único CSV todos los ficheros que terminan en "AR.csv"
# (por ejemplo: match_3869151_passes_events_AR.csv, ...).
#
# Requisitos:
#   pip install pandas
#
# Uso:
#   python combinar_AR.py

import pandas as pd
from pathlib import Path

# ========= PARÁMETROS A EDITAR =========

# Carpeta donde están los CSV
INPUT_FOLDER = Path("Partidos Argentina")      # "." = carpeta actual

# Patrón de ficheros a combinar (todos los que acaben en AR.csv)
FILE_PATTERN = "*AR.csv"

# Nombre del CSV combinado de salida
OUTPUT_CSV = "combinado_AR.csv"




def main():
    # Buscar todos los ficheros que coincidan con el patrón *AR.csv
    files = sorted(INPUT_FOLDER.glob(FILE_PATTERN))

    if not files:
        print(f"No se han encontrado ficheros que terminen en 'AR.csv' en {INPUT_FOLDER.resolve()}")
        return

    print("Ficheros que se van a combinar:")
    for f in files:
        print(f"  - {f.name}")

    dataframes = []

    for f in files:
        print(f"\nLeyendo y procesando: {f.name}")
        df = pd.read_csv(f)

        # Añadimos columna con el nombre del fichero origen (útil para depurar)
        df["source_file"] = f.name

        if df.empty:
            print(f"    OJO: después de los filtros no quedan filas en {f.name}")
        else:
            print(f"    Filas que se añaden al combinado: {len(df)}")
            dataframes.append(df)

    if not dataframes:
        print("\nNo hay datos para combinar (todos los dataframes quedaron vacíos).")
        return

    combinado = pd.concat(dataframes, ignore_index=True)

    print(f"\nTotal de filas combinadas: {len(combinado)}")
    print(f"Guardando en: {OUTPUT_CSV}")
    combinado.to_csv(OUTPUT_CSV, index=False)
    print("Hecho.")

if __name__ == "__main__":
    main()
