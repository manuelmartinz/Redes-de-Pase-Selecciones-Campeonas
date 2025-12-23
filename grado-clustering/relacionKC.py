#!/usr/bin/env python3
"""
Genera una gráfica de dispersión grado vs coeficiente de clustering
para una red (un CSV sin cabecera).

- Grado total k: columna E (5ª columna -> índice 4)
- Clustering:    columna R (18ª columna -> índice 17)

Uso:
    python scatter_k_vs_C.py archivo.csv NombreSeleccion

Ejemplo:
    python scatter_k_vs_C.py Francia.csv Francia
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 3:
        print("Uso: python scatter_k_vs_C.py <archivo.csv> <NombreSeleccion>")
        sys.exit(1)

    csv_path = sys.argv[1]
    label = sys.argv[2]   # "Francia", "España", "Argentina", etc.

    # ⚠️ Cambia sep=";" si tu CSV usa ';' como separador
    try:
        df = pd.read_csv(csv_path, header=None, sep=",")
    except Exception as e:
        print(f"Error al leer el CSV '{csv_path}': {e}")
        sys.exit(1)

    col_k = 4          # E -> índice 4
    col_C = 17         # R -> índice 17

    n_cols = len(df.columns)
    if col_k >= n_cols or col_C >= n_cols:
        print(f"El CSV '{csv_path}' no tiene suficientes columnas (necesita al menos 18).")
        print(f"Tiene {n_cols} columnas.")
        sys.exit(1)

    # Extraer columnas
    k = df.iloc[:, col_k]
    C = df.iloc[:, col_C]

    # Convertir a numérico y limpiar valores no válidos
    k = pd.to_numeric(k, errors="coerce")
    C = pd.to_numeric(C, errors="coerce")

    mask = k.notna() & C.notna()
    k = k[mask]
    C = C[mask]

    if k.empty:
        print(f"No hay datos numéricos válidos de k y C en '{csv_path}'.")
        sys.exit(1)

    # Gráfica de dispersión
    plt.figure()
    plt.scatter(k, C, alpha=0.7)

    plt.xlabel("Grado total k ")
    plt.ylabel("Coeficiente de clustering C ")
    plt.title(f"Relación grado vs clustering ({label})")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Guardar y mostrar
    safe_label = label.replace(" ", "_")
    output_png = f"scatter_k_vs_C_{safe_label}.png"
    plt.savefig(output_png, dpi=300)
    print(f"Gráfica guardada como: {output_png}")

    plt.show()

if __name__ == "__main__":
    main()

