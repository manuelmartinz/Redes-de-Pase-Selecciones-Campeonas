# extract_passes_single_match.py
#
# Extrae TODOS los pases de un partido (match_id) de StatsBomb Open Data
# y los guarda en un CSV.
#
# Requisitos:
#   pip install statsbombpy pandas

from statsbombpy import sb
import pandas as pd

# ========= PARÁMETROS A EDITAR =========

MATCH_ID = 7563         # <-- pon aquí el match_id que quieras
TEAM_FILTER = "France"    # solo pases de Spain

OUTPUT_CSV = f"match_{MATCH_ID}_passes_events_francia.csv"

# ======================================


def main():
    print(f"Descargando eventos de match_id={MATCH_ID}...")
    events = sb.events(match_id=MATCH_ID)

    # Solo eventos de tipo "Pass"
    passes = events[events["type"] == "Pass"].copy()

    # Filtrar solo por el equipo deseado
    if TEAM_FILTER is not None:
        passes = passes[passes["team"] == TEAM_FILTER].copy()

    if passes.empty:
        print("No se han encontrado pases. ¿Seguro que el match_id y el filtro son correctos?")
        return

    # Columnas que nos interesa guardar
    columnas_interes = [
        "match_id",
        "team",
        "player",               # quien pasa
        "pass_recipient",       # quien recibe
        "minute",
        "second",
        "period",
        "location",
        "pass_end_location",
        "pass_length",
        "pass_angle",
        "pass_height",
        "pass_type",
        "pass_technique",
        "pass_cross",
        "pass_cut_back",
        "pass_switch",
        "pass_through_ball",
        "pass_straight",
        "pass_deflected",
        "pass_outcome",
        "pass_shot_assist",
        "pass_goal_assist",
        "pass_assisted_shot_id",
        "under_pressure",
        "play_pattern",
    ]

    # Algunas columnas pueden no existir, así que nos quedamos con las que haya
    columnas_existentes = [c for c in columnas_interes if c in passes.columns]

    passes_clean = passes[columnas_existentes].copy()

    print(f"Guardando {len(passes_clean)} pases en {OUTPUT_CSV} ...")
    passes_clean.to_csv(OUTPUT_CSV, index=False)
    print("Hecho.")


if __name__ == "__main__":
    main()

