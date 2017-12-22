# -*- coding: utf-8 -*-
"""Script to export and import shaders by Fabien Meyran."""

import maya.cmds as cmds
import os

from PySide2 import QtCore
from PySide2 import QtWidgets


class Ui_importDialog(object):
    """Define the Import Shaders Dialog."""

    def setupUi(self, importDialog):
        """Set the UI."""
        importDialog.setObjectName("importDialog")
        importDialog.resize(270, 150)
        self.verticalLayout = QtWidgets.QVBoxLayout(importDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.imp_assign_checkbox = QtWidgets.QCheckBox(importDialog)
        self.imp_assign_checkbox.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.imp_assign_checkbox.setObjectName("imp_assign_checkbox")
        self.verticalLayout.addWidget(self.imp_assign_checkbox)
        self.imp_only_checkbox = QtWidgets.QCheckBox(importDialog)
        self.imp_only_checkbox.setContextMenuPolicy(
            QtCore.Qt.DefaultContextMenu
        )
        self.imp_only_checkbox.setObjectName("imp_only_checkbox")
        self.verticalLayout.addWidget(self.imp_only_checkbox)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        self.import_button = QtWidgets.QPushButton(importDialog)
        self.import_button.setMinimumSize(QtCore.QSize(0, 50))
        self.import_button.setObjectName("import_button")
        self.verticalLayout.addWidget(self.import_button)

        self.retranslateUi(importDialog)
        QtCore.QMetaObject.connectSlotsByName(importDialog)

    def retranslateUi(self, importDialog):
        """Set UI texts."""
        importDialog.setWindowTitle("Import Shaders")
        self.imp_assign_checkbox.setText("Import and assign")
        self.imp_only_checkbox.setText("Import shaders only")
        self.import_button.setText("Import shaders")


class ImportShaders (QtWidgets.QDialog):
    """Connect the UI to methods."""

    def __init__(self, parent=None, projectPath=None):
        """Initialize default variable and functions."""
        super(ImportShaders, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_importDialog()
        self.ui.setupUi(self)
        self.ui.imp_assign_checkbox.setChecked(True)

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
            self.ui.import_button.setEnabled(False)
            return

        self.mapEvents()

    def mapEvents(self):
        """Connect UI to methods."""
        self.ui.imp_assign_checkbox.clicked.connect(self.updateImpOnlyButton)
        self.ui.imp_only_checkbox.clicked.connect(self.updateImpAssignButton)
        self.ui.import_button.clicked.connect(self.input)

    def updateImpOnlyButton(self):
        """Disable Selection Checkbox."""
        self.ui.imp_only_checkbox.setChecked(False)

        if (
            not self.ui.imp_assign_checkbox.isChecked() and
            not self.ui.imp_only_checkbox.isChecked()
        ):
            self.ui.import_button.setEnabled(False)
        else:
            self.ui.import_button.setEnabled(True)

    def updateImpAssignButton(self):
        """Disable All Checkbox."""
        self.ui.imp_assign_checkbox.setChecked(False)

        if (
            not self.ui.imp_assign_checkbox.isChecked() and
            not self.ui.imp_only_checkbox.isChecked()
        ):
            self.ui.import_button.setEnabled(False)
        else:
            self.ui.import_button.setEnabled(True)

    def input(self):
        """Update if we import and/or assign shaders."""
        # get the scene path file
        self.shaderSceneFile = cmds.fileDialog2(
            fileMode=1,
            startingDirectory=self.shader_folder,
            caption="Import shaders",
            ff='Maya ASCII(*.ma)')

        scenePathList = self.shaderSceneFile[0].split('/')
        self.sceneName = scenePathList[-1].split('.ma')

        # get if we only want to import or not
        importAssign = self.ui.imp_assign_checkbox.isChecked()
        importOnly = self.ui.imp_only_checkbox.isChecked()

        # if the assignementInfo already exists,
        # then we ask if we only want to refresh the shaders.
        # "No" means do nothing.

        if cmds.objExists('SH_' + self.sceneName[0] + ':shadersAssignmentInfo'):
            confirmRefresh = cmds.confirmDialog(
                title='Refresh shaders',
                ma='center',
                message=(
                    "The shaders you are trying to import already exist"
                    "in this scene. Would you like to refresh them ?"
                ),
                button=['Yes', 'No']
            )

            if confirmRefresh == 'Yes':
                if importAssign:
                    self.applyShaders(1, 0)
                else:
                    self.applyShaders(1, 1)

            if confirmRefresh == 'No':
                pass

        # else, we execute the apply function
        else:
            if importAssign is True:
                self.applyShaders(0, 0)
            else:
                self.applyShaders(0, 1)
        self.accept()

    def applyShaders(self, rfrsh, only):
        """Import and/or assign shaders."""
        assetGroup = cmds.ls(sl=True)

        # if we want to only import the shaders and stop here.
        # Else, we execute the applying function.
        if only == 1:
            cmds.file(
                self.shaderSceneFile,
                i=True,
                ignoreVersion=True,
                mergeNamespacesOnClash=False,
                namespace="SH_" + self.sceneName[0],
                options="v=0;p=17;f=0",
                pr=True
            )

        if only == 0:
            if rfrsh == 0:
                cmds.file(
                    self.shaderSceneFile,
                    i=True,
                    ignoreVersion=True,
                    mergeNamespacesOnClash=False,
                    namespace="SH_" + self.sceneName[0],
                    options="v=0;p=17;f=0",
                    pr=True)

            if rfrsh == 1:
                oldSaInfoAttrList = cmds.listAttr(
                    'SH_' + self.sceneName[0] + ':shadersAssignmentInfo'
                )

                cmds.delete("SH_" + self.sceneName[0] + ':*')
                shaderNamespace = cmds.namespace(
                    rm="SH_"+self.sceneName[0],
                    f=True
                )
                cmds.file(
                    self.shaderSceneFile,
                    i=True,
                    ignoreVersion=True,
                    mergeNamespacesOnClash=False,
                    namespace="SH_" + self.sceneName[0],
                    options="v=0;p=17;f=0",
                    pr=True)

                newSaInfoAttrList = cmds.listAttr(
                    'SH_' + self.sceneName[0] + ':shadersAssignmentInfo'
                )

            # list of the attributes of the assignmentInfo
            saInfoAttrs = cmds.listAttr(
                'SH_' + self.sceneName[0] + ':shadersAssignmentInfo'
            )

            # getting the values from the assignmentInfo and operating them
            shaderInfoAttrList = []
            missingObjects = []
            missingObjShader = []

            # we extract each attribut "shaderInfo" name from the assignmentInfo
            for attribut in saInfoAttrs:
                attributName = attribut.split('shaderInfo')
                if len(attributName) == 2:
                    shaderInfoAttrList.append(attribut)

            # we get the info from each shading info attribut
            for attribut in shaderInfoAttrList:
                attributInfo = cmds.getAttr(
                    'SH_' +
                    self.sceneName[0] +
                    ':shadersAssignmentInfo.' +
                    attribut
                ).split(' = ')

                if len(attributInfo) == 2:
                    # if the object has the lambert1 shader
                    # (initialShadingGroup),
                    # then select the existing initialShadingGroup
                    if attributInfo[1] == 'initialShadingGroup':
                        cmds.select('initialShadingGroup', ne=True, r=True)
                    else:
                        cmds.select(
                            "SH_" + self.sceneName[0] + ':' + attributInfo[1],
                            ne=True,
                            r=True
                        )

                    shadingGroup = cmds.ls(sl=True)
                    object = []
                    if len(assetGroup) > 0:
                        assetGroupRelatives = cmds.listRelatives(
                            assetGroup[0], ad=True, f=True
                        )

                    if len(assetGroup) == 0:
                        assetGroupRelatives = cmds.ls()

                    for element in assetGroupRelatives:
                        if len(element.split(attributInfo[0])) == 2:
                            object.append(element)
                        else:
                            pass

                    if len(object) == 1:
                        cmds.select(object[0], r=True)
                        cmds.sets(e=True, forceElement=shadingGroup[0])

                    if len(object) > 1:
                        cmds.confirmDialog(
                            title='Warning',
                            message='More than one object matches name ' +
                            attributInfo[0] +
                            (
                                " in the scene.\nTo avoid this problem,"
                                "select in the outliner the group where the"
                                "asset is (for example 'asset/geo') and"
                                "refresh the shaders importing them again "
                                "with the tool."
                            ),
                            ma='center',
                            button=['Okay']
                        )
                        break

                    if len(object) == 0:
                        missingObjects.append(attributInfo[0])
                        missingObjShader.append(
                            ' shadered with : ' + attributInfo[1]
                        )
                else:
                    pass

            attrDifference = len(shaderInfoAttrList) - len(saInfoAttrs)

            if rfrsh == 1:
                if newSaInfoAttrList < oldSaInfoAttrList:
                    cmds.confirmDialog(
                        title='Warning',
                        message=(
                            "The new imported shader scene has less"
                            "shaders than before :"
                        ) + str(len(
                            newSaInfoAttrList - attrDifference)
                        ) + " now, " +
                        str(len(oldSaInfoAttrList - attrDifference)) +
                        ' before). This means ' +
                        str(len(oldSaInfoAttrList) -
                            len(newSaInfoAttrList)) + (
                            "objects may have lost their shaders because"
                            "either their shaders were not exported,"
                            "either they don\'t exist anymore.\n\n"
                            "If happens (objects turning into a neon-green"
                            "color) try to export again all the shaders"
                            "from the shading scene, or give another name"
                            "to the exported shader scene to"
                            "avoid overwriting."
                        ),
                        ma='center',
                        button=['Okay'])

            # if object are missing
            if len(missingObjects) > 0:
                objectListString = '\n'.join(missingObjects)
                shaderListString = '\n'.join(missingObjShader)
                if (cmds.window('warningWindow', exists=True)):
                    cmds.deleteUI('warningWindow')

                cmds.window('warningWindow', title="Warning", titleBarMenu=True)
                cmds.columnLayout(
                    cal='center',
                    width=440,
                    rowSpacing=10,
                    columnAttach=('left', 40)
                )
                cmds.separator(height=15, style='none')
                cmds.text(
                    label=(
                        "Following objects were missing,"
                        "or have a different name in the shader scene :"
                    ),
                    al='left'
                )
                cmds.rowColumnLayout(
                    numberOfColumns=4,
                    columnWidth=[
                        (1, 10),
                        (2, 180),
                        (3, 300),
                        (4, 10)
                    ]
                )
                cmds.text(label='', al='left')
                cmds.text(label=objectListString, al='left')
                cmds.text(label=shaderListString, al='left', en=False)
                cmds.text(label='', al='left')
                cmds.separator(height=20, style='none')
                cmds.showWindow()
