import pandas as pd
import streamlit as st

from crisp_edm_dashboard.analysis.gr13 import (
    descriptive_statistics,
    peaks_and_valleys,
)
from crisp_edm_dashboard.charts.gr13 import (
    absolute_evolution_chart,
    percentage_evolution_chart,
)
from crisp_edm_dashboard.config import (
    ARTICLE_END_YEAR,
    ARTICLE_START_YEAR,
    PROCESSED_DATA_DIR,
)
from crisp_edm_dashboard.tables.gr13 import (
    create_yearly_status_table,
)


GR13_DATA = (
    PROCESSED_DATA_DIR
    / "gr13.parquet"
)


@st.cache_data
def load_gr13() -> pd.DataFrame:
    """Carrega a base processada do GR13."""

    return pd.read_parquet(
        GR13_DATA
    )


def render() -> None:
    st.title(
        "Situação Acadêmica — GR13"
    )

    st.write(
        "Análise longitudinal das situações "
        "acadêmicas registradas no curso."
    )

    if not GR13_DATA.exists():
        st.error(
            "A base processada do GR13 ainda não existe. "
            "Execute primeiro: "
            "`poetry run python scripts/process_all.py`"
        )
        return

    df = load_gr13()

    min_year = int(
        df["PERIODO_LETIVO"].min()
    )

    max_year = int(
        df["PERIODO_LETIVO"].max()
    )

    default_start = max(
        min_year,
        ARTICLE_START_YEAR,
    )

    default_end = min(
        max_year,
        ARTICLE_END_YEAR,
    )

    if default_start > default_end:
        default_start = min_year
        default_end = max_year

    selected_period = st.slider(
        "Período da análise",
        min_value=min_year,
        max_value=max_year,
        value=(
            default_start,
            default_end,
        ),
    )

    start_year, end_year = selected_period

    filtered_df = df[
        df["PERIODO_LETIVO"].between(
            start_year,
            end_year,
        )
    ]

    yearly_table = (
        create_yearly_status_table(
            filtered_df
        )
    )

    st.caption(
        "Para o artigo científico, o período "
        f"de referência está definido como "
        f"{ARTICLE_START_YEAR}–{ARTICLE_END_YEAR}."
    )

    # -----------------------------------
    # Tabela principal
    # -----------------------------------

    st.subheader(
        "Tabela anual"
    )

    st.dataframe(
        yearly_table.round(2),
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------
    # Estatísticas
    # -----------------------------------

    st.subheader(
        "Estatísticas descritivas"
    )

    stats = descriptive_statistics(
        yearly_table
    )

    st.dataframe(
        stats.round(2),
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------
    # Picos e vales
    # -----------------------------------

    st.subheader(
        "Picos e vales"
    )

    peaks = peaks_and_valleys(
        yearly_table
    )

    st.dataframe(
        peaks,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------
    # Evolução absoluta
    # -----------------------------------

    st.subheader(
        "Evolução absoluta"
    )

    fig_absolute = (
        absolute_evolution_chart(
            yearly_table
        )
    )

    st.pyplot(
        fig_absolute,
        clear_figure=True,
    )

    # -----------------------------------
    # Evolução percentual
    # -----------------------------------

    st.subheader(
        "Evolução percentual"
    )

    fig_percentage = (
        percentage_evolution_chart(
            yearly_table
        )
    )

    st.pyplot(
        fig_percentage,
        clear_figure=True,
    )