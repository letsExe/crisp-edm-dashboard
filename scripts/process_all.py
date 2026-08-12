from crisp_edm_dashboard.config import (
    ensure_directories,
)
from crisp_edm_dashboard.processing.gr13 import (
    process_gr13,
)
from crisp_edm_dashboard.processing.gr14 import (
    process_gr14,
)
from crisp_edm_dashboard.processing.gr16 import (
    process_gr16,
)


def main() -> None:

    ensure_directories()

    print(
        "Processando GR13..."
    )

    gr13 = process_gr13()

    print(
        f"GR13 concluído: {len(gr13)} registros."
    )

    print()

    print(
        "Processando GR14..."
    )

    gr14 = process_gr14()

    print(
        f"GR14 concluído: {len(gr14)} registros."
    )

    print()

    print(
        "Processando GR16..."
    )

    gr16 = process_gr16()

    print(
        f"GR16 concluído: {len(gr16)} registros."
    )

    print()

    print(
        "Processamento concluído."
    )


if __name__ == "__main__":
    main()