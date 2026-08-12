import matplotlib.pyplot as plt
import pandas as pd


def sex_distribution_chart(
    table: pd.DataFrame,
):
    """Gráfico da distribuição por sexo."""

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        table["SEXO"],
        table["QUANTIDADE"],
    )

    ax.set_title(
        "Distribuição por Sexo"
    )

    ax.set_xlabel(
        "Sexo"
    )

    ax.set_ylabel(
        "Número de acadêmicos"
    )

    fig.tight_layout()

    return fig


def age_band_distribution_chart(
    table: pd.DataFrame,
):
    """Gráfico da distribuição por faixa etária."""

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ax.bar(
        table[
            "FAIXA_ETARIA"
        ],
        table[
            "QUANTIDADE"
        ],
    )

    ax.set_title(
        "Distribuição por Faixa Etária"
    )

    ax.set_xlabel(
        "Faixa etária"
    )

    ax.set_ylabel(
        "Número de acadêmicos"
    )

    ax.tick_params(
        axis="x",
        rotation=45,
    )

    fig.tight_layout()

    return fig


def sex_by_series_chart(
    table: pd.DataFrame,
):
    """Gráfico empilhado de sexo por série."""

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    series = table[
        "SERIE"
    ]

    sex_columns = [
        column
        for column in table.columns
        if column != "SERIE"
    ]

    bottom = None

    for sex in sex_columns:

        values = table[
            sex
        ]

        ax.bar(
            series,
            values,
            bottom=bottom,
            label=sex,
        )

        if bottom is None:
            bottom = values.copy()
        else:
            bottom = (
                bottom
                + values
            )

    ax.set_title(
        "Distribuição por Sexo e Série"
    )

    ax.set_xlabel(
        "Série"
    )

    ax.set_ylabel(
        "Número de acadêmicos"
    )

    ax.set_xticks(
        [1, 2, 3, 4]
    )

    ax.legend(
        title="Sexo"
    )

    fig.tight_layout()

    return fig


def position_by_race_chart(
    table: pd.DataFrame,
    year: int,
):
    """
    Gráfico percentual da posição curricular
    por cor/raça.
    """

    plot_table = (
        table.set_index(
            "COR_RACA"
        )
    )

    fig, ax = plt.subplots(
        figsize=(9, 6)
    )

    left = None

    for column in (
        plot_table.columns
    ):

        values = (
            plot_table[
                column
            ]
        )

        ax.barh(
            plot_table.index,
            values,
            left=left,
            label=column,
        )

        if left is None:
            left = values.copy()
        else:
            left = (
                left
                + values
            )

    ax.set_title(
        "Posição Curricular por Cor/Raça "
        f"— {year}"
    )

    ax.set_xlabel(
        "Percentual de acadêmicos (%)"
    )

    ax.set_ylabel(
        "Cor/raça"
    )

    ax.set_xlim(
        0,
        100,
    )

    ax.legend(
        title="Posição no curso"
    )

    fig.tight_layout()

    return fig


def age_band_by_series_chart(
    table: pd.DataFrame,
):
    """
    Gráfico empilhado de faixas etárias
    por série.
    """

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    series = table[
        "SERIE"
    ]

    columns = [
        column
        for column in table.columns
        if column != "SERIE"
    ]

    bottom = None

    for column in columns:

        values = table[
            column
        ]

        ax.bar(
            series,
            values,
            bottom=bottom,
            label=column,
        )

        if bottom is None:
            bottom = values.copy()
        else:
            bottom = (
                bottom
                + values
            )

    ax.set_title(
        "Distribuição de Faixa Etária por Série"
    )

    ax.set_xlabel(
        "Série"
    )

    ax.set_ylabel(
        "Número de acadêmicos"
    )

    ax.set_xticks(
        [1, 2, 3, 4]
    )

    ax.legend(
        title="Faixa etária"
    )

    fig.tight_layout()

    return fig