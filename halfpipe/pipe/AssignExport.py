# -*- coding: utf-8 -*-
"""Script to export and import shaders by Fabien Meyran."""

import maya.cmds as cmds
import os

from PySide2 import QtCore
from PySide2 import QtWidgets


class Ui_exportDialog(object):
    """Define the Export Shaders Dialog."""

    def setupUi(self, exportDialog):
        """Set the UI."""
        exportDialog.setObjectName("exportDialog")
        exportDialog.resize(270, 150)
        self.verticalLayout = QtWidgets.QVBoxLayout(exportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.all_checkbox = QtWidgets.QCheckBox(exportDialog)
        self.all_checkbox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.all_checkbox.setObjectName("all_checkbox")
        self.verticalLayout.addWidget(self.all_checkbox)
        self.selection_checkbox = QtWidgets.QCheckBox(exportDialog)
        self.selection_checkbox.setContextMenuPolicy(
            QtCore.Qt.DefaultContextMenu
        )
        self.selection_checkbox.setObjectName("selection_checkbox")
        self.verticalLayout.addWidget(self.selection_checkbox)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        self.export_button = QtWidgets.QPushButton(exportDialog)
        self.export_button.setMinimumSize(QtCore.QSize(0, 50))
        self.export_button.setObjectName("export_button")
        self.verticalLayout.addWidget(self.export_button)

        self.retranslateUi(exportDialog)
        QtCore.QMetaObject.connectSlotsByName(exportDialog)

    def retranslateUi(self, exportDialog):
        """Set UI texts."""
        exportDialog.setWindowTitle("Export Shaders")
        self.all_checkbox.setText("Export all shaders from scene")
        self.selection_checkbox.setText("Export shaders from selection")
        self.export_button.setText("Export shaders")


class ExportShaders (QtWidgets.QDialog):
    """Connect the UI to methods."""

    def __init__(self, parent=None, projectPath=None):
        """Initialize default variable and functions."""
        super(ExportShaders, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_exportDialog()
        self.ui.setupUi(self)
        self.ui.all_checkbox.setChecked(True)

        # Check if Shaders folders exists, create if not
        self.full_project_path = projectPath
        if projectPath is not None:
            self.shader_folder = os.path.normpath(os.path.join(
                self.full_project_path,
                '5_DATA',
                'SHADERS'
            ))
            if not os.path.exists(self.shader_folder):
                os.makedirs(self.shader_folder)
                print 'SHADERS folder created.'
        else:
            cmds.warning("Half Pipe project not set.")
            self.ui.export_button.setEnabled(False)
            return

        self.mapEvents()

    def mapEvents(self):
        """Connect UI to methods."""
        self.ui.all_checkbox.clicked.connect(self.updateAllButton)
        self.ui.selection_checkbox.clicked.connect(self.updateSelButton)
        self.ui.export_button.clicked.connect(self.output)

    def updateAllButton(self):
        """Disable Selection Checkbox."""
        self.ui.selection_checkbox.setChecked(False)

        if (
            not self.ui.all_checkbox.isChecked() and
            not self.ui.selection_checkbox.isChecked()
        ):
            self.ui.export_button.setEnabled(False)
        else:
            self.ui.export_button.setEnabled(True)

    def updateSelButton(self):
        """Disable All Checkbox."""
        self.ui.all_checkbox.setChecked(False)

        if (
            not self.ui.all_checkbox.isChecked() and
            not self.ui.selection_checkbox.isChecked()
        ):
            self.ui.export_button.setEnabled(False)
        else:
            self.ui.export_button.setEnabled(True)

    def output(self):
        """Export a .ma with shaders and links."""
        selection = cmds.ls(sl=True)

        # Ask the user where to export the shader scene file
        shaderSceneFile = cmds.fileDialog2(
            fileMode=0,
            startingDirectory=self.shader_folder,
            caption="Export shaders",
            ff='Maya ASCII(*.ma)')

        allShds = self.ui.all_checkbox.isChecked()
        selShds = self.ui.selection_checkbox.isChecked()

        try:
            cmds.delete('shadersAssignmentInfo')
        except:
            pass

        # Exctracting the scene name defined by the user

        scenePathList = shaderSceneFile[0].split('/')
        sceneName = scenePathList[-1].split('.ma')

        # Creating the assignementInfo node
        saInfo = cmds.createNode(
            "geometryVarGroup",
            name='shadersAssignmentInfo'
        )
        cmds.setAttr(saInfo + '.tx', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.ty', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.tz', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.rx', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.ry', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.rz', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.sx', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.sy', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.sz', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(saInfo + '.v', lock=True, keyable=False, channelBox=False)


        n = 0
        shaderList = []

        # if the user asked for selection only,
        # we take the selection as the list to proceed with.
        if selShds:
            objectList = selection

        # else, we list all the type mesh objects from the scene
        if allShds:
            objectList = cmds.ls(typ='mesh')

        # Getting each shader for each object,
        # and stocking the information as a string in the assingment info,
        # as a "shaderInfo" attribute
        for object in objectList:
            shader = cmds.listConnections(
                cmds.listHistory(object, f=1), type='shadingEngine'
            )
            shaderList.append(shader)
            cmds.addAttr(saInfo, ln='shaderInfo' + str(n), dt='string')

            objectNameList = object.split(':')

            # extract the name of the object if a namespace exists
            if len(objectNameList) > 1:
                objectName = objectNameList[-1]
            else:
                objectName = objectNameList[0]

            # if the object has no shader,
            # then we just fill the attribute with text "has no shader"
            if not shader:
                cmds.setAttr(
                    saInfo + '.shaderInfo' + str(n),
                    object + ' has no shader',
                    type='string'
                )
            else:
                cmds.setAttr(
                    saInfo + '.shaderInfo' + str(n),
                    objectName + ' = ' + shader[0],
                    type='string'
                )
            n = n + 1

        # selecting assignementInfo and shaders ready to export
        cmds.select(saInfo, r=True)
        for shader in shaderList:
            cmds.select(shader, ne=True, add=True)

        # export the files
        cmds.file(shaderSceneFile, op="v=0;p=17;f=0", typ="mayaAscii", es=True)
        cmds.warning("Shaders successfully exported.")
        self.accept()

        # cleaning stuff
        cmds.select(cl=True)
        cmds.delete(saInfo)