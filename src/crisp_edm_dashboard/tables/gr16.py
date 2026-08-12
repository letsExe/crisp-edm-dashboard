import pandas as pd


AGE_BAND_ORDER = [
    "18-24",
    "25-30",
    "31-40",
    "41-50",
    "51+",
    "Não informado",
]


RACE_ORDER = [
    "Branca",
    "Parda",
    "Preta",
    "Amarela",
    "Não declarada",
    "Não informado",
]


POSITION_ORDER = [
    "Séries 1–3",
    "Série final (4ª)",
]


def sex_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Quantidade de acadêmicos por sexo."""

    table = (
        df["SEXO"]
        .value_counts()
        .rename_axis(
            "SEXO"
        )
        .reset_index(
            name="QUANTIDADE"
        )
    )

    return table


def age_band_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Quantidade de acadêmicos por faixa etária."""

    table = (
        df["FAIXA_ETARIA"]
        .value_counts()
        .reindex(
            AGE_BAND_ORDER,
            fill_value=0,
        )
        .rename_axis(
            "FAIXA_ETARIA"
        )
        .reset_index(
            name="QUANTIDADE"
        )
    )

    table = table[
        table["QUANTIDADE"] > 0
    ]

    return table


def race_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Quantidade e percentual de acadêmicos
    por cor/raça.
    """

    total = len(df)

    table = (
        df["COR_RACA"]
        .value_counts()
        .reindex(
            RACE_ORDER,
            fill_value=0,
        )
        .rename_axis(
            "COR_RACA"
        )
        .reset_index(
            name="TOTAL_ALUNOS"
        )
    )

    table = table[
        table[
            "TOTAL_ALUNOS"
        ] > 0
    ].copy()

    table[
        "PERCENTUAL"
    ] = (
        table[
            "TOTAL_ALUNOS"
        ]
        .div(total)
        .mul(100)
    )

    return table


def sex_by_series(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Distribuição do sexo por série."""

    table = pd.crosstab(
        df["SERIE"],
        df["SEXO"],
    )

    table = (
        table.reindex(
            [1, 2, 3, 4],
            fill_value=0,
        )
        .reset_index()
    )

    return table


def position_by_race(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula a distribuição percentual da posição
    curricular dentro de cada grupo de cor/raça.
    """

    table = pd.crosstab(
        df["COR_RACA"],
        df[
            "POSICAO_CURRICULAR"
        ],
        normalize="index",
    ).mul(100)

    table = table.reindex(
        columns=POSITION_ORDER,
        fill_value=0,
    )

    existing_races = [
        race
        for race in RACE_ORDER
        if race in table.index
    ]

    table = table.reindex(
        existing_races
    )

    return (
        table
        .reset_index()
    )


def age_band_by_series(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Distribuição das faixas etárias por série.
    """

    table = pd.crosstab(
        df["SERIE"],
        df["FAIXA_ETARIA"],
    )

    existing_columns = [
        band
        for band in AGE_BAND_ORDER
        if band in table.columns
    ]

    table = table.reindex(
        index=[1, 2, 3, 4],
        columns=existing_columns,
        fill_value=0,
    )

    return table.reset_index()