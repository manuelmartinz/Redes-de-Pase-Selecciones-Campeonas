#!/usr/bin/env python3
"""
Lee un CSV SIN cabecera y genera un histograma usando la columna R
(18ª columna, índice 17 en Python) como coeficiente de clustering.

Uso:
    
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Uso: python hist_clustering_colR.py <archivo.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]

    # 1. Leer CSV SIN cabecera (header=None)
    try:
        df = pd.read_csv(csv_path, header=None)
        # Si tu CSV va con ; en vez de , usa:
        # df = pd.read_csv(csv_path, header=None, sep=";")
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        sys.exit(1)

    # Columna R -> índice 17 (A=0, B=1, ..., R=17)
    col_index = 17

    if col_index >= len(df.columns):
        print("El CSV no tiene tantas columnas.")
        print(f"Nº columnas encontradas: {len(df.columns)}")
        sys.exit(1)

    # 2. Extraer columna de clustering (columna R completa, desde la primera fila)
    clustering = df.iloc[:, col_index]

    # Convertir a numérico y eliminar valores no válidos
    clustering = pd.to_numeric(clustering, errors="coerce")
    clustering = clustering.dropna()

    if clustering.empty:
        print("No hay valores numéricos válidos en la columna R.")
        sys.exit(1)

    # 3. Crear histograma
    plt.figure()
    # bins=10 -> divide el rango [min(C), max(C)] en 10 "cajones"
    plt.hist(clustering, bins=10)

    plt.xlabel("Coeficiente de clustering")
    plt.ylabel("Número de nodos")
    plt.title("Histograma de coeficientes de clustering de Francia ")

    plt.tight_layout()

    # 4. Guardar y mostrar
    output_png = "hist_clustering_colR.png"
    plt.savefig(output_png, dpi=300)
    print(f"Histograma guardado como: {output_png}")

    plt.show()

if __name__ == "__main__":
    main()

