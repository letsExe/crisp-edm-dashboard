import pandas as pd

from crisp_edm_dashboard.tables.gr14 import (
    create_discipline_table,
    create_year_discipline_table,
)


SERIES_ORDER = {
    "1º ano": 1,
    "2º ano": 2,
    "3º ano": 3,
    "4º ano": 4,
}


def get_years(
    df: pd.DataFrame,
) -> list[int]:
    """Retorna os anos disponíveis."""

    return sorted(
        df["ANO"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )


def get_disciplines(
    df: pd.DataFrame,
    year: int | None = None,
) -> list[str]:
    """
    Retorna as disciplinas disponíveis.

    Se year for informado, retorna apenas
    disciplinas daquele ano.
    """

    filtered = df

    if year is not None:
        filtered = df[
            df["ANO"] == year
        ]

    return sorted(
        filtered["DISCIPLINA"]
        .dropna()
        .unique()
        .tolist()
    )


def discipline_details(
    df: pd.DataFrame,
    year: int,
    discipline: str,
) -> dict:
    """Retorna os indicadores de uma disciplina em um ano."""

    discipline_table = (
        create_discipline_table(
            df
        )
    )

    filtered = discipline_table[
        (
            discipline_table["ANO"]
            == year
        )
        & (
            discipline_table[
                "DISCIPLINA"
            ]
            == discipline
        )
    ]

    if filtered.empty:
        raise ValueError(
            "Disciplina não encontrada "
            f"no ano {year}: {discipline}"
        )

    total_failed = int(
        filtered[
            "REPROVADOS"
        ].sum()
    )

    total_approved = int(
        filtered[
            "APROVADOS"
        ].sum()
    )

    total_students = (
        total_failed
        + total_approved
    )

    failure_rate = (
        (
            total_failed
            / total_students
            * 100
        )
        if total_students
        else 0.0
    )

    approval_rate = (
        (
            total_approved
            / total_students
            * 100
        )
        if total_students
        else 0.0
    )

    series = sorted(
        filtered["SERIE"]
        .unique()
        .tolist(),
        key=lambda value: (
            SERIES_ORDER.get(
                value,
                999,
            )
        ),
    )

    return {
        "ANO": year,
        "DISCIPLINA": discipline,
        "TOTAL_ALUNOS": total_students,
        "REPROVADOS": total_failed,
        "APROVADOS": total_approved,
        "TAXA_REPROVACAO": failure_rate,
        "TAXA_APROVACAO": approval_rate,
        "SERIE": " / ".join(series),
    }


def top_disciplines_by_failures(
    df: pd.DataFrame,
    year: int,
    n: int = 3,
) -> pd.DataFrame:
    """
    Retorna as disciplinas com maior NÚMERO
    absoluto de reprovações em determinado ano.
    """

    table = (
        create_year_discipline_table(
            df
        )
    )

    filtered = table[
        table["ANO"] == year
    ].copy()

    filtered = (
        filtered.sort_values(
            [
                "REPROVADOS",
                "TAXA_REPROVACAO",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .head(n)
    )

    return filtered[
        [
            "DISCIPLINA",
            "REPROVADOS",
            "TOTAL_ALUNOS",
            "TAXA_REPROVACAO",
        ]
    ].reset_index(drop=True)


def discipline_evolution(
    df: pd.DataFrame,
    discipline: str,
) -> pd.DataFrame:
    """Evolução anual de uma disciplina."""

    table = (
        create_year_discipline_table(
            df
        )
    )

    result = table[
        table["DISCIPLINA"]
        == discipline
    ].copy()

    return (
        result.sort_values(
            "ANO"
        )
        .reset_index(drop=True)
    )


def failure_summary_by_series(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula a taxa GLOBAL de reprovação por série.

    A taxa é calculada por:
        total de reprovações / total de alunos * 100

    Dessa forma, disciplinas com poucos alunos
    não recebem o mesmo peso de disciplinas
    com muitas matrículas.
    """

    table = (
        create_discipline_table(
            df
        )
    )

    summary = (
        table.groupby(
            "SERIE",
            as_index=False,
        )
        .agg(
            REPROVADOS=(
                "REPROVADOS",
                "sum",
            ),
            APROVADOS=(
                "APROVADOS",
                "sum",
            ),
            TOTAL_ALUNOS=(
                "TOTAL_ALUNOS",
                "sum",
            ),
        )
    )

    summary[
        "TAXA_REPROVACAO"
    ] = (
        summary["REPROVADOS"]
        .div(
            summary["TOTAL_ALUNOS"]
            .replace(0, pd.NA)
        )
        .mul(100)
    )

    summary["ORDEM"] = (
        summary["SERIE"]
        .map(SERIES_ORDER)
        .fillna(999)
    )

    summary = (
        summary.sort_values(
            "ORDEM"
        )
        .drop(
            columns="ORDEM"
        )
        .reset_index(drop=True)
    )

    return summary