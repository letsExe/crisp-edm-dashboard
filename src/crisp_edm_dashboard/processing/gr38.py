import re

import pandas as pd

from crisp_edm_dashboard.config import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
)
from crisp_edm_dashboard.loaders.excel import (
    read_excel,
)
from crisp_edm_dashboard.utils.columns import (
    normalize_columns,
)


GR38_INPUT = (
    RAW_DATA_DIR
    / "gr38"
    / "GR38.xlsx"
)

GR38_OUTPUT = (
    PROCESSED_DATA_DIR
    / "gr38.parquet"
)

GR38_AUDIT_OUTPUT = (
    PROCESSED_DATA_DIR
    / "gr38_all_schemes.parquet"
)


# ---------------------------------------------------------
# A planilha possui três esquemas sobrepostos de faixa etária.
# Cada estudante aparece uma vez em cada esquema.
# ---------------------------------------------------------

AGE_SCHEME_1 = {
    "até 18 anos",
    "19 a 24 anos",
    "25 a 30 anos",
    "31 a 40 anos",
    "41 a 50 anos",
    "acima de 50 anos",
}

AGE_SCHEME_2 = {
    "18 a 24 anos",
    "25 a 29 anos",
    "30 a 34 anos",
    "35 a 39 anos",
    "40 a 44 anos",
    "45 a 49 anos",
    "50 a 54 anos",
    "55 a 59 anos",
}

AGE_SCHEME_3 = {
    "18 a 20 anos",
    "21 a 23 anos",
    "24 a 26 anos",
    "27 a 29 anos",
    "acima de 29 anos",
}


CANONICAL_AGE_SCHEME = "ESQUEMA_1"


AGE_BAND_MAP = {
    "até 18 anos": "Até 18 anos",
    "19 a 24 anos": "19–24 anos",
    "25 a 30 anos": "25–30 anos",
    "31 a 40 anos": "31–40 anos",
    "41 a 50 anos": "41–50 anos",
    "acima de 50 anos": "51+ anos",
}


def normalize_whitespace(
    value,
) -> str:
    """Remove espaços duplicados e espaços externos."""

    if pd.isna(value):
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value),
    ).strip()


def identify_age_scheme(
    value,
) -> str:
    """Identifica a qual esquema de faixa etária pertence a linha."""

    text = (
        normalize_whitespace(value)
        .lower()
    )

    if text in AGE_SCHEME_1:
        return "ESQUEMA_1"

    if text in AGE_SCHEME_2:
        return "ESQUEMA_2"

    if text in AGE_SCHEME_3:
        return "ESQUEMA_3"

    raise ValueError(
        "Faixa etária não reconhecida no GR38: "
        f"{value}"
    )


def normalize_age_band(
    value,
) -> str:
    """Padroniza as faixas utilizadas no esquema canônico."""

    text = (
        normalize_whitespace(value)
        .lower()
    )

    return AGE_BAND_MAP.get(
        text,
        normalize_whitespace(value),
    )


def validate_scheme_consistency(
    df: pd.DataFrame,
) -> None:
    """
    Verifica se os três esquemas representam
    a mesma população em cada ano e forma de ingresso.

    Os totais de estudantes, masculino e feminino
    devem ser idênticos entre os três esquemas.
    """

    expected_schemes = {
        "ESQUEMA_1",
        "ESQUEMA_2",
        "ESQUEMA_3",
    }

    for metric in [
        "TOTAL",
        "MASCULINO",
        "FEMININO",
    ]:

        pivot = df.pivot_table(
            index=[
                "ANO_REFERENCIA",
                "FORMA_INGRESSO",
            ],
            columns="ESQUEMA_FAIXA",
            values=metric,
            aggfunc="sum",
            fill_value=0,
        )

        missing_schemes = (
            expected_schemes
            - set(pivot.columns)
        )

        if missing_schemes:
            raise ValueError(
                "Nem todos os esquemas de faixa etária "
                "foram encontrados no GR38. "
                f"Faltando: {sorted(missing_schemes)}"
            )

        inconsistent = (
            pivot[
                [
                    "ESQUEMA_1",
                    "ESQUEMA_2",
                    "ESQUEMA_3",
                ]
            ]
            .nunique(axis=1)
            > 1
        )

        if inconsistent.any():

            problem_rows = (
                pivot[
                    inconsistent
                ]
            )

            raise ValueError(
                "Os três esquemas de faixa etária "
                f"não possuem os mesmos valores para {metric}.\n"
                f"{problem_rows}"
            )


def process_gr38(
    input_path=GR38_INPUT,
    output_path=GR38_OUTPUT,
    audit_output_path=GR38_AUDIT_OUTPUT,
) -> pd.DataFrame:
    """
    Limpa o GR38 e seleciona um único esquema
    de faixa etária para evitar tripla contagem
    dos ingressantes.
    """

    df = read_excel(
        input_path
    )

    df = normalize_columns(
        df
    )

    required_columns = {
        "PERIODO_LETIVO",
        "CURSO",
        "FORMA_DE_INGRESSO",
        "IDADE",
        "FAIXA_ETARIA",
        "MASCULINO",
        "FEMININO",
        "TOTAL",
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "O GR38 não possui todas as colunas esperadas. "
            f"Faltando: {sorted(missing_columns)}"
        )

    # -----------------------------------------------------
    # Campos numéricos
    # -----------------------------------------------------

    df["PERIODO_LETIVO"] = pd.to_numeric(
        df["PERIODO_LETIVO"],
        errors="coerce",
    )

    df["IDADE"] = pd.to_numeric(
        df["IDADE"],
        errors="coerce",
    )

    df["MASCULINO"] = pd.to_numeric(
        df["MASCULINO"],
        errors="coerce",
    )

    df["FEMININO"] = pd.to_numeric(
        df["FEMININO"],
        errors="coerce",
    )

    df["TOTAL"] = pd.to_numeric(
        df["TOTAL"],
        errors="coerce",
    )

    # -----------------------------------------------------
    # Remover cabeçalhos repetidos e linhas vazias
    # -----------------------------------------------------

    df = df.dropna(
        subset=[
            "PERIODO_LETIVO",
            "FORMA_DE_INGRESSO",
            "FAIXA_ETARIA",
            "TOTAL",
        ]
    )

    df["PERIODO_LETIVO"] = (
        df["PERIODO_LETIVO"]
        .astype(int)
    )

    df["MASCULINO"] = (
        df["MASCULINO"]
        .fillna(0)
        .astype(int)
    )

    df["FEMININO"] = (
        df["FEMININO"]
        .fillna(0)
        .astype(int)
    )

    df["TOTAL"] = (
        df["TOTAL"]
        .astype(int)
    )

    # -----------------------------------------------------
    # Validação do total
    # -----------------------------------------------------

    invalid_total = (
        df["TOTAL"]
        != (
            df["MASCULINO"]
            + df["FEMININO"]
        )
    )

    if invalid_total.any():
        raise ValueError(
            "Foram encontrados registros do GR38 "
            "em que TOTAL é diferente de "
            "MASCULINO + FEMININO."
        )

    # -----------------------------------------------------
    # Padronização textual
    # -----------------------------------------------------

    df["CURSO"] = (
        df["CURSO"]
        .apply(
            normalize_whitespace
        )
    )

    df["FORMA_DE_INGRESSO"] = (
        df["FORMA_DE_INGRESSO"]
        .apply(
            normalize_whitespace
        )
    )

    df["FAIXA_ETARIA"] = (
        df["FAIXA_ETARIA"]
        .apply(
            normalize_whitespace
        )
    )

    # -----------------------------------------------------
    # Identificação dos três esquemas
    # -----------------------------------------------------

    df["ESQUEMA_FAIXA"] = (
        df["FAIXA_ETARIA"]
        .apply(
            identify_age_scheme
        )
    )

    df = df.rename(
        columns={
            "PERIODO_LETIVO":
                "ANO_REFERENCIA",
            "FORMA_DE_INGRESSO":
                "FORMA_INGRESSO",
            "IDADE":
                "IDADE_ORIGINAL",
        }
    )

    # -----------------------------------------------------
    # Confirmar que os três esquemas representam
    # exatamente a mesma população
    # -----------------------------------------------------

    validate_scheme_consistency(
        df
    )

    # -----------------------------------------------------
    # Salvar a base completa apenas para auditoria
    # -----------------------------------------------------

    audit_output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        audit_output_path,
        index=False,
    )

    # -----------------------------------------------------
    # Selecionar um único esquema para a análise
    # -----------------------------------------------------

    canonical = df[
        df["ESQUEMA_FAIXA"]
        == CANONICAL_AGE_SCHEME
    ].copy()

    canonical["FAIXA_ETARIA"] = (
        canonical["FAIXA_ETARIA"]
        .apply(
            normalize_age_band
        )
    )

    canonical = canonical[
        [
            "ANO_REFERENCIA",
            "CURSO",
            "FORMA_INGRESSO",
            "FAIXA_ETARIA",
            "MASCULINO",
            "FEMININO",
            "TOTAL",
        ]
    ]

    canonical = (
        canonical.sort_values(
            [
                "ANO_REFERENCIA",
                "FORMA_INGRESSO",
                "FAIXA_ETARIA",
            ]
        )
        .reset_index(
            drop=True
        )
    )

    canonical.to_parquet(
        output_path,
        index=False,
    )

    return canonical