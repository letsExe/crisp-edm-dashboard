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


GR14_INPUT = (
    RAW_DATA_DIR
    / "gr14"
    / "GR14.xlsx"
)

GR14_OUTPUT = (
    PROCESSED_DATA_DIR
    / "gr14.parquet"
)


COLUMN_RENAME = {
    "ANO_LETIVO": "SERIE",
    "CODIGO_DE_DICIPLINA": "CODIGO_DISCIPLINA",
    "DESCRICAO_DICIPLINA": "DISCIPLINA",
    "APROVADOS": "APROVADOS",
    "REPROVADOS": "REPROVADOS",
    "APROVADOS": "APROVADOS",
    "REPROVADOS": "REPROVADOS",
}


def normalize_whitespace(
    value: str,
) -> str:
    """Remove espaços duplicados e espaços externos."""

    return re.sub(
        r"\s+",
        " ",
        str(value),
    ).strip()


def normalize_series(
    value: str,
) -> str:
    """
    Padroniza a série do curso.

    Exemplos:
        1 ano  -> 1º ano
        1° ano -> 1º ano
        1º ano -> 1º ano
    """

    value = normalize_whitespace(
        value
    ).lower()

    match = re.search(
        r"([1-9])",
        value,
    )

    if match:
        return (
            f"{match.group(1)}º ano"
        )

    return value


def process_gr14(
    input_path=GR14_INPUT,
    output_path=GR14_OUTPUT,
) -> pd.DataFrame:
    """
    Lê todas as abas do GR14, valida os dados,
    padroniza as variáveis e gera a base
    processada em Parquet.
    """

    sheets = read_all_sheets(
        input_path
    )

    frames = []

    for sheet_name, sheet_df in sheets.items():
        try:
            sheet_year = int(
                str(sheet_name).strip()
            )
        except ValueError as error:
            raise ValueError(
                "O nome da aba do GR14 deve representar "
                f"um ano. Aba encontrada: {sheet_name}"
            ) from error

        df = normalize_columns(
            sheet_df
        )

        df = df.rename(
            columns=COLUMN_RENAME
        )

        required_columns = {
            "ANO",
            "CURSO",
            "SERIE",
            "CODIGO_DISCIPLINA",
            "DISCIPLINA",
            "REPROVADOS",
            "APROVADOS",
        }

        missing_columns = (
            required_columns
            - set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                f"A aba {sheet_name} do GR14 "
                "não possui todas as colunas esperadas. "
                f"Faltando: {sorted(missing_columns)}"
            )

        # -----------------------------------
        # Conferência do ano
        # -----------------------------------

        original_year = pd.to_numeric(
            df["ANO"],
            errors="coerce",
        )

        mismatch = (
            original_year.notna()
            & (
                original_year
                != sheet_year
            )
        )

        if mismatch.any():
            raise ValueError(
                "Foram encontrados registros cujo "
                f"ANO não corresponde à aba {sheet_name}."
            )

        # O nome da aba será nossa referência
        # oficial para o ano.
        df["ANO"] = sheet_year

        # -----------------------------------
        # Padronização textual
        # -----------------------------------

        df["CURSO"] = (
            df["CURSO"]
            .apply(normalize_whitespace)
        )

        df["SERIE"] = (
            df["SERIE"]
            .apply(normalize_series)
        )

        df["DISCIPLINA"] = (
            df["DISCIPLINA"]
            .apply(normalize_whitespace)
        )

        df["CODIGO_DISCIPLINA"] = (
            df["CODIGO_DISCIPLINA"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # -----------------------------------
        # Campos numéricos
        # -----------------------------------

        df["REPROVADOS"] = pd.to_numeric(
            df["REPROVADOS"],
            errors="coerce",
        )

        df["APROVADOS"] = pd.to_numeric(
            df["APROVADOS"],
            errors="coerce",
        )

        # -----------------------------------
        # Registros inválidos
        # -----------------------------------

        df = df.dropna(
            subset=[
                "ANO",
                "SERIE",
                "DISCIPLINA",
                "REPROVADOS",
                "APROVADOS",
            ]
        )

        df["REPROVADOS"] = (
            df["REPROVADOS"]
            .astype(int)
        )

        df["APROVADOS"] = (
            df["APROVADOS"]
            .astype(int)
        )

        df = df[
            (df["REPROVADOS"] >= 0)
            & (df["APROVADOS"] >= 0)
        ]

        # -----------------------------------
        # Indicadores
        # -----------------------------------

        df["TOTAL_ALUNOS"] = (
            df["REPROVADOS"]
            + df["APROVADOS"]
        )

        # Não usamos os percentuais fornecidos
        # pelo Excel. Eles são recalculados
        # diretamente a partir das contagens.

        df["TAXA_REPROVACAO"] = (
            df["REPROVADOS"]
            .div(
                df["TOTAL_ALUNOS"]
                .replace(0, pd.NA)
            )
            .mul(100)
        )

        df["TAXA_APROVACAO"] = (
            df["APROVADOS"]
            .div(
                df["TOTAL_ALUNOS"]
                .replace(0, pd.NA)
            )
            .mul(100)
        )

        # -----------------------------------
        # Seleção das colunas
        # -----------------------------------

        df = df[
            [
                "ANO",
                "CURSO",
                "SERIE",
                "CODIGO_DISCIPLINA",
                "DISCIPLINA",
                "REPROVADOS",
                "APROVADOS",
                "TOTAL_ALUNOS",
                "TAXA_REPROVACAO",
                "TAXA_APROVACAO",
            ]
        ]

        frames.append(
            df
        )

    result = pd.concat(
        frames,
        ignore_index=True,
    )

    result = result.sort_values(
        [
            "ANO",
            "SERIE",
            "DISCIPLINA",
            "CODIGO_DISCIPLINA",
        ]
    ).reset_index(drop=True)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_parquet(
        output_path,
        index=False,
    )

    return result