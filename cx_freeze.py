import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
	"packages": ["os"], 
	"excludes": ["tkinter"],
	"include_files": [r'D:\Python27\Lib\site-packages\shapely\DLLs\geos_c.dll',
                      'app.ico',
                      ],
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "KML tools",
        version = "0.1",
        description = "KML tools",
        options = {"build_exe": build_exe_options},
        executables = [Executable("kmltools.pyw", base=base, icon='app.ico')])