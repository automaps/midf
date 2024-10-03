from pathlib import Path

from midf.serde.loading import parse_imdf

if __name__ == "__main__":
    imdf_dict = parse_imdf(
        Path(__file__).parent / "data" / "Kansas Airport - Demo Map_IMDF.zip"
    )
