import pandas as pd


def get_years(
    df: pd.DataFrame,
) -> list[int]:
    """Retorna os anos disponíveis."""

    return sorted(
        df[
            "ANO_REFERENCIA"
        ]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )


def filter_by_year(
    df: pd.DataFrame,
    year: int,
) -> pd.DataFrame:
    """Filtra o GR16 pelo ano de referência."""

    return (
        df[
            df[
                "ANO_REFERENCIA"
            ]
            == year
        ]
        .copy()
        .reset_index(
            drop=True
        )
    )


def age_statistics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Retorna estatísticas descritivas
    da idade dos acadêmicos.
    """

    age = (
        df["IDADE"]
        .dropna()
        .astype(float)
    )

    if age.empty:
        return pd.DataFrame(
            columns=[
                "Indicador",
                "Valor",
            ]
        )

    data = [
        (
            "Contagem de acadêmicos",
            int(age.count()),
        ),
        (
            "Média de idade",
            age.mean(),
        ),
        (
            "Desvio padrão",
            age.std(),
        ),
        (
            "Idade mínima",
            int(age.min()),
        ),
        (
            "1º quartil (Q1)",
            age.quantile(0.25),
        ),
        (
            "Mediana da idade",
            age.median(),
        ),
        (
            "3º quartil (Q3)",
            age.quantile(0.75),
        ),
        (
            "Idade máxima",
            int(age.max()),
        ),
    ]

    return pd.DataFrame(
        data,
        columns=[
            "Indicador",
            "Valor",
        ],
    )