import pandas as pd


def get_years(
    df: pd.DataFrame,
) -> list[int]:
    """Retorna os anos disponíveis no GR38."""

    return sorted(
        df[
            "ANO_REFERENCIA"
        ]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )


def get_admission_forms(
    df: pd.DataFrame,
) -> list[str]:
    """Retorna as formas de ingresso disponíveis."""

    return sorted(
        df[
            "FORMA_INGRESSO"
        ]
        .dropna()
        .unique()
        .tolist()
    )