import pandas as pd
import streamlit as st

from crisp_edm_dashboard.analysis.gr38 import (
    get_years,
)
from crisp_edm_dashboard.charts.gr38 import (
    admission_form_chart,
    admission_form_evolution_chart,
    age_band_by_admission_form_chart,
    age_band_chart,
    sex_by_admission_form_chart,
)
from crisp_edm_dashboard.config import (
    PROCESSED_DATA_DIR,
)
from crisp_edm_dashboard.tables.gr38 import (
    admission_form_distribution,
    admission_form_evolution,
    age_band_by_admission_form,
    age_band_distribution,
    sex_by_admission_form,
    year_summary,
)


GR38_DATA = (
    PROCESSED_DATA_DIR
    / "gr38.parquet"
)


@st.cache_data
def load_gr38() -> pd.DataFrame:
    """Carrega a base processada do GR38."""

    return pd.read_parquet(
        GR38_DATA
    )


def render() -> None:

    st.title(
        "🚪 Perfil dos Ingressantes — GR38"
    )

    st.write(
        """
        Análise das formas de ingresso e das
        características demográficas dos estudantes
        ingressantes no curso de Ciência da Computação.
        """
    )

    if not GR38_DATA.exists():

        st.error(
            "A base processada do GR38 ainda não existe. "
            "Execute primeiro: "
            "`poetry run python scripts/process_all.py`"
        )

        return

    df = load_gr38()

    years = get_years(
        df
    )

    selected_year = st.selectbox(
        "Ano de referência",
        years,
        key="gr38_year",
    )

    # ===================================
    # RESUMO
    # ===================================

    summary = year_summary(
        df,
        selected_year,
    )

    st.header(
        f"🚀 Resumo dos ingressantes em {selected_year}"
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(
        "Total de ingressantes",
        summary["TOTAL"],
        border=True,
    )

    col2.metric(
        "Sexo masculino",
        summary[
            "MASCULINO"
        ],
        border=True,
    )

    col3.metric(
        "Sexo feminino",
        summary[
            "FEMININO"
        ],
        border=True,
    )

    st.divider()

    # ===================================
    # FORMAS DE INGRESSO
    # ===================================

    st.header(
        "🔍 Formas de ingresso"
    )

    admission_table = (
        admission_form_distribution(
            df,
            selected_year,
        )
    )

    admission_display = (
        admission_table.rename(
            columns={
                "FORMA_INGRESSO":
                    "Forma de ingresso",
                "TOTAL":
                    "Total",
                "PERCENTUAL":
                    "Percentual (%)",
            }
        )
        .copy()
    )

    admission_display[
        "Percentual (%)"
    ] = (
        admission_display[
            "Percentual (%)"
        ]
        .round(2)
    )

    st.dataframe(
        admission_display,
        width="stretch",
        hide_index=True,
    )

    fig_admission = (
        admission_form_chart(
            admission_table,
            selected_year,
        )
    )

    st.pyplot(
        fig_admission,
        clear_figure=True,
    )

    st.divider()

    # ===================================
    # FAIXA ETÁRIA
    # ===================================

    st.header(
        "🎂 Faixa etária dos ingressantes"
    )

    st.write(
        """
        A planilha institucional apresenta três
        esquemas sobrepostos de classificação
        etária. Para evitar a contagem repetida dos
        mesmos ingressantes, esta análise utiliza
        apenas um esquema consistente de faixas.
        """
    )

    age_table = (
        age_band_distribution(
            df,
            selected_year,
        )
    )

    age_display = (
        age_table.rename(
            columns={
                "FAIXA_ETARIA":
                    "Faixa etária",
                "TOTAL":
                    "Total",
                "PERCENTUAL":
                    "Percentual (%)",
            }
        )
        .copy()
    )

    age_display[
        "Percentual (%)"
    ] = (
        age_display[
            "Percentual (%)"
        ]
        .round(2)
    )

    st.dataframe(
        age_display,
        width="stretch",
        hide_index=True,
    )

    fig_age = (
        age_band_chart(
            age_table,
            selected_year,
        )
    )

    st.pyplot(
        fig_age,
        clear_figure=True,
    )

    age_form_table = (
        age_band_by_admission_form(
            df,
            selected_year,
        )
    )

    with st.expander(
        "Ver faixa etária por forma de ingresso"
    ):

        fig_age_form = (
            age_band_by_admission_form_chart(
                age_form_table,
                selected_year,
            )
        )

        st.pyplot(
            fig_age_form,
            clear_figure=True,
        )

        st.dataframe(
            age_form_table,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ===================================
    # SEXO
    # ===================================

    st.header(
        "🚻 Distribuição por sexo"
    )

    st.write(
        """
        Comparação da distribuição por sexo entre
        as diferentes formas de ingresso.
        """
    )

    sex_table = (
        sex_by_admission_form(
            df,
            selected_year,
        )
    )

    fig_sex = (
        sex_by_admission_form_chart(
            sex_table,
            selected_year,
        )
    )

    st.pyplot(
        fig_sex,
        clear_figure=True,
    )

    with st.expander(
        "Ver tabela por sexo e forma de ingresso"
    ):

        sex_display = (
            sex_table.rename(
                columns={
                    "FORMA_INGRESSO":
                        "Forma de ingresso",
                    "MASCULINO":
                        "Masculino",
                    "FEMININO":
                        "Feminino",
                    "TOTAL":
                        "Total",
                }
            )
        )

        st.dataframe(
            sex_display,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ===================================
    # EVOLUÇÃO HISTÓRICA
    # ===================================

    st.header(
        "📈 Evolução das formas de ingresso"
    )

    st.write(
        """
        Evolução anual das modalidades de ingresso
        ao longo de todo o período disponível.
        """
    )

    evolution = (
        admission_form_evolution(
            df
        )
    )

    fig_evolution = (
        admission_form_evolution_chart(
            evolution
        )
    )

    st.pyplot(
        fig_evolution,
        clear_figure=True,
    )

    with st.expander(
        "Ver dados históricos"
    ):

        evolution_display = (
            evolution.rename(
                columns={
                    "ANO_REFERENCIA":
                        "Ano",
                    "FORMA_INGRESSO":
                        "Forma de ingresso",
                    "TOTAL":
                        "Total",
                }
            )
        )

        st.dataframe(
            evolution_display,
            width="stretch",
            hide_index=True,
        )