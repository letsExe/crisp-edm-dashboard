import matplotlib.pyplot as plt
import pandas as pd


def discipline_evolution_chart(
    evolution: pd.DataFrame,
    discipline: str,
    metric: str = "Quantidade de reprovações",
):
    """
    Cria gráfico temporal da disciplina.

    metric:
        Quantidade de reprovações
        Taxa de reprovação (%)
    """

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    if metric == "Taxa de reprovação (%)":
        y_column = (
            "TAXA_REPROVACAO"
        )
        y_label = (
            "Taxa de reprovação (%)"
        )
        title = (
            "Evolução da Taxa de Reprovação"
        )
    else:
        y_column = "REPROVADOS"
        y_label = (
            "Quantidade de reprovações"
        )
        title = (
            "Evolução das Reprovações"
        )

    ax.plot(
        evolution["ANO"],
        evolution[y_column],
        marker="o",
    )

    ax.set_title(
        f"{title} — {discipline}"
    )

    ax.set_xlabel(
        "Ano"
    )

    ax.set_ylabel(
        y_label
    )

    ax.grid(
        alpha=0.3
    )

    fig.tight_layout()

    return fig


def series_failure_chart(
    summary: pd.DataFrame,
):
    """Gráfico da taxa global de reprovação por série."""

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    bars = ax.bar(
        summary["SERIE"],
        summary[
            "TAXA_REPROVACAO"
        ],
    )

    ax.set_title(
        "Taxa Global de Reprovação por Série"
    )

    ax.set_xlabel(
        "Série"
    )

    ax.set_ylabel(
        "Taxa de reprovação (%)"
    )

    for bar, value in zip(
        bars,
        summary["TAXA_REPROVACAO"],
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}%",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()

    return fig