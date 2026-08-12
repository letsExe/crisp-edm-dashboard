import pandas as pd


def get_situation_columns(
    yearly_table: pd.DataFrame,
) -> list[str]:
    """Retorna apenas as colunas absolutas de situação."""

    excluded = {
        "PERIODO_LETIVO",
        "Total",
    }

    return [
        column
        for column in yearly_table.columns
        if column not in excluded
        and not column.startswith("% ")
    ]


def descriptive_statistics(
    yearly_table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula estatísticas descritivas para
    cada situação acadêmica.
    """

    situations = get_situation_columns(
        yearly_table
    )

    stats = (
        yearly_table[situations]
        .describe(
            percentiles=[
                0.25,
                0.50,
                0.75,
            ]
        )
        .T
        .reset_index()
    )

    stats = stats.rename(
        columns={
            "index": "Situação",
            "count": "Anos",
            "mean": "Média",
            "std": "Desvio padrão",
            "min": "Mínimo",
            "25%": "1º Quartil",
            "50%": "Mediana",
            "75%": "3º Quartil",
            "max": "Máximo",
        }
    )

    return stats


def peaks_and_valleys(
    yearly_table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identifica o maior e o menor valor registrado
    para cada situação acadêmica.
    """

    situations = get_situation_columns(
        yearly_table
    )

    results = []

    for situation in situations:
        series = yearly_table[
            [
                "PERIODO_LETIVO",
                situation,
            ]
        ]

        peak_row = series.loc[
            series[situation].idxmax()
        ]

        valley_row = series.loc[
            series[situation].idxmin()
        ]

        results.append(
            {
                "Situação": situation,
                "Ano do pico": int(
                    peak_row["PERIODO_LETIVO"]
                ),
                "Pico": int(
                    peak_row[situation]
                ),
                "Ano do vale": int(
                    valley_row["PERIODO_LETIVO"]
                ),
                "Vale": int(
                    valley_row[situation]
                ),
            }
        )

    return pd.DataFrame(results)