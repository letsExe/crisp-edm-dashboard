from pathlib import Path

import pandas as pd


def read_excel(
    path: Path,
    sheet_name=0,
):
    """Lê uma aba de um arquivo Excel."""

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}"
        )

    return pd.read_excel(
        path,
        sheet_name=sheet_name,
    )


def read_all_sheets(
    path: Path,
) -> dict[str, pd.DataFrame]:
    """Lê todas as abas de um arquivo Excel."""

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}"
        )

    return pd.read_excel(
        path,
        sheet_name=None,
    )