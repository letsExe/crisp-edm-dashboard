from pathlib import Path


# Raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dados
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Resultados
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Período definido para o artigo
ARTICLE_START_YEAR = 2008
ARTICLE_END_YEAR = 2024


def ensure_directories() -> None:
    """Cria os diretórios gerados pela aplicação, caso não existam."""

    directories = [
        PROCESSED_DATA_DIR,
        TABLES_DIR,
        FIGURES_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)