import pandas as pd


AGE_BAND_ORDER = [
    "Até 18 anos",
    "19–24 anos",
    "25–30 anos",
    "31–40 anos",
    "41–50 anos",
    "51+ anos",
]


def year_summary(
    df: pd.DataFrame,
    year: int,
) -> dict:
    """Resumo dos ingressantes de determinado ano."""

    filtered = df[
        df["ANO_REFERENCIA"]
        == year
    ]

    return {
        "TOTAL": int(
            filtered[
                "TOTAL"
            ].sum()
        ),
        "MASCULINO": int(
            filtered[
                "MASCULINO"
            ].sum()
        ),
        "FEMININO": int(
            filtered[
                "FEMININO"
            ].sum()
        ),
    }


def admission_form_distribution(
    df: pd.DataFrame,
    year: int,
) -> pd.DataFrame:
    """Distribuição dos ingressantes por forma de ingresso."""

    filtered = df[
        df["ANO_REFERENCIA"]
        == year
    ]

    table = (
        filtered.groupby(
            "FORMA_INGRESSO",
            as_index=False,
        )
        .agg(
            TOTAL=(
                "TOTAL",
                "sum",
            )
        )
    )

    total_students = (
        table["TOTAL"]
        .sum()
    )

    table["PERCENTUAL"] = (
        table["TOTAL"]
        .div(total_students)
        .mul(100)
    )

    return (
        table.sort_values(
            "TOTAL",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def age_band_distribution(
    df: pd.DataFrame,
    year: int,
) -> pd.DataFrame:
    """Distribuição por faixa etária."""

    filtered = df[
        df["ANO_REFERENCIA"]
        == year
    ]

    table = (
        filtered.groupby(
            "FAIXA_ETARIA",
            as_index=False,
        )
        .agg(
            TOTAL=(
                "TOTAL",
                "sum",
            )
        )
    )

    table[
        "FAIXA_ETARIA"
    ] = pd.Categorical(
        table[
            "FAIXA_ETARIA"
        ],
        categories=AGE_BAND_ORDER,
        ordered=True,
    )

    table = (
        table.sort_values(
            "FAIXA_ETARIA"
        )
        .reset_index(drop=True)
    )

    total_students = (
        table["TOTAL"].sum()
    )

    table["PERCENTUAL"] = (
        table["TOTAL"]
        .div(total_students)
        .mul(100)
    )

    return table


def age_band_by_admission_form(
    df: pd.DataFrame,
    year: int,
) -> pd.DataFrame:
    """Faixa etária por forma de ingresso."""

    filtered = df[
        df["ANO_REFERENCIA"]
        == year
    ]

    table = (
        filtered.pivot_table(
            index="FORMA_INGRESSO",
            columns="FAIXA_ETARIA",
            values="TOTAL",
            aggfunc="sum",
            fill_value=0,
            observed=False,
        )
    )

    columns = [
        band
        for band in AGE_BAND_ORDER
        if band in table.columns
    ]

    table = table.reindex(
        columns=columns,
        fill_value=0,
    )

    return (
        table
        .reset_index()
    )


def sex_by_admission_form(
    df: pd.DataFrame,
    year: int,
) -> pd.DataFrame:
    """Distribuição por sexo em cada forma de ingresso."""

    filtered = df[
        df["ANO_REFERENCIA"]
        == year
    ]

    table = (
        filtered.groupby(
            "FORMA_INGRESSO",
            as_index=False,
        )
        .agg(
            MASCULINO=(
                "MASCULINO",
                "sum",
            ),
            FEMININO=(
                "FEMININO",
                "sum",
            ),
        )
    )

    table["TOTAL"] = (
        table["MASCULINO"]
        + table["FEMININO"]
    )

    return (
        table.sort_values(
            "TOTAL",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def admission_form_evolution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Quantidade de ingressantes por ano e
    forma de ingresso.
    """

    return (
        df.groupby(
            [
                "ANO_REFERENCIA",
                "FORMA_INGRESSO",
            ],
            as_index=False,
        )
        .agg(
            TOTAL=(
                "TOTAL",
                "sum",
            )
        )
        .sort_values(
            [
                "ANO_REFERENCIA",
                "FORMA_INGRESSO",
            ]
        )
        .reset_index(drop=True)
    )