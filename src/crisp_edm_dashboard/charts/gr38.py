import matplotlib.pyplot as plt
import pandas as pd


def admission_form_chart(
    table: pd.DataFrame,
    year: int,
):
    """Gráfico das formas de ingresso."""

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    ax.barh(
        table["FORMA_INGRESSO"],
        table["TOTAL"],
    )

    ax.invert_yaxis()

    ax.set_title(
        "Ingressantes por Forma de Ingresso "
        f"— {year}"
    )

    ax.set_xlabel(
        "Número de ingressantes"
    )

    ax.set_ylabel(
        "Forma de ingresso"
    )

    fig.tight_layout()

    return fig


def age_band_chart(
    table: pd.DataFrame,
    year: int,
):
    """Distribuição dos ingressantes por faixa etária."""

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    ax.bar(
        table[
            "FAIXA_ETARIA"
        ].astype(str),
        table["TOTAL"],
    )

    ax.set_title(
        "Distribuição por Faixa Etária "
        f"— {year}"
    )

    ax.set_xlabel(
        "Faixa etária"
    )

    ax.set_ylabel(
        "Número de ingressantes"
    )

    ax.tick_params(
        axis="x",
        rotation=45,
    )

    fig.tight_layout()

    return fig


def age_band_by_admission_form_chart(
    table: pd.DataFrame,
    year: int,
):
    """Faixas etárias por forma de ingresso."""

    plot_table = (
        table.set_index(
            "FORMA_INGRESSO"
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    left = None

    for column in (
        plot_table.columns
    ):

        values = (
            plot_table[column]
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
        "Faixa Etária por Forma de Ingresso "
        f"— {year}"
    )

    ax.set_xlabel(
        "Número de ingressantes"
    )

    ax.set_ylabel(
        "Forma de ingresso"
    )

    ax.legend(
        title="Faixa etária"
    )

    fig.tight_layout()

    return fig


def sex_by_admission_form_chart(
    table: pd.DataFrame,
    year: int,
):
    """Comparação por sexo entre formas de ingresso."""

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    y_positions = range(
        len(table)
    )

    height = 0.35

    ax.barh(
        [
            value - height / 2
            for value in y_positions
        ],
        table[
            "MASCULINO"
        ],
        height=height,
        label="Masculino",
    )

    ax.barh(
        [
            value + height / 2
            for value in y_positions
        ],
        table[
            "FEMININO"
        ],
        height=height,
        label="Feminino",
    )

    ax.set_yticks(
        list(y_positions)
    )

    ax.set_yticklabels(
        table[
            "FORMA_INGRESSO"
        ]
    )

    ax.set_title(
        "Distribuição por Sexo e Forma de Ingresso "
        f"— {year}"
    )

    ax.set_xlabel(
        "Número de ingressantes"
    )

    ax.set_ylabel(
        "Forma de ingresso"
    )

    ax.legend(
        title="Sexo"
    )

    fig.tight_layout()

    return fig


def admission_form_evolution_chart(
    table: pd.DataFrame,
):
    """Evolução das formas de ingresso ao longo do tempo."""

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    for admission_form in (
        table[
            "FORMA_INGRESSO"
        ]
        .unique()
    ):

        filtered = table[
            table[
                "FORMA_INGRESSO"
            ]
            == admission_form
        ]

        ax.plot(
            filtered[
                "ANO_REFERENCIA"
            ],
            filtered["TOTAL"],
            marker="o",
            label=admission_form,
        )

    ax.set_title(
        "Evolução das Formas de Ingresso"
    )

    ax.set_xlabel(
        "Ano"
    )

    ax.set_ylabel(
        "Número de ingressantes"
    )

    ax.legend(
        title="Forma de ingresso",
        bbox_to_anchor=(
            1.02,
            1,
        ),
        loc="upper left",
    )

    fig.tight_layout()

    return fig