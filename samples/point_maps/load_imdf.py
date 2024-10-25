from pathlib import Path

from integration_system.mi import synchronize
from midf.conversion import to_mi_solution
from midf.linking import link_imdf
from midf.loading import MANIFEST_KEY, load_imdf
from midf.validation import IMDFValidator

if __name__ == "__main__":
  data_base = Path(__file__).parent / "data"

  imdf_dict = load_imdf(data_base / "Kansas Airport - Demo Map_IMDF_address_fix.zip")

  midf_solution = link_imdf(imdf_dict)

  imdf_manifest = imdf_dict.pop(MANIFEST_KEY)[0]

  errors = IMDFValidator().validate_dataset(imdf_dict, imdf_manifest)
  if errors:
    for error in errors:
      print(error)
  else:
    print("IMDF dataset is valid.")

  mi_solution = to_mi_solution(midf_solution)

  if True:
    synchronize(mi_solution)
  else:
    from integration_system.json_serde import to_json

    with open(data_base / "go.json", "w") as f:
      f.write(to_json(mi_solution))
