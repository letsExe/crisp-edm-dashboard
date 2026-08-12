import pandas as pd


def create_discipline_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Agrupa os registros por ano, série e disciplina.

    Diferentes códigos curriculares com a mesma
    descrição são consolidados dentro da mesma
    combinação ano + série + disciplina.
    """

    table = (
        df.groupby(
            [
                "ANO",
                "SERIE",
                "DISCIPLINA",
            ],
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
        )
    )

    table["TOTAL_ALUNOS"] = (
        table["REPROVADOS"]
        + table["APROVADOS"]
    )

    table["TAXA_REPROVACAO"] = (
        table["REPROVADOS"]
        .div(
            table["TOTAL_ALUNOS"]
            .replace(0, pd.NA)
        )
        .mul(100)
    )

    table["TAXA_APROVACAO"] = (
        table["APROVADOS"]
        .div(
            table["TOTAL_ALUNOS"]
            .replace(0, pd.NA)
        )
        .mul(100)
    )

    return table


def create_year_discipline_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Consolida cada disciplina dentro de um ano.

    Essa tabela é usada quando uma disciplina
    aparece associada a mais de uma série.
    """

    discipline_table = (
        create_discipline_table(
            df
        )
    )

    table = (
        discipline_table.groupby(
            [
                "ANO",
                "DISCIPLINA",
            ],
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

    table["TAXA_REPROVACAO"] = (
        table["REPROVADOS"]
        .div(
            table["TOTAL_ALUNOS"]
            .replace(0, pd.NA)
        )
        .mul(100)
    )

    table["TAXA_APROVACAO"] = (
        table["APROVADOS"]
        .div(
            table["TOTAL_ALUNOS"]
            .replace(0, pd.NA)
        )
        .mul(100)
    )

    return table