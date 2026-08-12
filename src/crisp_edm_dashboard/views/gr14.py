import pandas as pd
import streamlit as st

from crisp_edm_dashboard.analysis.gr14 import (
    discipline_details,
    discipline_evolution,
    failure_summary_by_series,
    get_disciplines,
    get_years,
    top_disciplines_by_failures,
)
from crisp_edm_dashboard.charts.gr14 import (
    discipline_evolution_chart,
    series_failure_chart,
)
from crisp_edm_dashboard.config import (
    PROCESSED_DATA_DIR,
)


GR14_DATA = (
    PROCESSED_DATA_DIR
    / "gr14.parquet"
)


@st.cache_data
def load_gr14() -> pd.DataFrame:
    """Carrega a base processada do GR14."""

    return pd.read_parquet(
        GR14_DATA
    )


def render() -> None:
    st.title(
        "📊 Aprovação e Reprovação — GR14"
    )

    st.write(
        """
        Análise do desempenho acadêmico por
        disciplina e série do curso de Ciência
        da Computação.
        """
    )

    if not GR14_DATA.exists():
        st.error(
            "A base processada do GR14 ainda não existe. "
            "Execute primeiro: "
            "`poetry run python scripts/process_all.py`"
        )
        return

    df = load_gr14()

    # ===================================
    # ANÁLISE DE UMA TURMA
    # ===================================

    st.header(
        "🔎 Análise por disciplina"
    )

    st.write(
        """
        Selecione um ano e uma disciplina para
        visualizar os indicadores correspondentes.
        """
    )

    years = get_years(
        df
    )

    selected_year = st.selectbox(
        "Ano",
        years,
        key="gr14_detail_year",
    )

    disciplines = get_disciplines(
        df,
        selected_year,
    )

    selected_discipline = st.selectbox(
        "Disciplina",
        disciplines,
        key="gr14_detail_discipline",
    )

    details = discipline_details(
        df,
        selected_year,
        selected_discipline,
    )

    st.subheader(
        f"{selected_discipline} — {selected_year}"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Total de alunos",
        details[
            "TOTAL_ALUNOS"
        ],
        border=True,
    )

    col2.metric(
        "Reprovados",
        (
            f"{details['REPROVADOS']} "
            f"({details['TAXA_REPROVACAO']:.2f}%)"
        ),
        border=True,
    )

    col3.metric(
        "Aprovados",
        (
            f"{details['APROVADOS']} "
            f"({details['TAXA_APROVACAO']:.2f}%)"
        ),
        border=True,
    )

    col4.metric(
        "Série",
        details[
            "SERIE"
        ],
        border=True,
    )

    st.divider()

    # ===================================
    # TOP 3
    # ===================================

    st.header(
        "📚 Disciplinas com maior número de reprovações"
    )

    ranking_year = st.selectbox(
        "Ano do ranking",
        years,
        key="gr14_ranking_year",
    )

    top3 = (
        top_disciplines_by_failures(
            df,
            ranking_year,
            n=3,
        )
    )

    display_top3 = (
        top3.rename(
            columns={
                "DISCIPLINA":
                    "Disciplina",
                "REPROVADOS":
                    "Reprovados",
                "TOTAL_ALUNOS":
                    "Total de alunos",
                "TAXA_REPROVACAO":
                    "Taxa de reprovação (%)",
            }
        )
    )

    display_top3[
        "Taxa de reprovação (%)"
    ] = (
        display_top3[
            "Taxa de reprovação (%)"
        ]
        .round(2)
    )

    st.dataframe(
        display_top3,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        """
        O ranking considera a quantidade absoluta
        de reprovações. A taxa de reprovação é
        apresentada como informação complementar.
        """
    )

    st.divider()

    # ===================================
    # EVOLUÇÃO TEMPORAL
    # ===================================

    st.header(
        "📈 Evolução por disciplina"
    )

    all_disciplines = (
        get_disciplines(
            df
        )
    )

    default_index = (
        all_disciplines.index(
            selected_discipline
        )
        if selected_discipline
        in all_disciplines
        else 0
    )

    evolution_discipline = (
        st.selectbox(
            "Disciplina para análise temporal",
            all_disciplines,
            index=default_index,
            key="gr14_evolution_discipline",
        )
    )

    evolution_metric = st.radio(
        "Indicador",
        [
            "Quantidade de reprovações",
            "Taxa de reprovação (%)",
        ],
        horizontal=True,
        key="gr14_evolution_metric",
    )

    evolution = (
        discipline_evolution(
            df,
            evolution_discipline,
        )
    )

    fig_evolution = (
        discipline_evolution_chart(
            evolution,
            evolution_discipline,
            evolution_metric,
        )
    )

    st.pyplot(
        fig_evolution,
        clear_figure=True,
    )

    with st.expander(
        "Ver dados da série histórica"
    ):
        evolution_display = (
            evolution[
                [
                    "ANO",
                    "REPROVADOS",
                    "APROVADOS",
                    "TOTAL_ALUNOS",
                    "TAXA_REPROVACAO",
                ]
            ]
            .copy()
        )

        evolution_display[
            "TAXA_REPROVACAO"
        ] = (
            evolution_display[
                "TAXA_REPROVACAO"
            ]
            .round(2)
        )

        evolution_display = (
            evolution_display.rename(
                columns={
                    "ANO":
                        "Ano",
                    "REPROVADOS":
                        "Reprovados",
                    "APROVADOS":
                        "Aprovados",
                    "TOTAL_ALUNOS":
                        "Total de alunos",
                    "TAXA_REPROVACAO":
                        "Taxa de reprovação (%)",
                }
            )
        )

        st.dataframe(
            evolution_display,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ===================================
    # DESEMPENHO POR SÉRIE
    # ===================================

    st.header(
        "🎓 Desempenho por série do curso"
    )

    st.write(
        """
        Taxa global de reprovação em cada série,
        considerando o conjunto das matrículas
        presentes no período analisado.
        """
    )

    series_summary = (
        failure_summary_by_series(
            df
        )
    )

    fig_series = (
        series_failure_chart(
            series_summary
        )
    )

    st.pyplot(
        fig_series,
        clear_figure=True,
    )

    with st.expander(
        "Ver dados por série"
    ):
        series_display = (
            series_summary.copy()
        )

        series_display[
            "TAXA_REPROVACAO"
        ] = (
            series_display[
                "TAXA_REPROVACAO"
            ]
            .round(2)
        )

        series_display = (
            series_display.rename(
                columns={
                    "SERIE":
                        "Série",
                    "REPROVADOS":
                        "Reprovados",
                    "APROVADOS":
                        "Aprovados",
                    "TOTAL_ALUNOS":
                        "Total de alunos",
                    "TAXA_REPROVACAO":
                        "Taxa de reprovação (%)",
                }
            )
        )

        st.dataframe(
            series_display,
            width="stretch",
            hide_index=True,
        )