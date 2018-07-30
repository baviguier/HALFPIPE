# -*- coding: utf-8 -*-
"""DOCSTRING."""

import maya.cmds as mc

import os

from pipe.utils import HALFPIPE_PATH_FILE

import maya.OpenMayaUI as apiUI
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from pipe.PipeTool import PipeTool
from pipe.PipeTool import PipeToolMainWindow


def getMayaWindow():
    """Get the main Maya window as a QtWidgets.QMainWindow instance.

    Returns
    -------
    QtWidgets.QMainWindow
        Instance of the top level Maya windows

    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QtWidgets.QMainWindow)


def pipeToolMain():
    """Show the Half Pipe window."""
    if not os.path.exists(HALFPIPE_PATH_FILE):
        os.makedirs(HALFPIPE_PATH_FILE)
    try:
        if mc.window(PipeToolMainWindow.name, q=True, ex=True):
            mc.deleteUI(PipeToolMainWindow.name)
    except Exception:
        pass

    try:
        workspace_name = PipeToolMainWindow.name + 'WorkspaceControl'
        if mc.workspaceControl(workspace_name, q=True, ex=True):
            mc.workspaceControl(workspace_name, e=True, close=True)
            mc.deleteUI(workspace_name, control=True)
    except Exception:
        pass

    main_window = PipeToolMainWindow(getMayaWindow(), dialog=PipeTool())
    main_window.show(dockable=True, area='right', floating=False)

    mc.workspaceControl(
        workspace_name,
        e=True,
        tabToControl=['AttributeEditor', -1],
        widthProperty='preferred',
        minimumWidth=1010
    )
    main_window.raise_()
