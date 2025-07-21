import logging
from pathlib import Path

from integration_system.mi import SyncLevel, synchronize
from midf.conversion import to_mi_solution
from midf.linking import link_imdf
from midf.loading import MANIFEST_KEY, load_imdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    data_base = Path(__file__).parent / "data" / "zips9"
    # data_base = (Path(__file__).parent / "data" / "zip3")

    for f in data_base.iterdir():
        if f.is_file() and f.suffix == ".zip":
            if False:
                if "Temasek_IMDF" not in f.stem:
                    continue

            logger.error(f"Processing {f}")

            try:
                imdf_dict = load_imdf(f)

                midf_solution = link_imdf(imdf_dict)

                imdf_manifest = imdf_dict.pop(MANIFEST_KEY)[0]

                if False:
                    from midf.validation.validator import IMDFValidator

                    errors = IMDFValidator().validate_dataset(imdf_dict, imdf_manifest)
                    if errors:
                        for error in errors:
                            print(error)
                    else:
                        print("IMDF dataset is valid.")

                mi_solution = to_mi_solution(midf_solution)

                if True:
                    synchronize(
                        mi_solution, sync_level=SyncLevel.venue, include_occupants=True
                    )
                else:
                    from integration_system.tools.serialisation import to_json

                    with open(data_base / "go.json", "w") as f:
                        f.write(to_json(mi_solution))
            except Exception as e:
                if True:
                    raise e
                logger.error(f"Failed to process {f}: {e}")
