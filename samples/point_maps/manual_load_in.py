from pathlib import Path

from sync_module.mi import synchronize
from midf.conversion import to_mi_solution
from midf.linking import link_imdf
from midf.loading import MANIFEST_KEY, load_imdf

a = Path(r"C:\Users\chen\Downloads\Finavia_IMDF_all_floors_20250320.zip")
imdf_dict = load_imdf(a)

midf_solution = link_imdf(imdf_dict)

imdf_manifest = imdf_dict.pop(MANIFEST_KEY)[0]

mi_solution = to_mi_solution(midf_solution)

synchronize(mi_solution)
