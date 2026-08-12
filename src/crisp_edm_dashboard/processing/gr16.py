import re

import pandas as pd

from crisp_edm_dashboard.config import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
)
from crisp_edm_dashboard.loaders.excel import (
    read_all_sheets,
)
from crisp_edm_dashboard.utils.columns import (
    normalize_columns,
)


GR16_INPUT = (
    RAW_DATA_DIR
    / "gr16"
    / "GR16.xlsx"
)

GR16_OUTPUT = (
    PROCESSED_DATA_DIR
    / "gr16.parquet"
)


SEX_MAP = {
    "m": "M",
    "masculino": "M",
    "f": "F",
    "feminino": "F",
}


RACE_MAP = {
    "branco": "Branca",
    "branca": "Branca",
    "preto": "Preta",
    "preta": "Preta",
    "pardo": "Parda",
    "parda": "Parda",
    "amarelo": "Amarela",
    "amarela": "Amarela",
    "não declarada": "Não declarada",
    "nao declarada": "Não declarada",
}


AGE_BAND_MAP = {
    "18-24": "18-24",
    "25-30": "25-30",
    "31-40": "31-40",
    "41-50": "41-50",
    "51-9999": "51+",
    "51+": "51+",
}


def normalize_whitespace(
    value: str,
) -> str:
    """Remove espaços extras de textos."""

    return re.sub(
        r"\s+",
        " ",
        str(value),
    ).strip()


def normalize_sex(
    value,
) -> str:
    """Padroniza os valores da variável sexo."""

    if pd.isna(value):
        return "Não informado"

    text = (
        normalize_whitespace(value)
        .lower()
    )

    return SEX_MAP.get(
        text,
        normalize_whitespace(value),
    )


def normalize_race(
    value,
) -> str:
    """
    Padroniza os valores de cor/raça.

    Valores ausentes são mantidos como
    uma categoria separada de 'Não declarada'.
    """

    if pd.isna(value):
        return "Não informado"

    text = (
        normalize_whitespace(value)
        .lower()
    )

    return RACE_MAP.get(
        text,
        normalize_whitespace(value),
    )


def normalize_age_band(
    value,
) -> str:
    """Padroniza as faixas etárias."""

    if pd.isna(value):
        return "Não informado"

    text = normalize_whitespace(
        value
    )

    return AGE_BAND_MAP.get(
        text,
        text,
    )


def classify_course_position(
    series: int,
) -> str:
    """
    Classifica a posição curricular sem inferir
    que o estudante seja efetivamente concluinte.
    """

    if series == 4:
        return "Série final (4ª)"

    return "Séries 1–3"


def process_gr16(
    input_path=GR16_INPUT,
    output_path=GR16_OUTPUT,
) -> pd.DataFrame:
    """
    Lê todas as abas do GR16, limpa e padroniza
    os dados e gera a base processada em Parquet.
    """

    sheets = read_all_sheets(
        input_path
    )

    frames = []

    for sheet_name, sheet_df in sheets.items():

        try:
            year = int(
                str(sheet_name).strip()
            )
        except ValueError:
            # Ignora abas que não representem anos
            continue

        df = sheet_df.copy()

        # Remove colunas vazias geradas pelo Excel,
        # como "Unnamed: 6".
        df = df.loc[
            :,
            ~df.columns
            .astype(str)
            .str.startswith("Unnamed")
        ]

        df = normalize_columns(
            df
        )

        required_columns = {
            "CURSO",
            "SERIE",
            "FAIXA_ETARIA",
            "SEXO",
            "COR_RACA",
            "IDADE",
        }

        missing_columns = (
            required_columns
            - set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                f"A aba {sheet_name} do GR16 "
                "não possui todas as colunas esperadas. "
                f"Faltando: {sorted(missing_columns)}"
            )

        # -----------------------------------
        # Campos numéricos
        # -----------------------------------

        df["SERIE"] = pd.to_numeric(
            df["SERIE"],
            errors="coerce",
        )

        df["IDADE"] = pd.to_numeric(
            df["IDADE"],
            errors="coerce",
        )

        # Remove linhas inválidas.
        #
        # Isso também elimina a linha de cabeçalho
        # repetida existente na aba de 2012.
        df = df.dropna(
            subset=[
                "SERIE",
            ]
        )

        df["SERIE"] = (
            df["SERIE"]
            .astype(int)
        )

        invalid_series = (
            ~df["SERIE"].isin(
                [1, 2, 3, 4]
            )
        )

        if invalid_series.any():
            values = (
                df.loc[
                    invalid_series,
                    "SERIE",
                ]
                .unique()
                .tolist()
            )

            raise ValueError(
                "Foram encontradas séries "
                f"inesperadas na aba {sheet_name}: "
                f"{values}"
            )

        # -----------------------------------
        # Textos e categorias
        # -----------------------------------

        df["CURSO"] = (
            df["CURSO"]
            .apply(
                normalize_whitespace
            )
        )

        df["SEXO"] = (
            df["SEXO"]
            .apply(
                normalize_sex
            )
        )

        df["COR_RACA"] = (
            df["COR_RACA"]
            .apply(
                normalize_race
            )
        )

        df["FAIXA_ETARIA"] = (
            df["FAIXA_ETARIA"]
            .apply(
                normalize_age_band
            )
        )

        # -----------------------------------
        # Ano e posição curricular
        # -----------------------------------

        df[
            "ANO_REFERENCIA"
        ] = year

        df[
            "POSICAO_CURRICULAR"
        ] = (
            df["SERIE"]
            .apply(
                classify_course_position
            )
        )

        # -----------------------------------
        # Seleção final
        # -----------------------------------

        df = df[
            [
                "ANO_REFERENCIA",
                "CURSO",
                "SERIE",
                "FAIXA_ETARIA",
                "SEXO",
                "COR_RACA",
                "IDADE",
                "POSICAO_CURRICULAR",
            ]
        ]

        frames.append(
            df
        )

    if not frames:
        raise ValueError(
            "Nenhuma aba válida foi encontrada "
            "no GR16."
        )

    result = pd.concat(
        frames,
        ignore_index=True,
    )

    result = (
        result.sort_values(
            [
                "ANO_REFERENCIA",
                "SERIE",
            ]
        )
        .reset_index(
            drop=True
        )
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_parquet(
        output_path,
        index=False,
    )

    return result