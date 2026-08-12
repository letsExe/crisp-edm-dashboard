import pandas as pd


SITUATION_ORDER = [
    "Formado",
    "Trancado",
    "Jubilado",
    "Cancelado por abandono",
    "Cancelado",
    "Abandono",
    "Cursando",
]


def create_yearly_status_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria a tabela anual com valores absolutos,
    total e percentuais por situação acadêmica.
    """

    pivot = df.pivot_table(
        index="PERIODO_LETIVO",
        columns="SITUACAO",
        values="QUANTIDADE",
        aggfunc="sum",
        fill_value=0,
    )

    pivot.columns.name = None

    # Ordenar primeiro as categorias conhecidas
    existing_situations = [
        situation
        for situation in SITUATION_ORDER
        if situation in pivot.columns
    ]

    extra_situations = [
        column
        for column in pivot.columns
        if column not in existing_situations
    ]

    situation_columns = (
        existing_situations
        + extra_situations
    )

    pivot = pivot[
        situation_columns
    ].copy()

    # Total anual
    pivot["Total"] = pivot[
        situation_columns
    ].sum(axis=1)

    # Percentuais
    for situation in situation_columns:
        pivot[f"% {situation}"] = (
            pivot[situation]
            .div(pivot["Total"])
            .mul(100)
            .fillna(0)
        )

    return pivot.reset_index()