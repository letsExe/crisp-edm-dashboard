import matplotlib.pyplot as plt
import pandas as pd

from crisp_edm_dashboard.analysis.gr13 import (
    get_situation_columns,
)


def absolute_evolution_chart(
    yearly_table: pd.DataFrame,
):
    """Gráfico de evolução absoluta das situações."""

    situations = get_situation_columns(
        yearly_table
    )

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    for situation in situations:
        ax.plot(
            yearly_table["PERIODO_LETIVO"],
            yearly_table[situation],
            marker="o",
            label=situation,
        )

    ax.set_title(
        "Evolução das Situações Acadêmicas"
    )
    ax.set_xlabel("Ano letivo")
    ax.set_ylabel("Quantidade de acadêmicos")
    ax.legend()

    fig.tight_layout()

    return fig


def percentage_evolution_chart(
    yearly_table: pd.DataFrame,
):
    """Gráfico de evolução percentual das situações."""

    percentage_columns = [
        column
        for column in yearly_table.columns
        if column.startswith("% ")
    ]

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    for column in percentage_columns:
        label = column.removeprefix("% ")

        ax.plot(
            yearly_table["PERIODO_LETIVO"],
            yearly_table[column],
            marker="o",
            label=label,
        )

    ax.set_title(
        "Evolução Percentual das Situações Acadêmicas"
    )
    ax.set_xlabel("Ano letivo")
    ax.set_ylabel("Percentual (%)")
    ax.legend()

    fig.tight_layout()

    return fig