#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# pyTailor v1.0.0 15/02/2019
# A program designed for a tailoring and alterations business
#-------------------------------------------------------------------------------

# Importing Libraries
import sys
from cx_Freeze import setup
from cx_Freeze import Executable


# Declaring include files
include_files = ["database/", "images/"]
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="pyTailor++",
      version="1.0.0",
      description="Tailoring and Alterations Software",
      options={'build_exe': {"include_files": include_files}},
      executables=[Executable("main.py",
                              base=base,
                              icon="images/pytailor++.ico",
                              targetName="pyTailor++.exe")])

