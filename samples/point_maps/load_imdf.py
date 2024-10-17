from pathlib import Path

from integration_system.mi import synchronize
from midf.conversion import to_mi_solution
from midf.linking import link_imdf
from midf.loading import load_imdf

if __name__ == "__main__":
  data_base = Path(__file__).parent / "data"

  imdf_dict = load_imdf(data_base / "Kansas Airport - Demo Map_IMDF_address_fix.zip")

  midf_solution = link_imdf(imdf_dict)

  mi_solution = to_mi_solution(midf_solution)

  if True:
    synchronize(mi_solution)
  else:
    from integration_system.json_serde import to_json

    with open(data_base / "go.json", "w") as f:
      f.write(to_json(mi_solution))
