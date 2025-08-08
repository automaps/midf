from download_files import download_files
from fix_pc_jsons import fix_pc_venue_jsons
from imdfify_pc_venue import to_imdf_venue
from load_pc_imdf_venues import upload_to_mi

download_files()
fix_pc_venue_jsons()
to_imdf_venue()
upload_to_mi()
