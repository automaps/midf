PROJECT_NAME = "MapsIndoors Data Format"
PROJECT_AUTHOR = "Christian Heider Lindbjerg"
PROJECT_ORGANISATION = "MapsPeople"
PROJECT_VERSION = "0.0.1"
PROJECT_YEAR = 2024

__doc__ = f"""
MapsIndoors Data Format

=====================   ======================
project name:           {PROJECT_NAME}
project author:         {PROJECT_AUTHOR}
project organisation:   {PROJECT_ORGANISATION}
project version:        {PROJECT_VERSION}
project year:           {PROJECT_YEAR}
=====================   ======================

"""
__version__ = PROJECT_VERSION
__author__ = PROJECT_AUTHOR

try:
    from apppath import AppPath

    PROJECT_APP_PATH = AppPath(PROJECT_NAME, app_author=PROJECT_AUTHOR)
except Exception:
    PROJECT_APP_PATH = None
