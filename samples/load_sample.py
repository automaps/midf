from pathlib import Path

from midf.loading import parse_imdf

if __name__ == "__main__":
    parse_imdf(Path(__file__).parent / "data" / "Kansas Airport - Demo Map_IMDF.zip")
