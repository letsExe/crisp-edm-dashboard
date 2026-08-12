import streamlit as st

from crisp_edm_dashboard.views.gr13 import (
    render as render_gr13,
)
from crisp_edm_dashboard.views.gr14 import (
    render as render_gr14,
)
from crisp_edm_dashboard.views.overview import (
    render as render_overview,
)


st.set_page_config(
    page_title="CRISP-EDM Dashboard",
    page_icon="📊",
    layout="wide",
)


page = st.sidebar.radio(
    "Navegação",
    [
        "Visão Geral",
        "GR13 — Situação Acadêmica",
        "GR14 — Aprovação e Reprovação",
        "GR16 — Perfil Discente",
        "GR38 — Perfil dos Ingressantes",
        "Metodologia",
    ],
)


if page == "Visão Geral":
    render_overview()

elif page == "GR13 — Situação Acadêmica":
    render_gr13()

elif page == "GR14 — Aprovação e Reprovação":
    render_gr14()

elif page == "GR16 — Perfil Discente":
    st.title(
        "GR16 — Perfil Discente"
    )
    st.info(
        "Dashboard em reconstrução."
    )

elif page == "GR38 — Perfil dos Ingressantes":
    st.title(
        "GR38 — Perfil dos Ingressantes"
    )
    st.info(
        "Dashboard em reconstrução."
    )

elif page == "Metodologia":
    st.title(
        "Metodologia"
    )

    st.write(
        """
        O projeto utiliza o processo CRISP-EDM para
        organizar a preparação, análise, avaliação e
        apresentação dos dados educacionais.
        """
    )