import re
import unicodedata

import pandas as pd


def normalize_column_name(column: str) -> str:
    """
    Padroniza o nome de uma coluna.

    Exemplo:
        'COR/RAÇA ' -> 'COR_RACA'
        'PERIODO LETIVO' -> 'PERIODO_LETIVO'
        'SITUAÇÃO' -> 'SITUACAO'
    """

    value = str(column).strip()

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    value = value.upper()

    value = re.sub(r"[/\\\-\s]+", "_", value)
    value = re.sub(r"_+", "_", value)

    return value.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza todos os nomes das colunas de um DataFrame."""

    df = df.copy()

    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    return df