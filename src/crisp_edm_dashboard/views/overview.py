import streamlit as st


def render() -> None:
    st.title(
        "Análise Acadêmica — Ciência da Computação"
    )

    st.write(
        """
        Dashboard desenvolvido para análise longitudinal
        de dados acadêmicos do curso de Ciência da
        Computação da UNIOESTE — Campus de Foz do Iguaçu.
        """
    )

    st.subheader(
        "Relatórios analisados"
    )

    st.markdown(
        """
        **GR13 — Situação acadêmica**

        Evolução das situações acadêmicas ao longo dos anos.

        **GR14 — Desempenho por disciplina**

        Aprovação, reprovação e análise por série.

        **GR16 — Perfil discente**

        Características demográficas dos acadêmicos.

        **GR38 — Perfil dos ingressantes**

        Formas de ingresso e características dos novos
        acadêmicos.
        """
    )