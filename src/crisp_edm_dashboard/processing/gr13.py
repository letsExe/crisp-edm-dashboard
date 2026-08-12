import unicodedata

import pandas as pd

from crisp_edm_dashboard.config import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
)
from crisp_edm_dashboard.loaders.excel import read_excel
from crisp_edm_dashboard.utils.columns import normalize_columns


GR13_INPUT = RAW_DATA_DIR / "gr13" / "GR13.xlsx"
GR13_OUTPUT = PROCESSED_DATA_DIR / "gr13.parquet"


SITUATION_MAP = {
    "formado": "Formado",
    "trancado": "Trancado",
    "jubilado": "Jubilado",
    "cancelado por abandono": "Cancelado por abandono",
    "cancelado": "Cancelado",
    "abandono": "Abandono",
    "cursando": "Cursando",
}


def normalize_text(value: str) -> str:
    """Remove diferenças de acentuação, caixa e espaços."""

    value = str(value).strip().lower()

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    return value


def normalize_situation(value: str) -> str:
    """Padroniza as categorias de situação acadêmica."""

    normalized = normalize_text(value)

    return SITUATION_MAP.get(
        normalized,
        str(value).strip(),
    )


def process_gr13(
    input_path=GR13_INPUT,
    output_path=GR13_OUTPUT,
) -> pd.DataFrame:
    """
    Carrega, valida e padroniza os dados brutos do GR13.
    """

    df = read_excel(input_path)

    df = normalize_columns(df)

    required_columns = {
        "SITUACAO",
        "PERIODO_LETIVO",
        "QUANTIDADE",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "O GR13 não possui todas as colunas esperadas. "
            f"Faltando: {sorted(missing_columns)}"
        )

    df = df[
        [
            "SITUACAO",
            "PERIODO_LETIVO",
            "QUANTIDADE",
        ]
    ].copy()

    # Padronizar situações
    df["SITUACAO"] = (
        df["SITUACAO"]
        .apply(normalize_situation)
    )

    # Converter campos numéricos
    df["PERIODO_LETIVO"] = pd.to_numeric(
        df["PERIODO_LETIVO"],
        errors="coerce",
    )

    df["QUANTIDADE"] = pd.to_numeric(
        df["QUANTIDADE"],
        errors="coerce",
    )

    # Remover registros inválidos
    df = df.dropna(
        subset=[
            "SITUACAO",
            "PERIODO_LETIVO",
            "QUANTIDADE",
        ]
    )

    df["PERIODO_LETIVO"] = (
        df["PERIODO_LETIVO"].astype(int)
    )

    df["QUANTIDADE"] = (
        df["QUANTIDADE"].astype(int)
    )

    # Impedir quantidades negativas
    df = df[df["QUANTIDADE"] >= 0]

    # Consolidar possíveis registros repetidos
    df = (
        df.groupby(
            [
                "PERIODO_LETIVO",
                "SITUACAO",
            ],
            as_index=False,
        )["QUANTIDADE"]
        .sum()
    )

    df = df.sort_values(
        [
            "PERIODO_LETIVO",
            "SITUACAO",
        ]
    ).reset_index(drop=True)

    # Salvar base processada
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        output_path,
        index=False,
    )

    return df