# build_pass_network_by_type_weighted.py
#
# Construye una red dirigida y ponderada:
#   - Nodos: jugadores
#   - Aristas: (Source -> Target, pass_category)
#   - Weight = nº de pases COMPLETADOS de esa categoría
#
# pass_category se define SOLO con pass_type y flags pass_*:
#   1) Assist            -> pass_shot_assist o pass_goal_assist True
#   2) Cross             -> pass_cross True
#   3) Through ball      -> pass_through_ball True
#   4) Switch of play    -> pass_switch True
#   5) Throw-in          -> pass_type == "Throw-in"
#   6) Goal Kick         -> pass_type == "Goal Kick"
#   7) Free Kick         -> pass_type == "Free Kick"
#   8) Regular pass      -> resto
#
# IMPORTANTE:
#   - Los eventos con pass_type "Recovery" o "Interception" se MARCAN
#     en recovery_interception_pass, pero NO se cuentan como pases
#     (completed = 0, failed = 0) y por tanto no suman a Weight.
#
# NO se usa play_pattern para nada.

import pandas as pd

INPUT_CSV = "/home/manuel/Escritorio/RSC P4/Partidos Argentina/combinado_AR.csv"
OUTPUT_CSV = "/home/manuel/Escritorio/RSC P4/Partidos Argentina/comb_AR_edges.csv"

TEAM_FILTER = None  # o "Argentina", "Spain", etc. si en el CSV hay varios equipos


def to_bool(val):
    """Convierte valores (True/False, 1/0, 'True', NaN...) a bool de forma robusta."""
    if pd.isna(val):
        return False
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, str):
        return val.strip().lower() in ("true", "t", "yes", "y", "1")
    return bool(val)


def classify_pass(row: pd.Series) -> str:
    """
    Clasificación de tipo de pase SOLO con pass_type y flags pass_*.
    NO usa play_pattern.

    Prioridad:
      1) Assist (shot + goal)
      2) Cross
      3) Through ball
      4) Switch of play
      5) Throw-in
      6) Goal Kick
      7) Free Kick
      8) Regular pass (resto)
    """

    ptype = row.get("pass_type", None)

    cross = to_bool(row.get("pass_cross", False))
    switch = to_bool(row.get("pass_switch", False))
    through = to_bool(row.get("pass_through_ball", False))

    shot_assist = to_bool(row.get("pass_shot_assist", False))
    goal_assist = to_bool(row.get("pass_goal_assist", False))
    assist_flag = shot_assist or goal_assist

    # 1) Asistencias (de tiro o de gol)
    if assist_flag:
        return "Assist"

    # 2) Centros
    if cross:
        return "Cross"

    # 3) Pases al hueco / entre líneas
    if through:
        return "Through ball"

    # 4) Cambios de orientación
    if switch:
        return "Switch of play"

    # 5) Saque de banda
    if ptype == "Throw-in":
        return "Throw-in"

    # 6) Saque de puerta
    if ptype == "Goal Kick":
        return "Goal Kick"

    # 7) Falta (pase desde Free Kick)
    if ptype == "Free Kick":
        return "Free Kick"

    # 8) Todo lo demás -> pase normal
    return "Regular pass"


def main():
    df = pd.read_csv(INPUT_CSV)

    # Filtrar por equipo si procede
    if TEAM_FILTER is not None and "team" in df.columns:
        df = df[df["team"] == TEAM_FILTER].copy()

    # Columnas básicas obligatorias
    for col in ["player", "pass_recipient"]:
        if col not in df.columns:
            raise ValueError(f"Falta la columna '{col}' en {INPUT_CSV}")

    # Quitamos filas sin origen o destino
    df = df.dropna(subset=["player", "pass_recipient"]).copy()

    # Flag adicional: evento Recovery/Interception
    if "pass_type" in df.columns:
        df["is_ri_event"] = df["pass_type"].isin(["Recovery", "Interception"])
        df["recovery_interception_pass"] = df["is_ri_event"].astype(int)
    else:
        df["is_ri_event"] = False
        df["recovery_interception_pass"] = 0

    # Pase completado (pass_outcome NaN => completado),
    # PERO excluimos Recovery/Interception de completed y failed
    if "pass_outcome" in df.columns:
        base_completed = df["pass_outcome"].isna()
    else:
        # Si no hay pass_outcome, asumimos que son completados,
        # salvo los Recovery/Interception que queremos excluir
        base_completed = True

    df["completed"] = base_completed & ~df["is_ri_event"]
    df["failed"] = (~base_completed) & ~df["is_ri_event"]

    # Pasamos a enteros para agregarlos bien
    df["completed"] = df["completed"].astype(int)
    df["failed"] = df["failed"].astype(int)

    # Aseguramos que las columnas de assist son numéricas 0/1 (si existen)
    for col in ["pass_shot_assist", "pass_goal_assist"]:
        if col in df.columns:
            df[col] = df[col].apply(to_bool).astype(int)
        else:
            df[col] = 0

    # Clasificación de tipo de pase SIN usar play_pattern
    df["pass_category"] = df.apply(classify_pass, axis=1)

    # Agrupamos por jugador origen, destino y categoría
    group_cols = ["player", "pass_recipient", "pass_category"]

    agg_dict = {
        "completed": "sum",           # nº pases completados => Weight
        "failed": "sum",
        "pass_shot_assist": "sum",    # número de shot assists
        "pass_goal_assist": "sum",    # número de goal assists
        "recovery_interception_pass": "sum",  # nº de eventos Recovery/Interception
    }

    edges = (
        df.groupby(group_cols)
          .agg(agg_dict)
          .reset_index()
          .rename(columns={
              "completed": "Weight",
              "failed": "failed_passes",
          })
    )

    # total de pases (solo los que cuentan como pases) = completados + fallados
    edges["total_passes"] = edges["Weight"] + edges["failed_passes"]

    # Contador combinado de asistencias (shot + goal)
    edges["assist_count"] = edges["pass_shot_assist"] + edges["pass_goal_assist"]

    # (Opcional) eliminar columnas auxiliares de asistencias
    edges = edges.drop(columns=["pass_shot_assist", "pass_goal_assist"])

    # Renombrar para Gephi
    edges = edges.rename(columns={
        "player": "Source",
        "pass_recipient": "Target",
    })

    # Label para colorear aristas en Gephi
    edges["label"] = edges["pass_category"]

    # Aseguramos que assist_count sea entero
    edges["assist_count"] = edges["assist_count"].fillna(0).astype(int)

    # ❗ Eliminar aristas sin ningún pase COMPLETADO (Weight = 0)
    edges = edges[edges["Weight"] > 0].copy()

    print(f"Nº de aristas (Source→Target por categoría, Weight>0): {len(edges)}")
    print(f"Total de pases COMPLETADOS (suma de Weight): {int(edges['Weight'].sum())}")
    print(f"Total eventos Recovery/Interception (agregados): {int(edges['recovery_interception_pass'].sum())}")

    edges.to_csv(OUTPUT_CSV, index=False)
    print(f"Red de pases guardada en {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

