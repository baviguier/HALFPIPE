Launch by copy/paste this code in a Python tab:

import sys
import types
import maya.cmds as mc

path = r"C:\folder\halfpipe"
if not path in sys.path:
    sys.path.insert(0, path)
    
from pipe.PipeTool import PipeToolMainWindow
if mc.window(PipeToolMainWindow.name, q=True, ex=True):
    mc.deleteUI(PipeToolMainWindow.name)

# Get a reference to each loaded module
loaded_modules = dict([
    (key, value)
    for key, value in sys.modules.items()
    if (
        key.startswith('pipe') and
        isinstance(value, types.ModuleType)
    )
])

# Delete references to these loaded modules from sys.modules
for key in loaded_modules:
    del sys.modules[key]

# Load each of the modules again
# Make old modules share state with new modules
for key in loaded_modules:
    print('re-loading %s' % key)
    newmodule = __import__(key)
    oldmodule = loaded_modules[key]
    oldmodule.__dict__.clear()
    oldmodule.__dict__.update(newmodule.__dict__)

from pipe import pipeToolMain
window = pipeToolMain()