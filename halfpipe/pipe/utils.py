# -*- coding: utf-8 -*-
"""Collection of methods to use in the tool."""

import os
import re

from PySide2 import QtCore
from PySide2 import QtGui

import maya.OpenMayaUI as apiUI
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

HALFPIPE_PATH_FILE = os.path.normpath(os.path.join(
    "C:/Users", os.environ['USERNAME'], 'AppData', 'Local', '.HalfPipe'
))
SETTINGS_FILE = 'settings.json'
PROJECT_SETTINGS_FILE = 'project_settings.json'
DEFAULT_COLOR = '#9D6AFF'


def load_icon(buttonToChange, image_path):
    """Replace a button by an image."""
    full_icon_path = os.path.join(
        os.path.split(__file__)[0],
        "..",
        image_path
    )
    buttonToChange.setIcon(QtGui.QIcon(full_icon_path))
    buttonToChange.setIconSize(QtCore.QSize(14, 14))
    buttonToChange.setText('')


def formatText(text):
    """Change the user text to respect folder name conventions."""
    text = text.upper()
    text = re.sub('[^0-9a-zA-Z_]+', '', text)
    text = re.sub(r'\W+', '', text)
    return text


def formatName(text):
    """Change the user text to respect name conventions."""
    text = re.sub('[^0-9a-zA-Z]+', '', text)
    text = re.sub(r'\W+', '', text)
    return text


def getSelfAndUpdate():
    """Find self in memory and update the references table."""
    ptr = apiUI.MQtUtil.findWindow('PipeToolWindow')
    window = wrapInstance(long(ptr), QtWidgets.QMainWindow)
    window.centralWidget().updateReferenceTable()
    print 'reading file', window
    print 'reading file', ptr
    print 'reading file', window.centralWidget()
