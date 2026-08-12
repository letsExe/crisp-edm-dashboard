import pandas as pd
import streamlit as st

from crisp_edm_dashboard.analysis.gr16 import (
    age_statistics,
    filter_by_year,
    get_years,
)
from crisp_edm_dashboard.charts.gr16 import (
    age_band_by_series_chart,
    age_band_distribution_chart,
    position_by_race_chart,
    sex_by_series_chart,
    sex_distribution_chart,
)
from crisp_edm_dashboard.config import (
    PROCESSED_DATA_DIR,
)
from crisp_edm_dashboard.tables.gr16 import (
    age_band_by_series,
    age_band_distribution,
    position_by_race,
    race_distribution,
    sex_by_series,
    sex_distribution,
)


GR16_DATA = (
    PROCESSED_DATA_DIR
    / "gr16.parquet"
)


@st.cache_data
def load_gr16() -> pd.DataFrame:
    """Carrega a base processada do GR16."""

    return pd.read_parquet(
        GR16_DATA
    )


def render() -> None:

    st.title(
        "👥 Perfil Discente — GR16"
    )

    st.write(
        """
        Análise descritiva do perfil dos acadêmicos
        do curso de Ciência da Computação,
        considerando idade, sexo, faixa etária,
        cor/raça e série.
        """
    )

    if not GR16_DATA.exists():

        st.error(
            "A base processada do GR16 ainda não existe. "
            "Execute primeiro: "
            "`poetry run python scripts/process_all.py`"
        )

        return

    df = load_gr16()

    years = get_years(
        df
    )

    selected_year = st.selectbox(
        "Ano de referência",
        years,
        key="gr16_year",
    )

    df_year = filter_by_year(
        df,
        selected_year,
    )

    st.caption(
        f"Análises referentes ao ano de {selected_year}."
    )

    # ===================================
    # RESUMO
    # ===================================

    total_students = len(
        df_year
    )

    mean_age = (
        df_year[
            "IDADE"
        ]
        .mean()
    )

    female_count = int(
        (
            df_year[
                "SEXO"
            ]
            == "F"
        ).sum()
    )

    male_count = int(
        (
            df_year[
                "SEXO"
            ]
            == "M"
        ).sum()
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Total de acadêmicos",
        total_students,
        border=True,
    )

    col2.metric(
        "Idade média",
        f"{mean_age:.2f}",
        border=True,
    )

    col3.metric(
        "Sexo feminino",
        female_count,
        border=True,
    )

    col4.metric(
        "Sexo masculino",
        male_count,
        border=True,
    )

    st.divider()

    # ===================================
    # IDADE
    # ===================================

    st.header(
        "📅 Análise descritiva da idade"
    )

    stats = age_statistics(
        df_year
    )

    stats_display = (
        stats.copy()
    )

    stats_display[
        "Valor"
    ] = (
        stats_display[
            "Valor"
        ]
        .apply(
            lambda value: (
                f"{value:.2f}"
                if isinstance(
                    value,
                    float,
                )
                and not value.is_integer()
                else f"{value:.0f}"
            )
        )
    )

    st.dataframe(
        stats_display,
        width="stretch",
        hide_index=True,
    )

    # ===================================
    # COR / RAÇA
    # ===================================

    st.subheader(
        "Distribuição por cor/raça"
    )

    race_table = (
        race_distribution(
            df_year
        )
    )

    race_display = (
        race_table.rename(
            columns={
                "COR_RACA":
                    "Cor/Raça",
                "TOTAL_ALUNOS":
                    "Total de acadêmicos",
                "PERCENTUAL":
                    "Percentual (%)",
            }
        )
        .copy()
    )

    race_display[
        "Percentual (%)"
    ] = (
        race_display[
            "Percentual (%)"
        ]
        .round(2)
    )

    st.dataframe(
        race_display,
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # ===================================
    # SEXO E FAIXA ETÁRIA
    # ===================================

    col_left, col_right = (
        st.columns(2)
    )

    with col_left:

        st.header(
            "Distribuição por sexo"
        )

        sex_table = (
            sex_distribution(
                df_year
            )
        )

        fig_sex = (
            sex_distribution_chart(
                sex_table
            )
        )

        st.pyplot(
            fig_sex,
            clear_figure=True,
        )

    with col_right:

        st.header(
            "Distribuição por faixa etária"
        )

        age_band_table = (
            age_band_distribution(
                df_year
            )
        )

        fig_age_band = (
            age_band_distribution_chart(
                age_band_table
            )
        )

        st.pyplot(
            fig_age_band,
            clear_figure=True,
        )

    st.divider()

    # ===================================
    # POSIÇÃO NO CURSO / COR-RAÇA
    # ===================================

    st.header(
        "🧭 Posição no curso por cor/raça"
    )

    st.write(
        """
        A análise compara os acadêmicos matriculados
        nas séries 1–3 com aqueles matriculados na
        série final do curso.

        **A presença na 4ª série não significa que o
        acadêmico seja efetivamente concluinte.**
        """
    )

    position_table = (
        position_by_race(
            df_year
        )
    )

    fig_position = (
        position_by_race_chart(
            position_table,
            selected_year,
        )
    )

    st.pyplot(
        fig_position,
        clear_figure=True,
    )

    with st.expander(
        "Ver tabela de percentuais"
    ):

        position_display = (
            position_table
            .copy()
            .rename(
                columns={
                    "COR_RACA":
                        "Cor/Raça",
                }
            )
        )

        numeric_columns = (
            position_display
            .select_dtypes(
                include="number"
            )
            .columns
        )

        position_display[
            numeric_columns
        ] = (
            position_display[
                numeric_columns
            ]
            .round(2)
        )

        st.dataframe(
            position_display,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ===================================
    # SEXO POR SÉRIE
    # ===================================

    st.header(
        "🎓 Distribuição por sexo e série"
    )

    sex_series_table = (
        sex_by_series(
            df_year
        )
    )

    fig_sex_series = (
        sex_by_series_chart(
            sex_series_table
        )
    )

    st.pyplot(
        fig_sex_series,
        clear_figure=True,
    )

    # ===================================
    # FAIXA ETÁRIA POR SÉRIE
    # ===================================

    with st.expander(
        "Ver distribuição de faixa etária por série"
    ):

        age_series_table = (
            age_band_by_series(
                df_year
            )
        )

        fig_age_series = (
            age_band_by_series_chart(
                age_series_table
            )
        )

        st.pyplot(
            fig_age_series,
            clear_figure=True,
        )