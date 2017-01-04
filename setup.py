from distutils.core import setup
import py2exe

import glob

includes = ["sip", "pyproj"]
excludes = ["_ssl"]
options = {"py2exe":
            {"compressed": 1,
             "optimize": 2,
             "includes": includes,
             "excludes": excludes,
             "dll_excludes": ["MSVCP90.dll"],
             #"dll_excludes": ["MSVCP90.dll", "w9xpopen.exe", "SSLEAY32.dll", "LIBEAY32.dll"],
             #"bundle_files": 1,
            }
          }
          
MyDataFiles = [('DLLS', ['''D:\Python27\Lib\site-packages\shapely\DLLs\geos_c.dll''']),
              ]
          
setup(
    version = "0.1.0",
    description = "KML Tool",
    name = "KML Tool",
    options = options,
    data_files = MyDataFiles,
    #zipfile="pylibs.zip",
    windows=[{"script": "app.pyw",
              "icon_resources": [(0, r"app.ico")],}],
    )
    
