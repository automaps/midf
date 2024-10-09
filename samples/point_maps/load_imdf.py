from pathlib import Path

from midf.linking import link_imdf
from midf.loading import load_imdf

if __name__ == "__main__":
    imdf_dict = load_imdf(
        Path(__file__).parent / "data" / "Kansas Airport - Demo Map_IMDF.zip"
    )

    midf_solution = link_imdf(imdf_dict)

    print(midf_solution)
