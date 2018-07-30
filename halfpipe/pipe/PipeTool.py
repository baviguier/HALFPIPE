# -*- coding: utf-8 -*-
"""Half Pipe Code.

Version 0.3.0
"""

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import datetime
import fnmatch
from functools import partial
import glob
import json
import maya.mel
import os
from os import listdir
from os.path import isfile
from os.path import join
import re
import shutil
import subprocess
import time

import maya.cmds as mc
import maya.cmds

from pipe.utils import DEFAULT_COLOR
from pipe.utils import HALFPIPE_PATH_FILE
from pipe.utils import PROJECT_SETTINGS_FILE
from pipe.utils import SETTINGS_FILE

from pipe.AssignExport import ExportShaders
from pipe.AssignImport import ImportShaders
from pipe.BackUpDialog import BackUp
from pipe.Prefill import Prefill
from pipe.ProjectSettingsDialog import ProjectSettings
from pipe.ReferenceDialog import ReferenceDialog
from pipe.SaveMasterDialog import SetSaveMasterDialog
from pipe.SectorSettingsDialog import SectorSettingsDialog
from pipe.SetProjectDialog import SetProjectDialog

from pipe.utils import formatName
from pipe.utils import formatText
from pipe.utils import load_icon


class Ui_pipeForm(object):
    """Main UI."""

    # ####################################################################### #
    #                                   UI                                    #
    # ####################################################################### #

    def setupUi(self, pipeForm):
        """Define Main UI."""
        pipeForm.setObjectName("pipeForm")
        pipeForm.resize(510, 900)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(pipeForm)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pipeWidget = QtWidgets.QWidget(pipeForm)
        self.pipeWidget.setObjectName("pipeWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pipeWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.titleLayout = QtWidgets.QVBoxLayout()
        self.titleLayout.setSpacing(3)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleLayout.setObjectName("titleLayout")
        self.projectPathLabel = QtWidgets.QLabel(self.pipeWidget)
        # font = QtWidgets.QFont()
        # font.setItalic(True)
        # self.projectPathLabel.setFont(font)
        self.projectPathLabel.setObjectName("projectPathLabel")
        self.titleLayout.addWidget(self.projectPathLabel)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.projectImage = QtWidgets.QLabel(self.pipeWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.projectImage.sizePolicy().hasHeightForWidth()
        )
        self.projectImage.setSizePolicy(sizePolicy)
        self.projectImage.setMinimumSize(QtCore.QSize(0, 80))
        self.projectImage.setMaximumSize(QtCore.QSize(16777215, 80))
        self.projectImage.setAutoFillBackground(True)
        # self.projectImage.setFrameShape(QtWidgets.QFrame.Box)
        # self.projectImage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.projectImage.setTextFormat(QtCore.Qt.AutoText)
        self.projectImage.setAlignment(QtCore.Qt.AlignCenter)
        self.projectImage.setObjectName("projectImage")
        self.verticalLayout.addWidget(self.projectImage)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(0, 3, 0, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectName = QtWidgets.QPushButton(self.pipeWidget)
        self.projectName.setMinimumSize(QtCore.QSize(0, 25))
        # font = QtWidgets.QFont()
        # font.setWeight(50)
        # font.setBold(False)
        # self.projectName.setFont(font)
        # self.projectName.setFrameShape(QtWidgets.QFrame.Box)
        # self.projectName.setAlignment(QtCore.Qt.AlignCenter)
        self.projectName.setObjectName("projectName")
        self.horizontalLayout.addWidget(self.projectName)
        self.settingsProjectButton = QtWidgets.QPushButton(self.pipeWidget)
        self.settingsProjectButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.settingsProjectButton.setObjectName("settingsProjectButton")
        self.horizontalLayout.addWidget(self.settingsProjectButton)
        self.backUpButton = QtWidgets.QPushButton(self.pipeWidget)
        self.backUpButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.backUpButton.setObjectName("backUpButton")
        self.horizontalLayout.addWidget(self.backUpButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.titleLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.titleLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.pipeWidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setObjectName("tabWidget")
        self.projectTab = QtWidgets.QWidget()
        self.projectTab.setObjectName("projectTab")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.projectTab)
        self.verticalLayout_18.setSpacing(3)
        self.verticalLayout_18.setContentsMargins(3, 12, 3, 3)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.projectSplitter = QtWidgets.QSplitter(self.projectTab)
        self.projectSplitter.setOrientation(QtCore.Qt.Vertical)
        self.projectSplitter.setObjectName("projectSplitter")
        self.layoutWidget_2 = QtWidgets.QWidget(self.projectSplitter)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.browserLayout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.browserLayout.setSpacing(8)
        self.browserLayout.setContentsMargins(0, 0, 0, 3)
        self.browserLayout.setObjectName("browserLayout")
        self.navigationLayout = QtWidgets.QVBoxLayout()
        self.navigationLayout.setSpacing(3)
        self.navigationLayout.setContentsMargins(0, 0, 0, 0)
        self.navigationLayout.setObjectName("navigationLayout")
        self.sectorLayout = QtWidgets.QHBoxLayout()
        self.sectorLayout.setSpacing(3)
        self.sectorLayout.setContentsMargins(0, 0, 0, 0)
        self.sectorLayout.setObjectName("sectorLayout")
        self.sectorComboBox = QtWidgets.QComboBox(self.layoutWidget_2)
        # font = QtWidgets.QFont()
        # self.sectorComboBox.setFont(font)
        self.sectorComboBox.setObjectName("sectorComboBox")
        self.sectorComboBox.setMinimumSize(QtCore.QSize(16777215, 25))
        self.sectorLayout.addWidget(self.sectorComboBox)
        self.settingsSectorButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.settingsSectorButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.settingsSectorButton.setObjectName("settingsSectorButton")
        self.sectorLayout.addWidget(self.settingsSectorButton)
        self.navigationLayout.addLayout(self.sectorLayout)
        self.browserTableLayout = QtWidgets.QHBoxLayout()
        self.browserTableLayout.setSpacing(3)
        self.browserTableLayout.setContentsMargins(0, 0, 0, 0)
        self.browserTableLayout.setObjectName("browserTableLayout")
        self.sequenceLayout = QtWidgets.QVBoxLayout()
        self.sequenceLayout.setSpacing(3)
        self.sequenceLayout.setObjectName("sequenceLayout")
        self.sequenceTitleLayout = QtWidgets.QVBoxLayout()
        self.sequenceTitleLayout.setSpacing(0)
        self.sequenceTitleLayout.setContentsMargins(0, 0, 0, 0)
        self.sequenceTitleLayout.setObjectName("sequenceTitleLayout")
        self.sequenceLabel = QtWidgets.QLabel(self.layoutWidget_2)
        self.sequenceLabel.setMinimumSize(QtCore.QSize(0, 22))
        self.sequenceLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        # font = QtWidgets.QFont()
        # font.setWeight(50)
        # font.setBold(False)
        # self.sequenceLabel.setFont(font)
        # self.sequenceLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.sequenceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sequenceLabel.setObjectName("sequenceLabel")
        self.sequenceTitleLayout.addWidget(self.sequenceLabel)
        self.sequenceButtonsLayout = QtWidgets.QHBoxLayout()
        self.sequenceButtonsLayout.setSpacing(3)
        self.sequenceButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.sequenceButtonsLayout.setObjectName("sequenceButtonsLayout")
        self.sequencePlusButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.sequencePlusButton.setObjectName("sequencePlusButton")
        self.sequenceButtonsLayout.addWidget(self.sequencePlusButton)
        self.sequenceMinusButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.sequenceMinusButton.setObjectName("sequenceMinusButton")
        self.sequenceButtonsLayout.addWidget(self.sequenceMinusButton)
        self.sequenceTitleLayout.addLayout(self.sequenceButtonsLayout)
        self.sequenceLayout.addLayout(self.sequenceTitleLayout)
        self.sequenceList = QtWidgets.QListWidget(self.layoutWidget_2)
        self.sequenceList.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sequenceList.setObjectName("sequenceList")
        self.sequenceLayout.addWidget(self.sequenceList)
        self.browserTableLayout.addLayout(self.sequenceLayout)
        self.sceneLayout = QtWidgets.QVBoxLayout()
        self.sceneLayout.setSpacing(3)
        self.sceneLayout.setObjectName("sceneLayout")
        self.sceneTitleLayout = QtWidgets.QVBoxLayout()
        self.sceneTitleLayout.setSpacing(0)
        self.sceneTitleLayout.setContentsMargins(0, 0, 0, 0)
        self.sceneTitleLayout.setObjectName("sceneTitleLayout")
        self.sceneLabel = QtWidgets.QLabel(self.layoutWidget_2)
        self.sceneLabel.setMinimumSize(QtCore.QSize(0, 22))
        self.sceneLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        # font = QtWidgets.QFont()
        # font.setWeight(50)
        # font.setBold(False)
        # self.sceneLabel.setFont(font)
        # self.sceneLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.sceneLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sceneLabel.setObjectName("sceneLabel")
        self.sceneTitleLayout.addWidget(self.sceneLabel)
        self.sceneButtonsLayout = QtWidgets.QHBoxLayout()
        self.sceneButtonsLayout.setSpacing(3)
        self.sceneButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.sceneButtonsLayout.setObjectName("sceneButtonsLayout")
        self.scenePlusButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.scenePlusButton.setObjectName("scenePlusButton")
        self.sceneButtonsLayout.addWidget(self.scenePlusButton)
        self.sceneMinusButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.sceneMinusButton.setObjectName("sceneMinusButton")
        self.sceneButtonsLayout.addWidget(self.sceneMinusButton)
        self.sceneTitleLayout.addLayout(self.sceneButtonsLayout)
        self.sceneLayout.addLayout(self.sceneTitleLayout)
        self.sceneList = QtWidgets.QListWidget(self.layoutWidget_2)
        self.sceneList.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sceneList.setObjectName("sceneList")
        self.sceneLayout.addWidget(self.sceneList)
        self.browserTableLayout.addLayout(self.sceneLayout)
        self.navigationLayout.addLayout(self.browserTableLayout)
        self.browserLayout.addLayout(self.navigationLayout)
        self.sceneInfoLayout = QtWidgets.QVBoxLayout()
        self.sceneInfoLayout.setSpacing(3)
        self.sceneInfoLayout.setContentsMargins(0, 0, 0, 0)
        self.sceneInfoLayout.setObjectName("sceneInfoLayout")
        self.sceneImage = QtWidgets.QLabel(self.layoutWidget_2)
        self.sceneImage.setMinimumSize(QtCore.QSize(200, 113))
        self.sceneImage.setMaximumSize(QtCore.QSize(200, 113))
        self.sceneImage.setAutoFillBackground(True)
        # self.sceneImage.setFrameShape(QtWidgets.QFrame.Box)
        self.sceneImage.setAlignment(QtCore.Qt.AlignCenter)
        self.sceneImage.setObjectName("sceneImage")
        self.sceneInfoLayout.addWidget(self.sceneImage)
        self.sceneSnapshotLayout = QtWidgets.QHBoxLayout()
        self.sceneSnapshotLayout.setSpacing(6)
        self.sceneSnapshotLayout.setObjectName("sceneSnapshotLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.sceneSnapshotLayout.addItem(spacerItem)
        self.snapshotButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.snapshotButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.snapshotButton.setObjectName("snapshotButton")
        self.sceneSnapshotLayout.addWidget(self.snapshotButton)
        self.importButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.importButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.importButton.setObjectName("importButton")
        self.sceneSnapshotLayout.addWidget(self.importButton)
        self.sceneInfoLayout.addLayout(self.sceneSnapshotLayout)
        self.ref_scene_button = QtWidgets.QPushButton(self.layoutWidget_2)
        self.ref_scene_button.setMinimumSize(QtCore.QSize(0, 30))
        self.ref_scene_button.setObjectName("ref_scene_button")
        self.sceneInfoLayout.addWidget(self.ref_scene_button)
        self.import_scene_button = QtWidgets.QPushButton(self.layoutWidget_2)
        self.import_scene_button.setMinimumSize(QtCore.QSize(0, 30))
        self.import_scene_button.setObjectName("import_scene_button")
        self.sceneInfoLayout.addWidget(self.import_scene_button)
        self.sceneFormLayout = QtWidgets.QFormLayout()
        self.sceneFormLayout.setContentsMargins(3, 0, 0, 0)
        self.sceneFormLayout.setSpacing(6)
        self.sceneFormLayout.setObjectName("sceneFormLayout")
        self.versionLabel01 = QtWidgets.QLabel(self.layoutWidget_2)
        self.versionLabel01.setObjectName("versionLabel01")
        self.sceneFormLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.versionLabel01
        )
        self.versionAnswerLabel01 = QtWidgets.QLabel(self.layoutWidget_2)
        self.versionAnswerLabel01.setObjectName("versionAnswerLabel01")
        self.sceneFormLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.versionAnswerLabel01
        )
        self.dateLabel01 = QtWidgets.QLabel(self.layoutWidget_2)
        self.dateLabel01.setObjectName("dateLabel01")
        self.sceneFormLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.dateLabel01
        )
        self.dateAnswerLabel01 = QtWidgets.QLabel(self.layoutWidget_2)
        self.dateAnswerLabel01.setObjectName("dateAnswerLabel01")
        self.sceneFormLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.dateAnswerLabel01
        )
        self.artistLabel01 = QtWidgets.QLabel(self.layoutWidget_2)
        self.artistLabel01.setObjectName("artistLabel01")
        self.sceneFormLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.artistLabel01
        )
        self.artistAnswerLabel01 = QtWidgets.QComboBox(self.layoutWidget_2)
        self.artistAnswerLabel01.setMinimumSize(QtCore.QSize(16777215, 25))
        self.artistAnswerLabel01.setObjectName("artistAnswerLabel01")
        self.sceneFormLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.artistAnswerLabel01
        )
        self.commentLabel01 = QtWidgets.QLabel(self.layoutWidget_2)
        self.commentLabel01.setObjectName("commentLabel01")
        self.sceneFormLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.commentLabel01
        )
        self.commentAnswerLabel01 = QtWidgets.QPlainTextEdit(
            self.layoutWidget_2
        )
        # self.commentAnswerLabel01.setAlignment(
        #     QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        # )
        self.commentAnswerLabel01.setObjectName("commentAnswerLabel01")
        self.commentAnswerLabel01.setMinimumSize(QtCore.QSize(0, 25))
        self.commentAnswerLabel01.setMaximumSize(QtCore.QSize(16777215, 80))
        self.sceneFormLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.commentAnswerLabel01
        )
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.sceneFormLayout.setItem(
            4, QtWidgets.QFormLayout.LabelRole, spacerItem1
        )
        self.sceneInfoLayout.addLayout(self.sceneFormLayout)
        self.browserLayout.addLayout(self.sceneInfoLayout)
        self.layoutWidget_3 = QtWidgets.QWidget(self.projectSplitter)
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.sceneHistoryLayout = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.sceneHistoryLayout.setSpacing(5)
        self.sceneHistoryLayout.setContentsMargins(0, 0, 0, 0)
        self.sceneHistoryLayout.setObjectName("sceneHistoryLayout")
        self.sceneHistoryLabel = QtWidgets.QLabel(self.layoutWidget_3)
        self.sceneHistoryLabel.setObjectName("sceneHistoryLabel")
        self.sceneHistoryLayout.addWidget(self.sceneHistoryLabel)
        self.sceneHistoryTable = QtWidgets.QTableWidget(self.layoutWidget_3)
        self.sceneHistoryTable.setObjectName("sceneHistoryTable")
        self.sceneHistoryTable.setColumnCount(5)
        self.sceneHistoryTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.sceneHistoryTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sceneHistoryTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sceneHistoryTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sceneHistoryTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.sceneHistoryTable.setHorizontalHeaderItem(4, item)
        self.sceneHistoryTable.horizontalHeader().setVisible(True)
        self.sceneHistoryTable.verticalHeader().setVisible(False)
        # self.sceneHistoryTable.horizontalHeader().setStretchLastSection(True)
        self.sceneHistoryTable.setColumnWidth(0, 90)
        self.sceneHistoryTable.setColumnWidth(1, 100)
        self.sceneHistoryTable.setColumnWidth(2, 100)
        self.sceneHistoryTable.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch
        )
        self.sceneHistoryTable.setColumnWidth(4, 30)
        self.sceneHistoryTable.resizeRowsToContents()
        # self.sceneHistoryTable.horizontalHeader().setResizeMode(
        #   QtGui.QHeaderView.Stretch
        # )
        self.sceneHistoryLayout.addWidget(self.sceneHistoryTable)
        self.projectSplitter.setStretchFactor(0, 5)
        self.projectSplitter.setStretchFactor(1, 10)
        self.verticalLayout_18.addWidget(self.projectSplitter)
        self.tabWidget.addTab(self.projectTab, "")
        self.currentSceneTab = QtWidgets.QWidget()
        self.currentSceneTab.setObjectName("currentSceneTab")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.currentSceneTab)
        self.verticalLayout_17.setSpacing(6)
        self.verticalLayout_17.setContentsMargins(3, 12, 3, 3)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.currentSceneLayout = QtWidgets.QHBoxLayout()
        self.currentSceneLayout.setSpacing(3)
        self.currentSceneLayout.setObjectName("currentSceneLayout")
        self.sceneThumbnailLayout = QtWidgets.QVBoxLayout()
        self.sceneThumbnailLayout.setSpacing(3)
        self.sceneThumbnailLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint
        )
        self.sceneThumbnailLayout.setContentsMargins(0, 0, 0, 0)
        self.sceneThumbnailLayout.setObjectName("sceneThumbnailLayout")
        self.currentSceneImage = QtWidgets.QLabel(self.currentSceneTab)
        self.currentSceneImage.setMinimumSize(QtCore.QSize(200, 113))
        self.currentSceneImage.setMaximumSize(QtCore.QSize(200, 113))
        self.currentSceneImage.setAutoFillBackground(True)
        # self.currentSceneImage.setFrameShape(QtWidgets.QFrame.Box)
        self.currentSceneImage.setAlignment(QtCore.Qt.AlignCenter)
        self.currentSceneImage.setObjectName("currentSceneImage")
        self.sceneThumbnailLayout.addWidget(self.currentSceneImage)
        self.snapshotLayout = QtWidgets.QHBoxLayout()
        self.snapshotLayout.setSpacing(6)
        self.snapshotLayout.setContentsMargins(0, 0, 0, 0)
        self.snapshotLayout.setObjectName("snapshotLayout")
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.snapshotLayout.addItem(spacerItem2)
        self.currentSnapshotButton = QtWidgets.QPushButton(
            self.currentSceneTab
        )
        self.currentSnapshotButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.currentSnapshotButton.setObjectName("currentSnapshotButton")
        self.snapshotLayout.addWidget(self.currentSnapshotButton)
        self.currentImportButton = QtWidgets.QPushButton(self.currentSceneTab)
        self.currentImportButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.currentImportButton.setObjectName("currentImportButton")
        self.snapshotLayout.addWidget(self.currentImportButton)
        self.sceneThumbnailLayout.addLayout(self.snapshotLayout)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 0, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.sceneThumbnailLayout.addItem(spacerItem3)
        self.currentSceneLayout.addLayout(self.sceneThumbnailLayout)
        self.currentSceneFormLayout = QtWidgets.QFormLayout()
        self.currentSceneFormLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint
        )
        self.currentSceneFormLayout.setContentsMargins(3, 0, 0, 0)
        self.currentSceneFormLayout.setObjectName("currentSceneFormLayout")

        self.nameLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.nameLabel02.setObjectName("nameLabel02")
        self.currentSceneFormLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.nameLabel02
        )
        self.nameAnswerLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.nameAnswerLabel02.setObjectName("nameAnswerLabel02")
        self.currentSceneFormLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.nameAnswerLabel02
        )

        self.versionLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.versionLabel02.setObjectName("versionLabel02")
        self.currentSceneFormLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.versionLabel02
        )
        self.versionAnswerLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.versionAnswerLabel02.setObjectName("versionAnswerLabel02")
        self.currentSceneFormLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.versionAnswerLabel02
        )
        self.dateLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.dateLabel02.setObjectName("dateLabel02")
        self.currentSceneFormLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.dateLabel02
        )
        self.dateAnswerLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.dateAnswerLabel02.setObjectName("dateAnswerLabel02")
        self.currentSceneFormLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.dateAnswerLabel02
        )
        self.artistLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.artistLabel02.setObjectName("artistLabel02")
        self.currentSceneFormLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.artistLabel02
        )
        self.artistAnswerLabel02 = QtWidgets.QComboBox(self.currentSceneTab)
        self.artistAnswerLabel02.setMinimumSize(QtCore.QSize(16777215, 25))
        self.artistAnswerLabel02.setObjectName("artistAnswerLabel02")
        self.currentSceneFormLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.artistAnswerLabel02
        )
        self.commentLabel02 = QtWidgets.QLabel(self.currentSceneTab)
        self.commentLabel02.setObjectName("commentLabel02")
        self.currentSceneFormLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.commentLabel02
        )
        self.commentAnswerLabel02 = QtWidgets.QPlainTextEdit(
            self.currentSceneTab
        )
        # self.commentAnswerLabel02.setAlignment(
        #     QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        # )
        self.commentAnswerLabel02.setObjectName("commentAnswerLabel02")
        self.commentAnswerLabel02.setMinimumSize(QtCore.QSize(0, 25))
        self.commentAnswerLabel02.setMaximumSize(QtCore.QSize(16777215, 60))
        self.currentSceneFormLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.commentAnswerLabel02
        )
        self.currentSceneLayout.addLayout(self.currentSceneFormLayout)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.currentSceneLayout.addItem(spacerItem3)
        self.verticalLayout_17.addLayout(self.currentSceneLayout)
        self.savingLayout = QtWidgets.QVBoxLayout()
        self.savingLayout.setSpacing(3)
        self.savingLayout.setObjectName("savingLayout")
        # self.currentSceneSplitter = QtWidgets.QSplitter(self.currentSceneTab)
        # self.currentSceneSplitter.setOrientation(QtCore.Qt.Vertical)
        # self.currentSceneSplitter.setObjectName("currentSceneSplitter")
        # self.layoutWidget_4 = QtWidgets.QWidget(self.currentSceneSplitter)
        # self.layoutWidget_4.setObjectName("layoutWidget_4")

        self.exportButtonsLayout = QtWidgets.QHBoxLayout()
        self.exportButtonsLayout.setSpacing(3)
        self.exportButtonsLayout.setSizeConstraint(
            QtWidgets.QLayout.SetMaximumSize
        )
        self.exportButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.exportButtonsLayout.setObjectName("exportButtonsLayout")
        self.exportLayout = QtWidgets.QVBoxLayout()
        self.exportLayout.setSpacing(3)
        self.exportLayout.setContentsMargins(0, 0, 0, 0)
        self.exportLayout.setObjectName("exportLayout")
        self.expObjectButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.expObjectButton.sizePolicy().hasHeightForWidth()
        )
        self.expObjectButton.setSizePolicy(sizePolicy)
        self.expObjectButton.setMinimumSize(QtCore.QSize(40, 40))
        # self.expObjectButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.expObjectButton.setObjectName("expObjectButton")
        self.exportLayout.addWidget(self.expObjectButton)
        self.expAbcButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.expAbcButton.sizePolicy().hasHeightForWidth()
        )
        self.expAbcButton.setSizePolicy(sizePolicy)
        self.expAbcButton.setMinimumSize(QtCore.QSize(40, 40))
        # self.expAbcButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.expAbcButton.setObjectName("expAbcButton")
        self.exportLayout.addWidget(self.expAbcButton)
        self.exportButtonsLayout.addLayout(self.exportLayout)
        self.importLayout = QtWidgets.QVBoxLayout()
        self.importLayout.setSpacing(3)
        self.importLayout.setContentsMargins(0, 0, 0, 0)
        self.importLayout.setObjectName("importLayout")
        self.impAbcButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.impAbcButton.sizePolicy().hasHeightForWidth()
        )
        self.impAbcButton.setSizePolicy(sizePolicy)
        self.impAbcButton.setMinimumSize(QtCore.QSize(40, 40))
        # self.impAbcButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.impAbcButton.setObjectName("impAbcButton")
        self.importLayout.addWidget(self.impAbcButton)
        self.reButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.reButton.sizePolicy().hasHeightForWidth()
        )
        self.reButton.setSizePolicy(sizePolicy)
        self.reButton.setMinimumSize(QtCore.QSize(40, 40))
        # self.reButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.reButton.setObjectName("reButton")
        self.importLayout.addWidget(self.reButton)
        self.exportButtonsLayout.addLayout(self.importLayout)
        self.verticalLayout_17.addLayout(self.exportButtonsLayout)

        # self.verticalLayoutWidget = QtWidgets.QWidget(
        #     self.currentSceneSplitter
        # )
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 451, 291))
        # self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.references_layout = QtWidgets.QVBoxLayout()
        self.references_layout.setContentsMargins(0, 0, 0, 0)
        self.references_layout.setObjectName("references_layout")
        self.reference_label = QtWidgets.QLabel()
        self.reference_label.setObjectName("reference_label")
        self.references_layout.addWidget(self.reference_label)
        self.references_table = QtWidgets.QTableWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.references_table.sizePolicy().hasHeightForWidth()
        )
        self.references_table.setSizePolicy(sizePolicy)
        self.references_table.setFrameShadow(QtWidgets.QFrame.Plain)
        self.references_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.references_table.setObjectName("references_table")
        self.references_table.setColumnCount(4)
        self.references_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.references_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.references_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.references_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.references_table.setHorizontalHeaderItem(3, item)
        self.references_table.horizontalHeader().setVisible(True)
        self.references_table.verticalHeader().setVisible(False)
        self.references_table.horizontalHeader().setSortIndicatorShown(False)
        self.references_table.horizontalHeader().setStretchLastSection(True)
        self.references_table.verticalHeader().setDefaultSectionSize(57)
        self.references_table.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
        )
        self.references_layout.addWidget(self.references_table)
        self.ref_buttons_layout = QtWidgets.QHBoxLayout()
        self.ref_buttons_layout.setSpacing(6)
        self.ref_buttons_layout.setObjectName("ref_buttons_layout")
        self.namespace_button = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.namespace_button.sizePolicy().hasHeightForWidth()
        )
        self.namespace_button.setSizePolicy(sizePolicy)
        self.namespace_button.setMinimumSize(QtCore.QSize(0, 30))
        self.namespace_button.setObjectName("namespace_button")
        self.ref_buttons_layout.addWidget(self.namespace_button)
        self.reload_ref_button = QtWidgets.QPushButton(

        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.reload_ref_button.sizePolicy().hasHeightForWidth()
        )
        self.reload_ref_button.setSizePolicy(sizePolicy)
        self.reload_ref_button.setMinimumSize(QtCore.QSize(0, 30))
        self.reload_ref_button.setObjectName("reload_ref_button")
        self.ref_buttons_layout.addWidget(self.reload_ref_button)
        self.merge_ref_button = QtWidgets.QPushButton(

        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.merge_ref_button.sizePolicy().hasHeightForWidth()
        )
        self.merge_ref_button.setSizePolicy(sizePolicy)
        self.merge_ref_button.setMinimumSize(QtCore.QSize(0, 30))
        self.merge_ref_button.setObjectName("merge_ref_button")
        self.ref_buttons_layout.addWidget(self.merge_ref_button)
        self.replace_ref_button = QtWidgets.QPushButton(

        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.replace_ref_button.sizePolicy().hasHeightForWidth()
        )
        self.replace_ref_button.setSizePolicy(sizePolicy)
        self.replace_ref_button.setMinimumSize(QtCore.QSize(0, 30))
        self.replace_ref_button.setObjectName("replace_ref_button")
        self.ref_buttons_layout.addWidget(self.replace_ref_button)
        self.delete_ref_button = QtWidgets.QPushButton(

        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.delete_ref_button.sizePolicy().hasHeightForWidth()
        )
        self.delete_ref_button.setSizePolicy(sizePolicy)
        self.delete_ref_button.setMinimumSize(QtCore.QSize(0, 30))
        self.delete_ref_button.setObjectName("delete_ref_button")
        self.ref_buttons_layout.addWidget(self.delete_ref_button)
        self.references_layout.addLayout(self.ref_buttons_layout)
        self.verticalLayout_17.addLayout(self.references_layout, stretch=20)

        # self.savingLayout.addWidget(self.currentSceneSplitter)
        self.savingFooterLayout = QtWidgets.QVBoxLayout()
        self.savingFooterLayout.setSpacing(3)
        self.savingFooterLayout.setObjectName("savingFooterLayout")
        self.currentScenePathLabel = QtWidgets.QLabel(self.currentSceneTab)
        self.currentScenePathLabel.setMaximumSize(QtCore.QSize(16777215, 16))
        # font = QtWidgets.QFont()
        # font.setItalic(True)
        # self.currentScenePathLabel.setFont(font)
        self.currentScenePathLabel.setObjectName("currentScenePathLabel")
        self.savingFooterLayout.addWidget(self.currentScenePathLabel)
        self.savingButtonsLayout = QtWidgets.QHBoxLayout()
        self.savingButtonsLayout.setSpacing(3)
        self.savingButtonsLayout.setSizeConstraint(
            QtWidgets.QLayout.SetMaximumSize
        )
        self.savingButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.savingButtonsLayout.setObjectName("savingButtonsLayout")
        self.saveVersionButton = QtWidgets.QPushButton(self.currentSceneTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.saveVersionButton.sizePolicy().hasHeightForWidth()
        )
        self.saveVersionButton.setSizePolicy(sizePolicy)
        self.saveVersionButton.setMinimumSize(QtCore.QSize(0, 40))
        self.saveVersionButton.setMaximumSize(QtCore.QSize(16777215, 55))
        self.saveVersionButton.setObjectName("saveVersionButton")
        self.savingButtonsLayout.addWidget(self.saveVersionButton)
        self.saveMasterButton = QtWidgets.QPushButton(self.currentSceneTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.saveMasterButton.sizePolicy().hasHeightForWidth()
        )
        self.saveMasterButton.setSizePolicy(sizePolicy)
        self.saveMasterButton.setMinimumSize(QtCore.QSize(0, 40))
        self.saveMasterButton.setMaximumSize(QtCore.QSize(16777215, 55))
        self.saveMasterButton.setObjectName("saveMasterButton")
        self.savingButtonsLayout.addWidget(self.saveMasterButton)
        self.savingFooterLayout.addLayout(self.savingButtonsLayout)
        self.savingLayout.addLayout(self.savingFooterLayout)
        self.verticalLayout_17.addLayout(self.savingLayout)
        self.tabWidget.addTab(self.currentSceneTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout_3.addWidget(self.pipeWidget)

        self.retranslateUi(pipeForm)
        QtCore.QMetaObject.connectSlotsByName(pipeForm)

    def retranslateUi(self, pipeForm):
        """Retranslating the UI."""
        pipeForm.setWindowTitle("Pipe")
        self.projectPathLabel.setText("Pipe Path")
        self.projectImage.setText("Project Image")
        self.projectName.setText("PROJECT NAME")
        self.settingsProjectButton.setText("O")
        self.backUpButton.setText("B")
        self.settingsSectorButton.setText("O")
        self.sequenceLabel.setText("CATEGORY")
        self.sequencePlusButton.setText("+")
        self.sequenceMinusButton.setText("-")
        self.sceneLabel.setText("SCENE")
        self.scenePlusButton.setText("+")
        self.sceneMinusButton.setText("-")
        self.sceneImage.setText("Scene Picture")
        self.snapshotButton.setText("S")
        self.importButton.setText("I")
        self.ref_scene_button.setText("Reference Scene")
        self.import_scene_button.setText("Import Scene")
        self.versionLabel01.setText("VERSION:")
        self.versionAnswerLabel01.setText("")
        self.dateLabel01.setText("DATE:")
        self.dateAnswerLabel01.setText("")
        self.artistLabel01.setText("ARTIST:")
        # self.artistAnswerLabel01.setText("")
        self.commentLabel01.setText("COMMENT:")
        # self.commentAnswerLabel01.setText("")
        self.sceneHistoryLabel.setText("Selected Scene History:")
        self.sceneHistoryTable.horizontalHeaderItem(0).setText("VERSION")
        self.sceneHistoryTable.horizontalHeaderItem(1).setText("DATE")
        self.sceneHistoryTable.horizontalHeaderItem(2).setText("ARTIST")
        self.sceneHistoryTable.horizontalHeaderItem(3).setText("COMMENT")
        self.sceneHistoryTable.horizontalHeaderItem(4).setText("X")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.projectTab), "PROJECT"
        )
        self.currentSceneImage.setText("Scene Picture")
        self.currentSnapshotButton.setText("S")
        self.currentImportButton.setText("I")
        # self.renderSettingsComboBox.addItem('No render settings set.')
        # self.importRenderSettingsButton.setText("I")
        self.nameLabel02.setText("SCENE:")
        self.nameAnswerLabel02.setText("")
        self.versionLabel02.setText("VERSION:")
        self.versionAnswerLabel02.setText("")
        self.dateLabel02.setText("DATE:")
        self.dateAnswerLabel02.setText("")
        self.artistLabel02.setText("ARTIST:")
        # self.artistAnswerLabel02.setText("")
        self.commentLabel02.setText("COMMENT:")
        # self.commentAnswerLabel02.setText("")
        self.expObjectButton.setText("Export Object")
        self.expAbcButton.setText("Export Alembic")
        self.impAbcButton.setText("Imp / Ref Alembic")
        self.reButton.setText("Reference Editor")
        self.currentScenePathLabel.setText("Path Scene:")
        self.saveVersionButton.setText("SAVE VERSION")
        self.saveMasterButton.setText("SAVE MASTER")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.currentSceneTab), "CURRENT SCENE"
        )

        self.reference_label.setText("References in the scene:")
        item = self.references_table.horizontalHeaderItem(0)
        item.setText("SNAPSHOT")
        item = self.references_table.horizontalHeaderItem(1)
        item.setText("SCENE")
        item = self.references_table.horizontalHeaderItem(2)
        item.setText("ARTIST")
        item = self.references_table.horizontalHeaderItem(3)
        item.setText("DATE")
        self.namespace_button.setText("Namespace")
        self.reload_ref_button.setText("Reload")
        self.merge_ref_button.setText("Import")
        self.replace_ref_button.setText("Replace")
        self.delete_ref_button.setText("Delete")


class ImgWidget(QtWidgets.QLabel):
    """Put an image in a label."""

    def __init__(self, imagePath, parent=None):
        """Set a pixmap for a given path."""
        super(ImgWidget, self).__init__(parent)

        full_image_path = os.path.join(
            os.path.split(__file__)[0],
            "..",
            imagePath
        )
        pic = QtGui.QPixmap(full_image_path)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setScaledContents(True)
        self.setPixmap(pic)


class PipeTool(QtWidgets.QWidget):
    """Code the main UI."""

    workspace_folder_list = dict([
        ('preprod', '1_PREPROD'),
        ('prod', '2_PROD'),
        ('postprod', '3_POSTPROD'),
        ('input', '4_INPUT'),
        ('data', '5_DATA'),
        ('output', '6_OUTPUT')
    ])

    data_folder_name = '_DATA'
    data_file_name = 'scene_info.json'
    snapshot_file_name = 'snapshot.png'
    version_folder_name = "_VERSIONS"

    refresh_freq = 10000  # milisec

    master_icon = QtGui.QIcon(os.path.join(
        os.path.split(__file__)[0],
        "..",
        "icons",
        "lock33.png"
    ))

    trash_icon = QtGui.QIcon(os.path.join(
        os.path.split(__file__)[0],
        "..",
        "icons",
        "trash.png"
    ))

    def __init__(self):
        """Initialize methods necessary for the main Ui."""
        super(PipeTool, self).__init__()

        # ################################################################### #
        #                          Default Variables                          #
        # ################################################################### #
        self.path_settings_file = os.path.join(
            HALFPIPE_PATH_FILE, SETTINGS_FILE
        )

        self.sequence_label = None
        self.current_sequence_path = None
        self.current_sequence_path = None
        self.current_scene_path = None
        self.back_up_destination_path = None
        self.back_up_selected_checkboxes = []
        self.loaded_data = None
        self.scene_image_path = None
        self.selected_ref_names = []
        self.number_of_ref_rows_selected = None
        self.last_version_path = None
        self.master_path = None
        self.abc_path = None
        self.master_name = None
        self.users_list = []
        self.default_sector_namespace = None
        self.ref_paths = []
        self.project_settings_path = None
        self.project_path = None
        self.full_project_path = None
        self.banner_path = r'icons\banner_purple_t.png'
        self.username = 'Undefined'
        self.prefix_dict = {}
        self.deleting_all = False

        # self.reference_checker = mc.scriptJob(
        #     cf=['readingFile', getSelfAndUpdate]
        # )
        self.timer = QtCore.QTimer(self)
        # self.timer.start(self.refresh_freq)

        self.default_folders = [
            '1_MODELING', '5_LAYOUT', '2_RIG', '3_ANIMATION',
            '4_TEXTURING', '6_FX', '7_RENDER'
        ]

        # ################################################################### #
        #                   Initialize Mandatory Functions                    #
        # ################################################################### #

        self.ui = Ui_pipeForm()
        self.ui.setupUi(self)
        self.setHeader()
        self.menu()
        self.sceneMenu()
        self.mapEvents()
        self.updateProject()
        self.updateFromProjectSettings()
        self.createMELworkspace()
        self.styleSheetMethods()

        self.ui.tabWidget.setCurrentIndex(0)

    def menu(self):
        """Change the Project Name QPushButton to a menu."""
        menu = QtWidgets.QMenu()
        menu.addAction(
            'Change Banner', self.importBanner
        )
        menu.addAction(
            'Reset Banner', self.resetBanner
        )
        menu.addAction(
            'Change Half Pipe Color', self.changeColor
        )
        menu.addAction(
            'Reset Half Pipe Color', self.resetColor
        )
        menu.addAction(
            'Project Settings', self.projectSettings
        )
        menu.addAction(
            'Pre Fill Options', self.prefillOptions
        )
        menu.addAction(
            'View Help', self.viewHelp
        )

        menu.setStyleSheet("""
            QMenu{
                color: #EBEBEB;
                background-color: #282828;
            }

            QMenu::item:selected{
                background-color: #4F82A1;
                color: #EBEBEB;
            }

        """)

        self.ui.projectName.setMenu(menu)
        self.ui.projectName.menu()

    def updateFromProjectSettings(self):
        """Change the settings by reading the project settings file."""
        if self.full_project_path is None:
            self.custom_color = DEFAULT_COLOR
            return

        # Load the json file.
        self.project_settings_path = os.path.normpath(os.path.join(
            self.full_project_path,
            PROJECT_SETTINGS_FILE
        ))
        if os.path.exists(self.project_settings_path):
            with open(self.project_settings_path, 'r') as settings_file:
                data = json.loads(settings_file.read())
        else:
            data = dict({
                'users_list': ['Undefined', 'Sansa', 'Cersei', 'Dany'],
                'fps': 'film'
            })
            with open(self.project_settings_path, 'w') as settings_file:
                settings_file.write(json.dumps(data))

        # Check for integrity of the file.
        if (
            not data or
            'users_list' not in data or
            not data['users_list'] or
            'fps' not in data or
            not data['fps']
        ):
            raise ValueError('Error while getting data.')

        # Change the username
        self.project_name = os.path.split(self.data['last_project'])[-1]

        if (
            not self.data or
            self.project_name not in self.data or
            not self.data[self.project_name]
        ):
            self.username = 'Undefined'
        else:
            self.username = self.data[self.project_name]

        # Change the color.
        if (
            not data or
            'color' not in data or
            not data['color']
        ):
            self.custom_color = DEFAULT_COLOR
        if data['color'] != "No Color Set":
            self.custom_color = data['color']
        else:
            self.custom_color = DEFAULT_COLOR

        self.users_list = data['users_list']
        self.project_fps = data['fps']
        mc.currentUnit(time=self.project_fps)

        if (
            not data or
            'prefix' not in data or
            not data['prefix']
        ):
            self.prefix_dict = {}
        else:
            self.prefix_dict = data['prefix']

        # Change the combobox
        self.ui.artistAnswerLabel01.setCurrentText('Undefined')
        self.ui.artistAnswerLabel02.setCurrentText(self.username)

    def setHeader(self):
        """Set Icon in QTableView."""
        headerItem = QtWidgets.QTableWidgetItem("")
        headerItem.setIcon(self.trash_icon)
        headerItem.setTextAlignment(QtCore.Qt.AlignHCenter)

        self.ui.sceneHistoryTable.setHorizontalHeaderItem(4, headerItem)

    def styleSheetMethods(self):
        """Edit the UI."""
        self.ui.tabWidget.setStyleSheet("""
            QTabWidget::pane { /* The tab widget frame */
                border-top: 0px;
            }

            QTabBar::tab {
                /* Text color */
                color: #A6A6A6;
                border: 0px solid #000000;
                border-bottom: 2px solid #333333;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 3px 5px 3px 5px;
                margin: 7px 10px 0px 7px;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                border-bottom-color: """ + self.custom_color + """;
            }
        """)

        self.ui.projectName.setStyleSheet("""
            QPushButton { background-color: #353535;
            border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #292929;
                border-radius: 12px;
            }
            QPushButton:pressed {
                background-color: #282828;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 12px;
            }

            QPushButton::menu-indicator {
                image: url(noimg);
                border-width: 0px;
                border: 0px;
            }
        """)

        self.ui.projectImage.setStyleSheet("""
            QLabel {
                background-color: #353535;
                border-radius: 11px;
            }

            QLabel:hover{
                background-color: #292929;
                filter: brightness(120%);
            }
        """)

        self.ui.currentSceneImage.setStyleSheet("""
            background-color: #393939;
            border-radius: 11px;
        """)

        self.ui.sceneImage.setStyleSheet("""
            background-color: #393939;
            border-radius: 11px;
        """)

        self.ui.ref_scene_button.setStyleSheet("""
            QPushButton { background-color: #555555;
            border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #666666;
                border-radius: 12px;
            }
            QPushButton:pressed {
                background-color: #EBEBEB;
                border-radius: 12px;
            }
        """)

        self.ui.import_scene_button.setStyleSheet("""
            QPushButton { background-color: #555555;
            border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #666666;
                border-radius: 12px;
            }
            QPushButton:pressed {
                background-color: #EBEBEB;
                border-radius: 12px;
            }
        """)

        self.ui.sequenceList.setStyleSheet("""
            QListWidget{
                selection-background-color:""" + self.custom_color + """;
            }
        """)
        self.ui.sceneList.setStyleSheet("""
            QListWidget{
                selection-background-color:""" + self.custom_color + """;
            }
        """)

        self.ui.artistAnswerLabel01.setStyleSheet("""
        QComboBox {
            min-width: 10em;
        }
        """)

        self.ui.commentAnswerLabel01.setStyleSheet("""
            QPlainTextEdit {
                background: #444444;
                border: 0px solid #444444;
            }
            QPlainTextEdit:focus {
                border-radius: 13px;
                color: #FFFFFF;
                background: #333333;
                border: 0px solid #282828;
            }
        """)

        self.ui.commentAnswerLabel02.setStyleSheet("""
            QPlainTextEdit {
                background: #444444;
                border: 0px solid #444444;
            }
            QPlainTextEdit:focus {
                border-radius: 13px;
                color: #FFFFFF;
                background: #333333;
                border: 0px solid #282828;
            }
        """)

        self.ui.sceneHistoryTable.setStyleSheet("""
            QTableView {
                color: #A6A6A6;
                border: 2px solid #2B2B2B;
                background: #2B2B2B;
                selection-background-color: #2B2B2B;
                gridline-color: #2B2B2B;
            }

            QHeaderView::section {
                color: #A6A6A6;
                background: #2B2B2B;
                border: 0px solid #2B2B2B;
                border-bottom: 2px solid #555555;
                padding-bottom: 9px;
                padding-top: 6px;
            }

            QPlainTextEdit:focus {
                border-radius: 13px;
                color: #FFFFFF;
                background: #252525;
                border: 0px solid #252525;
            }

            QPlainTextEdit {
                color: #A6A6A6;
                background: #2B2B2B;
                border: 0px solid #2B2B2B;
            }

            QComboBox {
                color: #A6A6A6;
                background: #2B2B2B;
                border: 0px;
            }

            QComboBox::down-arrow {
                image: url(noimg);
                border-width: 0px;
                border: 0px;
            }

            QComboBox::drop-down {
                border: 0px;
            }

            QPushButton { background-color: #2B2B2B;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #555555;
                border-radius: 12px;
            }
            QPushButton:pressed {
                background-color: #282828;
                border-radius: 12px;
            }
        """)

        # QTableView {
        #     color: #A6A6A6;
        #     background: #282828;
        #     selection-background-color: #444444;
        #     gridline-color: #282828;
        # }
        #
        # QHeaderView::section {
        #     color: #A6A6A6;
        #     background: #282828;
        #     border: 2px solid #282828;
        #     border-right: 2px solid #555555;
        #     padding-bottom: 10px;
        # }
        #
        # QHeaderView::section:horizontal:last {
        #     color: #A6A6A6;
        #     background: #282828;
        #     border: 2px solid #282828;
        #     padding-bottom: 10px;
        # }

        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.references_table.setStyleSheet("""
            QTableView {
                color: #A6A6A6;
                border: 2px solid #2B2B2B;
                background: #2B2B2B;
                selection-background-color: #444444;
                gridline-color: #2B2B2B;
            }

            QHeaderView::section {
                color: #A6A6A6;
                background: #2B2B2B;
                border: 0px solid #2B2B2B;
                border-bottom: 2px solid #555555;
                padding-bottom: 9px;
                padding-top: 6px;
            }
        """)

        self.setStyleSheetButton(self.ui.settingsProjectButton)
        self.setStyleSheetButton(self.ui.backUpButton)
        self.setStyleSheetButton(self.ui.snapshotButton)
        self.setStyleSheetButton(self.ui.currentSnapshotButton)
        self.setStyleSheetButton(self.ui.importButton)
        self.setStyleSheetButton(self.ui.currentImportButton)
        self.setStyleSheetButton(self.ui.settingsSectorButton)
        self.setStyleSheetButton(self.ui.namespace_button)
        self.setStyleSheetButton(self.ui.reload_ref_button)
        self.setStyleSheetButton(self.ui.merge_ref_button)
        self.setStyleSheetButton(self.ui.replace_ref_button)
        self.setStyleSheetButton(self.ui.delete_ref_button)
        self.setStyleSheetSavingButton(self.ui.saveVersionButton)
        self.setStyleSheetSavingButton(self.ui.saveMasterButton)

    def setStyleSheetButton(self, button):
        """Change the look of Icon Push Buttons."""
        button.setMinimumSize(QtCore.QSize(25, 25))
        button.setStyleSheet("""
            QPushButton { background-color: #555555;
            border: 0px;
            border-radius: 12px;
            }
            QPushButton:hover {
            background-color: #666666;
            border: 0px;
            border-radius: 12px;
            }
            QPushButton:pressed {
            background-color: #282828;
            border-radius: 12px;
            }
        """)

    def setStyleSheetSavingButton(self, button):
        """Change the look of Icon Push Buttons."""
        button.setMinimumSize(QtCore.QSize(25, 25))
        button.setStyleSheet("""
            QPushButton { background-color: #555555;
            border: 0px;
            min-height: 40px;
            }
            QPushButton:hover {
            background-color: """ + self.custom_color + """ ;
            border: 0px;
            }
            QPushButton:pressed {
            background-color: #282828;
            }
        """)

    def setStyleSheetLargeButton(self, button):
        """Change the look of Icon Push Buttons."""
        button.setMinimumSize(QtCore.QSize(25, 25))
        button.setStyleSheet("""
            QPushButton { background-color: #555555;
            border: 0px;
            min-height: 40px;
            }
            QPushButton:hover {
            background-color: #666666;
            border: 0px;
            }
            QPushButton:pressed {
            background-color: #282828;
            }
        """)

    def changeColor(self):
        """Open a QColorDialog and change UI Color."""
        if not self.full_project_path:
            mc.warning('No Half Pipe project set!')
            return
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
                rgb = (color.red(), color.green(), color.blue())
                self.custom_color = str("rgb(%d,%d,%d)" % rgb)

                # Load the json file.
                project_settings_path = os.path.normpath(os.path.join(
                    self.full_project_path,
                    PROJECT_SETTINGS_FILE
                ))
                data = []
                if os.path.exists(project_settings_path):
                    with open(project_settings_path, 'r') as settings_file:
                        data = json.loads(settings_file.read())

                data['color'] = self.custom_color

                with open(project_settings_path, 'w') as settings_file:
                    settings_file.write(json.dumps(data))
                self.styleSheetMethods()
                self.loadBanner()

    def resetColor(self):
        """Change the color of the pipe back to its default."""
        if not self.full_project_path:
            return
        self.custom_color = DEFAULT_COLOR

        # Load the json file.
        project_settings_path = os.path.normpath(os.path.join(
            self.full_project_path,
            PROJECT_SETTINGS_FILE
        ))
        data = []
        if os.path.exists(project_settings_path):
            with open(project_settings_path, 'r') as settings_file:
                data = json.loads(settings_file.read())

        data['color'] = self.custom_color

        with open(project_settings_path, 'w') as settings_file:
            settings_file.write(json.dumps(data))
        self.styleSheetMethods()
        self.loadBanner()

    def viewHelp(self):
        """Open the help.pdf."""
        pdf_path = os.path.join(
            os.path.abspath(os.path.join(__file__, "../..")),
            r'help.pdf'
        )
        if os.path.exists(pdf_path):
            subprocess.Popen([pdf_path], shell=True)
        else:
            mc.warning('Could not find ../halfpipe/help.pdf')

    def mapEvents(self):
        """Connect methods to UI."""
        self.ui.projectImage.mousePressEvent = self.open_directory

        self.ui.sequenceList.itemSelectionChanged.connect(self.listScenes)
        self.ui.sectorComboBox.currentIndexChanged.connect(
            self.updateSectorLabel
        )
        self.ui.settingsSectorButton.clicked.connect(self.openSectorSettings)

        self.ui.sequencePlusButton.clicked.connect(partial(
            self.addItem,
            listDest=self.ui.sequenceList
        ))
        self.ui.sequenceMinusButton.clicked.connect(partial(
            self.removeItem,
            listDest=self.ui.sequenceList
        ))

        self.ui.scenePlusButton.clicked.connect(partial(
            self.addItem,
            listDest=self.ui.sceneList
        ))

        self.ui.sceneMinusButton.clicked.connect(partial(
            self.removeItem,
            listDest=self.ui.sceneList
        ))

        self.ui.settingsProjectButton.clicked.connect(self.setSettingsProject)
        self.ui.backUpButton.clicked.connect(self.openBackUpDialog)
        self.ui.sceneList.itemSelectionChanged.connect(
            self.updateToNewScenePath
        )

        self.ui.snapshotButton.clicked.connect(self.takeSnapshot)
        self.ui.currentSnapshotButton.clicked.connect(self.takeSnapshot)
        self.ui.importButton.clicked.connect(self.importImage)
        self.ui.currentImportButton.clicked.connect(self.importImage)

        self.ui.artistAnswerLabel01.currentIndexChanged.connect(
            self.updateBrowserSceneInfo
        )
        self.ui.commentAnswerLabel01.textChanged.connect(
            self.updateBrowserSceneInfo
        )

        # Connect current scene info
        self.ui.artistAnswerLabel02.currentIndexChanged.connect(
            self.updateCurrentSceneInfo
        )
        self.ui.commentAnswerLabel02.textChanged.connect(
            self.updateCurrentSceneInfo
        )

        self.ui.sceneList.itemDoubleClicked.connect(self.openScene)
        self.ui.ref_scene_button.clicked.connect(self.referenceScene)
        self.ui.import_scene_button.clicked.connect(self.importScene)

        # Export Alembic
        self.ui.expObjectButton.clicked.connect(self.openExportAbc)

        # Export Shaders
        self.ui.impAbcButton.clicked.connect(self.exportShaders)

        # Import or Ref Alembic
        self.ui.expAbcButton.clicked.connect(self.refOrImportAlembic)

        # Assemble Shaders
        self.ui.reButton.clicked.connect(self.assembleShaders)

        self.ui.saveVersionButton.clicked.connect(self.incrementalSave)
        self.ui.saveMasterButton.clicked.connect(self.openSaveMasterDialog)

        # self.ui.sceneHistoryTable.cellClicked.connect(self.tableClickedReturnPos)
        self.ui.sceneHistoryTable.cellDoubleClicked.connect(
            self.tableClickedOpen
        )
        self.ui.sceneHistoryTable.horizontalHeader(
        ).sectionDoubleClicked.connect(
            self.deleteAllVersions
        )

        self.ui.references_table.clicked.connect(self.referenceItemSelected)

        self.ui.namespace_button.clicked.connect(self.namespaceDialog)
        self.ui.reload_ref_button.clicked.connect(self.reloadReference)
        self.ui.merge_ref_button.clicked.connect(self.importOneReference)
        self.ui.replace_ref_button.clicked.connect(self.replaceReference)
        self.ui.delete_ref_button.clicked.connect(self.removeOneReference)

        self.timer.timeout.connect(self.updateReferenceTable)
        self.ui.tabWidget.tabBarClicked.connect(self.updateFromTab)

    def updateProject(self):
        """Update the PROD Path and reinitialize first methods."""
        if os.path.exists(self.path_settings_file):
            with open(self.path_settings_file, 'r') as settings_file:
                self.data = json.loads(settings_file.read())
        else:
            self.data = dict([
                ('last_project', ''),
            ])
            with open(self.path_settings_file, 'w') as settings_file:
                settings_file.write(json.dumps(self.data))

        if (
            not self.data or
            'last_project' not in self.data or
            not self.data['last_project'] or
            not os.path.exists(self.data['last_project'])
        ):
            self.username = 'Undefined'
            self.users_list = ['Undefined']
            self.custom_color = DEFAULT_COLOR
            self.project_fps = 'film'
            self.full_project_path = None

            self.ui.settingsSectorButton.setEnabled(False)
            self.ui.sequencePlusButton.setEnabled(False)
            self.ui.sequenceMinusButton.setEnabled(False)

        else:
            self.full_project_path = os.path.normpath(
                self.data['last_project']
            )
            self.project_path = os.path.normpath(
                os.path.join(self.full_project_path, '2_PROD')
            )
            self.ui.settingsSectorButton.setEnabled(True)
            self.ui.sequencePlusButton.setEnabled(True)
            self.ui.sequenceMinusButton.setEnabled(True)

        self.updateFromProjectSettings()
        self.styleSheetMethods()
        self.updateSectorCombo()
        self.updateSectorLabel()
        self.printLabels()
        self.set_images()
        self.loadBanner()
        self.load_image_scene()
        self.loadCurrentSceneInfo()
        self.set_workspace()
        self.updateToNewScenePath()
        self.listScenes()
        self.updateReferenceTable()
        self.fillComboBox()
        self.load_current_image_scene()

    # ####################################################################### #
    #                                 Global                                  #
    # ####################################################################### #
    def createFolder(self, folder):
        """Create a folder."""
        if not os.path.exists(folder):
            os.makedirs(folder)

    def createFoldersList(self, folder_list, root_folder):
        """Create a list of folders in a root folder."""
        for folder in folder_list:
            path = os.path.normpath(os.path.join(
                root_folder, folder
            ))
            self.createFolder(path)

    def create_project(self):
        """Create all folders needed to set the Maya workspace."""
        self.createFoldersList(
            self.workspace_folder_list.values(), self.full_project_path
        )

        input_folder_list = ['1_TEXTURES', '2_STOCKSHOTS', '3_OTHER']
        input_path = os.path.normpath(
            os.path.join(
                self.full_project_path, self.workspace_folder_list['input']
            )
        )
        self.createFoldersList(input_folder_list, input_path)

        output_folder_list = [
            '1_MAYA',
            '2_PLAYBLAST',
            '3_ANIMATIQUE',
            '4_COMP',
            '5_MASTER'
        ]
        output_path = os.path.normpath(
            os.path.join(
                self.full_project_path, self.workspace_folder_list['output']
            )
        )
        self.createFoldersList(output_folder_list, output_path)

        data_folder_list = [
            'AUTOSAVE',
            'SCRIPTS',
            'CACHE',
            'RENDER_DATA',
            'SHADERS'
        ]
        data_path = os.path.normpath(
            os.path.join(
                self.full_project_path, self.workspace_folder_list['data']
            )
        )
        self.createFoldersList(data_folder_list, data_path)

    def createMELworkspace(self, path=None):
        """Create the MEL file used by Maya to set the project."""
        if not self.full_project_path:
            return

        mel_workspace_text = """//Maya 2017 Project Definition"

            workspace -fr "fluidCache" "5_DATA/CACHE";
            workspace -fr "images" "6_OUTPUT/1_MAYA";
            workspace -fr "JT_ATF" "5_DATA";
            workspace -fr "offlineEdit" "5_DATA";
            workspace -fr "STEP_ATF Export" "5_DATA";
            workspace -fr "furShadowMap" "5_DATA/RENDER_DATA";
            workspace -fr "INVENTOR_ATF Export" "5_DATA";
            workspace -fr "scripts" "5_DATA/SCRIPTS";
            workspace -fr "STL_ATF" "5_DATA";
            workspace -fr "DAE_FBX" "5_DATA";
            workspace -fr "shaders" "5_DATA/RENDER_DATA";
            workspace -fr "NX_ATF" "5_DATA";
            workspace -fr "furFiles" "5_DATA/RENDER_DATA";
            workspace -fr "CATIAV5_ATF Export" "5_DATA";
            workspace -fr "OBJ" "5_DATA";
            workspace -fr "alembicCache" "5_DATA/CACHE";
            workspace -fr "FBX export" "5_DATA";
            workspace -fr "furEqualMap" "5_DATA/RENDER_DATA";
            workspace -fr "BIF" "5_DATA";
            workspace -fr "DAE_FBX export" "5_DATA";
            workspace -fr "CATIAV5_ATF" "5_DATA";
            workspace -fr "SAT_ATF Export" "5_DATA";
            workspace -fr "movie" "6_OUTPUT/2_PLAYBLAST";
            workspace -fr "ASS Export" "5_DATA";
            workspace -fr "autoSave" "5_DATA/AUTOSAVE";
            workspace -fr "move" "5_DATA";
            workspace -fr "mayaAscii" "2_PROD";
            workspace -fr "NX_ATF Export" "5_DATA";
            workspace -fr "sound" "4_INPUT";
            workspace -fr "mayaBinary" "2_PROD";
            workspace -fr "timeEditor" "5_DATA";
            workspace -fr "JT_ATF Export" "5_DATA";
            workspace -fr "iprImages" "5_DATA/RENDER_DATA";
            workspace -fr "FBX" "5_DATA";
            workspace -fr "renderData" "5_DATA/RENDER_DATA";
            workspace -fr "CATIAV4_ATF" "5_DATA";
            workspace -fr "fileCache" "5_DATA/CACHE";
            workspace -fr "eps" "5_DATA";
            workspace -fr "STL_ATF Export" "5_DATA";
            workspace -fr "3dPaintTextures" "4_INPUT/1_TEXTURES";
            workspace -fr "translatorData" "5_DATA";
            workspace -fr "mel" "5_DATA/SCRIPTS";
            workspace -fr "particles" "5_DATA/CACHE";
            workspace -fr "scene" "2_PROD";
            workspace -fr "SAT_ATF" "5_DATA";
            workspace -fr "PROE_ATF" "5_DATA";
            workspace -fr "WIRE_ATF Export" "5_DATA";
            workspace -fr "sourceImages" "4_INPUT/1_TEXTURES";
            workspace -fr "furImages" "5_DATA/RENDER_DATA";
            workspace -fr "clips" "6_OUTPUT/PLAYBLAST";
            workspace -fr "INVENTOR_ATF" "5_DATA";
            workspace -fr "STEP_ATF" "5_DATA";
            workspace -fr "depth" "5_DATA/RENDER_DATA";
            workspace -fr "IGES_ATF Export" "5_DATA";
            workspace -fr "sceneAssembly" "5_DATA";
            workspace -fr "IGES_ATF" "5_DATA";
            workspace -fr "teClipExports" "6_OUTPUT/PLAYBLAST";
            workspace -fr "ASS" "5_DATA/CACHE";
            workspace -fr "audio" "5_DATA";
            workspace -fr "bifrostCache" "5_DATA/CACHE";
            workspace -fr "Alembic" "5_DATA";
            workspace -fr "illustrator" "5_DATA";
            workspace -fr "diskCache" "5_DATA";
            workspace -fr "WIRE_ATF" "5_DATA";
            workspace -fr "templates" "5_DATA";
            workspace -fr "OBJexport" "5_DATA";
            workspace -fr "furAttrMap" "5_DATA/RENDER_DATA";"""

        project_path = self.full_project_path
        if path is not None:
            project_path = path
        workspace_mel_file = os.path.join(
            project_path, "workspace.mel"
        )

        if self.checkProjectCorrect() and not os.path.exists(
            workspace_mel_file
        ):
                with open(workspace_mel_file, "w") as myfile:
                    myfile.write(mel_workspace_text)
                myfile.close()

    def checkProjectCorrect(self):
        """Check if the current Project has all mandatory folders."""
        for folder in self.workspace_folder_list.values():
            category_path = os.path.normpath(
                os.path.join(self.full_project_path, folder)
            )
            if not os.path.exists(category_path):
                given_directory = False
            else:
                given_directory = True
        return given_directory

    def set_workspace(self):
        """Set the workspace."""
        if not self.full_project_path:
            return
        workspace_mel_file = os.path.join(
            self.full_project_path, "workspace.mel"
        )

        if os.path.exists(workspace_mel_file):
            mc.workspace(self.full_project_path, openWorkspace=True)
        else:
            mc.warning('Could not find path workspace.mel at {0}'.format(
                self.full_project_path)
            )
            return

    def writeFirstTimeSettings(
        self, project_name, artists_list, user_fps, user_name
    ):
        """Write Settings File when creating a half pipe project."""
        self.project_settings_path = os.path.normpath(
            os.path.join(
                self.full_project_path,
                PROJECT_SETTINGS_FILE)
            )

        fps = user_fps
        users_list = artists_list
        users_list.append('Undefined')

        data = {}
        data['users_list'] = users_list
        data['fps'] = fps
        data['color'] = "No Color Set"

        with open(self.project_settings_path, 'w') as settings_file:
            settings_file.write(json.dumps(data))

        self.path_settings_file = os.path.join(
            HALFPIPE_PATH_FILE, SETTINGS_FILE
        )
        user_data = []
        with open(self.path_settings_file, 'r') as settings_file:
            user_data = json.loads(settings_file.read())

        user_data['last_project'] = self.full_project_path
        user_data[project_name] = user_name

        os.remove(self.path_settings_file)
        with open(self.path_settings_file, 'w') as settings_file:
            settings_file.write(json.dumps(user_data))

    def updateSectorCombo(self):
        """Update the list in the Sector Combo Box."""
        self.ui.sectorComboBox.clear()
        if self.project_path is None:
            return
        for folder in os.listdir(self.project_path):
            self.ui.sectorComboBox.addItem(folder)

    def updateSectorLabel(self):
        """Refresh UI and lists when the category is changed."""
        if self.project_path is None:
            return
        self.sequence_label = self.ui.sectorComboBox.currentText()
        self.ui.sequenceLabel.setText(self.sequence_label)
        self.current_sector_path = os.path.normpath(
            os.path.join(self.project_path, self.sequence_label)
        )
        if not self.sequence_label:
            return
        self.listSequences()

    def takeSnapshot(self):
        """Take a snapshot of the current viewport."""
        image_format = mc.getAttr('defaultRenderGlobals.imageFormat')
        mc.setAttr('defaultRenderGlobals.imageFormat', 32)
        current_time = mc.currentTime(query=True)

        # Tab index = 0 -> project tab
        # Tab index = 1 -> current scene tab
        tab_index = self.ui.tabWidget.currentIndex()
        if tab_index == 0:
            data_path = os.path.normpath(os.path.join(
                self.current_scene_path,
                self.data_folder_name
            ))
        if tab_index == 1:
            current_scene_folder = os.path.split(
                mc.file(query=True, sceneName=True)
            )[0]
            if not os.path.exists(current_scene_folder):
                return
            if os.path.split(
                current_scene_folder
            )[-1] == self.version_folder_name:
                current_scene_folder = os.path.split(current_scene_folder)[0]
            data_path = os.path.normpath(os.path.join(
                current_scene_folder,
                self.data_folder_name
            ))

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        snapshot_path = os.path.normpath(os.path.join(
            data_path,
            self.snapshot_file_name
        ))

        # print 'SNAPSHOT PATH', snapshot_path
        # print 'EXISTS', os.path.exists(snapshot_path)

        if os.path.exists(snapshot_path) and os.path.isfile(snapshot_path):
            os.remove(snapshot_path)

        mc.playblast(
            orn=False, framePadding=0, v=False, startTime=current_time,
            endTime=current_time, format='image', compression='png',
            percent=100, w=200, h=113, f=snapshot_path, quality=100
        )
        os.rename(
            snapshot_path + '.' + str(
                int(current_time)
            ) + '.png', snapshot_path
        )
        mc.setAttr('defaultRenderGlobals.imageFormat', image_format)
        self.scene_image_path = snapshot_path

        if tab_index == 0:
            self.load_image_scene()
        if tab_index == 1:
            self.load_current_image_scene()

    def importImage(self):
        """Change the image scene to an imported image."""
        # Tab index = 0 -> project tab
        # Tab index = 1 -> current scene tab
        tab_index = self.ui.tabWidget.currentIndex()
        if tab_index == 0:
            data_path = os.path.normpath(os.path.join(
                self.current_scene_path,
                self.data_folder_name
            ))
        if tab_index == 1:
            current_scene_folder = os.path.split(
                mc.file(query=True, sceneName=True)
            )[0]
            if not os.path.exists(current_scene_folder):
                return
            if os.path.split(
                current_scene_folder
            )[-1] == self.version_folder_name:
                current_scene_folder = os.path.split(current_scene_folder)[0]
            data_path = os.path.normpath(os.path.join(
                current_scene_folder,
                self.data_folder_name
            ))

        snapshot_path = os.path.normpath(os.path.join(
            data_path,
            self.snapshot_file_name
        ))
        old_image_path = self.scene_image_path
        selected_file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select an image",
            "C:/",
            "Images (*bmp *.jpg *.jpeg *.png *tga *.tif)"
        )

        if selected_file[0] == ('') and old_image_path is not None:
            self.scene_image_path = old_image_path
        elif selected_file[0] == ('') and old_image_path is None:
            self.scene_image_path = None
        else:
            snapshot_name = os.path.splitext(self.snapshot_file_name)[0]
            for filename in os.listdir(data_path):
                if snapshot_name in filename:
                    os.remove(os.path.join(data_path, filename))

            extension = os.path.splitext(selected_file[0])[-1]
            old_file_name = os.path.split(selected_file[0])[-1]
            file_path = os.path.normpath(
                os.path.join(data_path, old_file_name)
            )
            snapshot_path = ''.join([
                os.path.splitext(snapshot_path)[0],
                extension
            ])
            if file_path == snapshot_path:
                os.remove(file_path)
                shutil.copyfile(selected_file[0], snapshot_path)
            else:
                shutil.copyfile(selected_file[0], snapshot_path)

            self.scene_image_path = snapshot_path

        if tab_index == 0:
            self.load_image_scene()
        if tab_index == 1:
            self.load_current_image_scene()

    def importBanner(self):
        """Change the image scene to an imported image."""
        if not self.full_project_path:
            mc.warning('No Half Pipe project set!')
            return

        project_data_path = os.path.normpath(os.path.join(
            self.full_project_path,
            '5_DATA'
        ))
        banners = []

        # Look for any custom banner file.
        for filepath in glob.glob(os.path.join(project_data_path, 'banner*')):
            banners.append(filepath)

        # Change the banner path.
        if banners != []:
            old_image_path = banners[0]
        else:
            old_image_path = None

        # Pick an image.
        selected_file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select an image",
            "C:/",
            "Images (*bmp *.jpg *.jpeg *.png *tga *.tif)"
        )

        if selected_file[0] == ('') and old_image_path is not None:
            self.banner_path = old_image_path
        elif selected_file[0] == ('') and old_image_path is None:
            self.banner_path = r'icons\banner_purple_t.png'
        else:
            # Replace image file by removing old ones.
            for filepath in glob.glob(os.path.join(
                project_data_path, 'banner*'
            )):
                os.remove(os.path.join(filepath))

            extension = os.path.splitext(selected_file[0])[-1]
            old_file_name = os.path.split(selected_file[0])[-1]
            file_path = os.path.normpath(
                os.path.join(project_data_path, old_file_name)
            )
            banner_path = os.path.normpath(os.path.join(
                project_data_path,
                ('banner' + extension)
            ))
            if file_path == banner_path:
                if os.path.exists(file_path):
                    os.remove(file_path)
                shutil.copyfile(selected_file[0], banner_path)
            else:
                shutil.copyfile(selected_file[0], banner_path)

            self.banner_path = banner_path
            self.loadBanner()

    def resetBanner(self):
        """Delete old file and replace banner in UI."""
        if not self.full_project_path:
            return
        project_data_path = os.path.normpath(os.path.join(
            self.full_project_path,
            '5_DATA'
        ))
        banners = []

        # Look for any custom banner file.
        for filepath in glob.glob(os.path.join(project_data_path, 'banner*')):
            banners.append(filepath)

        # Change the banner path.
        if banners != []:
            for banner in banners:
                os.remove(os.path.normpath(os.path.join(
                    project_data_path,
                    banner
                )))
        self.loadBanner()

    def loadBanner(self):
        """Load the Banner."""
        if not self.full_project_path:
            self.banner_path = r'icons\banner_purple_t.png'
            self.load_image(self.ui.projectImage, self.banner_path)
            return

        project_data_path = os.path.normpath(os.path.join(
            self.full_project_path,
            '5_DATA'
        ))
        banners = []

        # Look for any custom banner file.
        for filepath in glob.glob(os.path.join(project_data_path, 'banner*')):
            banners.append(filepath)

        # Change the banner path.
        if banners != []:
            self.banner_path = banners[0]
        else:
            # Look for a custom color.
            if self.custom_color == DEFAULT_COLOR:
                self.banner_path = r'icons\banner_purple_t.png'
            else:
                self.banner_path = r'icons\banner_white_t.png'

        # Load Image
        self.load_image(self.ui.projectImage, self.banner_path)

    def load_image(self, labelToChange, image_path):
        """Replace a label by an image."""
        full_image_path = os.path.join(
            os.path.split(__file__)[0],
            "..",
            image_path
        )
        pixmap = QtGui.QPixmap(full_image_path)
        labelToChange.setPixmap(pixmap)

    def load_image_by_expanding(self, labelToChange, image_path):
        """Replace a label by an image."""
        full_image_path = os.path.join(
            os.path.split(__file__)[0],
            "..",
            image_path
        )
        pixmap = QtGui.QPixmap(full_image_path)
        w = labelToChange.width()
        h = labelToChange.height()
        labelToChange.setPixmap(pixmap.scaled(
            w, h, QtCore.Qt.KeepAspectRatioByExpanding)
        )

    def load_image_scene(self):
        """Load the image scene."""
        if self.scene_image_path is None:
            self.load_image_by_expanding(
                self.ui.sceneImage, r'icons\default_filled_img.png'
            )

        else:
            self.load_image_by_expanding(
                self.ui.sceneImage, self.scene_image_path
            )

    def load_current_image_scene(self):
        """Load the image scene of the Current Tab."""
        current_scene_path = os.path.split(
            mc.file(query=True, sceneName=True)
        )[0]
        current_scene_data_path = os.path.normpath(os.path.join(
            current_scene_path,
            self.data_folder_name
        ))

        if not os.path.exists(current_scene_data_path):
            current_scene_data_path = os.path.normpath(os.path.join(
                current_scene_path.rsplit('_VERSIONS', 1)[0],
                self.data_folder_name
            ))

        if os.path.exists(current_scene_data_path):
            for file in os.listdir(current_scene_data_path):
                if fnmatch.fnmatch(file, 'snapshot*'):
                    self.snapshot_file_name = file

        self.scene_image_path = os.path.normpath(os.path.join(
            current_scene_data_path,
            self.snapshot_file_name
        ))
        real = os.path.exists(self.scene_image_path)

        if self.scene_image_path is None or not real:
            self.load_image_by_expanding(
                self.ui.currentSceneImage, r'icons\default_filled_img.png'
            )
        else:
            self.load_image_by_expanding(
                self.ui.currentSceneImage, self.scene_image_path
            )

    def set_images(self):
        """Set all images in the UI."""
        load_icon(self.ui.expObjectButton, r'icons\export.png')
        self.ui.expObjectButton.setText(' Export Alembic')
        load_icon(self.ui.expAbcButton, r'icons\import.png')
        self.ui.expAbcButton.setText(' Import or Ref Alembic')
        load_icon(self.ui.impAbcButton, r'icons\export.png')
        self.ui.impAbcButton.setText(' Export Shaders')
        load_icon(self.ui.reButton, r'icons\import.png')
        self.ui.reButton.setText(' Import Shaders')

        load_icon(self.ui.saveVersionButton, r'icons\save.png')
        load_icon(self.ui.saveMasterButton, r'icons\saveMaster.png')
        self.ui.saveVersionButton.setText(' SAVE VERSION')
        self.ui.saveMasterButton.setText(' SAVE MASTER')

        load_icon(self.ui.settingsProjectButton, r'icons\settings.png')
        load_icon(self.ui.backUpButton, r'icons\backup.png')
        load_icon(self.ui.settingsSectorButton, r'icons\settings.png')
        load_icon(self.ui.sequencePlusButton, r'icons\plus.png')
        self.ui.sequencePlusButton.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.scenePlusButton, r'icons\plus.png')
        self.ui.scenePlusButton.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.sequenceMinusButton, r'icons\minus.png')
        self.ui.sequenceMinusButton.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.sceneMinusButton, r'icons\minus.png')
        self.ui.sceneMinusButton.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.snapshotButton, r'icons\snapshot.png')
        load_icon(self.ui.currentSnapshotButton, r'icons\snapshot.png')
        load_icon(self.ui.importButton, r'icons\import.png')
        load_icon(self.ui.currentImportButton, r'icons\import.png')

    def projectSettings(self):
        """Open the Project Settings Dialog."""
        if not self.full_project_path:
            mc.warning('No Half Pipe project set!')
            return
        current_workspace = os.path.normpath(mc.workspace(fullName=True))
        project_name = os.path.split(self.full_project_path)[-1]
        if (
            self.full_project_path is None or
            not os.path.exists(self.full_project_path) or
            current_workspace != self.full_project_path
        ):
            mc.warning('Load a Half Pipe Project first.')
            return

        dialog = ProjectSettings(self, project_name)
        exec_output = dialog.exec_()

        if exec_output == 0:
            return

        # Change the FPS
        self.project_fps = dialog.string_command_fps
        mc.currentUnit(time=self.project_fps)

        # Change the Users Settings
        self.users_list = sorted(dialog.users_list)
        self.fillComboBox()

        self.project_settings_path = os.path.normpath(
            os.path.join(self.full_project_path, PROJECT_SETTINGS_FILE)
        )

        data = {}
        data['color'] = self.custom_color
        data['users_list'] = self.users_list
        data['fps'] = self.project_fps

        with open(self.project_settings_path, 'w') as settings_file:
            settings_file.write(json.dumps(data))

        # Change the Username
        self.path_settings_file = os.path.join(
            HALFPIPE_PATH_FILE, SETTINGS_FILE
        )

        user_data = []
        with open(self.path_settings_file, 'r') as settings_file:
            user_data = json.loads(settings_file.read())

        user_data['last_project'] = self.full_project_path
        user_data[project_name] = dialog.username

        os.remove(self.path_settings_file)
        with open(self.path_settings_file, 'w') as settings_file:
            settings_file.write(json.dumps(user_data))

        self.updateProject()
        # self.updateFromProjectSettings()

    def prefillOptions(self):
        """Open the Pre Fill Options Dialog."""
        dialog = Prefill(self.full_project_path, self)
        return_value = dialog.exec_()
        if return_value:
            self.prefix_dict = dialog.prefix_dict
            # print "PREFIX DICT", self.prefix_dict
            # Load the json file.
            project_settings_path = os.path.normpath(os.path.join(
                self.full_project_path,
                PROJECT_SETTINGS_FILE
            ))

            # Write prefix
            data = []
            if os.path.exists(project_settings_path):
                with open(project_settings_path, 'r') as settings_file:
                    data = json.loads(settings_file.read())

            data['prefix'] = self.prefix_dict

            with open(project_settings_path, 'w') as settings_file:
                settings_file.write(json.dumps(data))

    def delete_confirmation_dialog(self, question):
        """Define the UI for a confirmation dialog box."""
        message_box = QtWidgets.QMessageBox(self)
        message_box.setText(question)
        message_box.setInformativeText(
            "All contents and references will be lost."
        )
        message_box.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        message_box.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        message_box_return_value = message_box.exec_()
        return message_box_return_value == QtWidgets.QMessageBox.Ok

    def fillComboBox(self):
        """Add artist names to the artist comboboxes."""
        self.ui.artistAnswerLabel01.clear()
        self.ui.artistAnswerLabel02.clear()
        for name in self.users_list:
            self.ui.artistAnswerLabel01.addItem(name)
            self.ui.artistAnswerLabel02.addItem(name)

    def save_scene_info(
        self,
        artist_combox,
        commentEdit,
        version_number=None,
        saving=True,
        currentScene=None
    ):
        """Write the information on disk."""
        scene = None
        if currentScene is None:
            scene = self.current_scene_path
        else:
            scene = currentScene

        scene = scene.strip()
        if not scene:
            return

        scene_name = os.path.split(scene)[-1]
        # The master scene is the scene with version 000
        scene_version = '000'
        if version_number is not None:
            scene_version = str(version_number).zfill(3)
        scene_artist = artist_combox.currentText()
        save_time = datetime.datetime.fromtimestamp(
            time.time()
        )
        date = save_time.strftime('%d %b %Y %H:%M')
        comment = commentEdit.toPlainText()

        scene_data = dict([
            ('Name', scene_name),
            ('Version', scene_version),
            ('Artist', scene_artist),
            ('Date', date),
            ('Comment', comment)
        ])

        output_path = os.path.normpath(os.path.join(
            scene, self.data_folder_name
        ))

        if (
            not self.full_project_path or
            not (
                os.path.normpath(self.full_project_path) in
                os.path.normpath(mc.file(q=True, sceneName=True))
            )
        ):
            return

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        scene_info_file = os.path.normpath(os.path.join(
            output_path,
            self.data_file_name
        ))

        data = []
        if os.path.exists(scene_info_file):
            with open(scene_info_file, 'r') as settings_file:
                for line in settings_file.readlines():
                    data.append(json.loads(line.strip()))

        versions = set([scene_info['Version'] for scene_info in data])
        found = scene_version in versions
        # If version is not found and we're not saving, skip all modifications
        # to the scene info data (e.g modifying when master data with unsaved
        # scene)
        if not found and not saving:
            return
        # If version is not found but we're saving, just append the current
        # data to the list and save it
        elif not found and saving:
            data.append(scene_data)
        # Otherwise modify the existing data
        else:
            for index in range(len(data)):
                if data[index]['Version'] == scene_version:
                    data[index] = scene_data
                    break

        with open(scene_info_file, 'w') as settings_file:
            for scene_info in data:
                settings_file.write(json.dumps(scene_info) + '\n')

    def update_scene_info(
        self,
        scene_name,
        version_label,
        artist_label,
        date_label,
        comment_label,
        path=None,
        scene_version='000',
        scene_name_label=None
    ):
        """Update the scene information labels."""
        self.scene_image_path = None
        if scene_name_label is not None:
            scene_name_label.setText('')

        # Data file path of the selected scene.
        scene_info_file = None
        if self.current_scene_path and path is None:
            scene_info_file = os.path.normpath(os.path.join(
                self.current_scene_path,
                self.data_folder_name,
                self.data_file_name
            ))
        elif path == 'Not Open':
            scene_info_file = None
        elif path is not None and os.path.exists(path):
            folders = os.path.normpath(path).split(os.sep)
            if self.version_folder_name in folders:
                index = folders.index(self.version_folder_name)
                path = os.sep.join(folders[:index])
            else:
                path = os.sep.join(folders[:-1])
            scene_info_file = os.path.normpath(os.path.join(
                path,
                self.data_folder_name,
                self.data_file_name
            ))

        data = []
        current_data = []
        # print 'scene_info_file', scene_info_file
        # When the scene information file doesn't exist, return nothing.
        if scene_info_file is None or not os.path.exists(scene_info_file):
            version_label.setText('')
            self.ui.artistAnswerLabel01.setCurrentText('Undefined')
            self.ui.artistAnswerLabel02.setCurrentText(self.username)
            date_label.setText('')
            comment_label.setPlainText('')
            self.scene_image_path = None
            self.load_image_scene()
            return

        # Now that we're sure the file exists, let's load it.
        with open(scene_info_file, 'r') as settings_file:
                for line in settings_file.readlines():
                    data.append(dict(json.loads(line.strip())))

        # Find the latest version
        versions = []
        for item in data:
            versions.append(item['Version'])

        # Extract the dictionnary of the wanted scene.
        for item in data:
            if scene_name == item['Name']:
                # Check for the Master Version (000)
                # or the given one by the programmer.
                if int(scene_version) == int(item['Version']):
                    if item not in current_data:
                        current_data.append(item)
        # If no Master scene or version doesn't exists, use last version.
        if current_data == []:
            for item in data:
                last_scene_version = sorted(versions)[-1]
                if int(last_scene_version) == int(item['Version']):
                    if item not in current_data:
                        current_data.append(item)

        if len(current_data) > 1:
            raise ValueError('Too many values in current_data')
        elif len(current_data) == 0:
            raise ValueError('No current_data found')
        current_data = current_data[0]

        # Current Name Label
        if scene_name_label is not None:
            scene_name_label.setText(current_data['Name'])

        # Version Label
        if 'Version' not in current_data or not current_data['Version']:
            version_label.setText('')
        elif current_data['Version'] == '000':
            version_label.setText('MASTER')
        else:
            version_label.setText(current_data['Version'])

        # Artist Label
        all_items = [
            artist_label.itemText(i) for i in range(artist_label.count())
        ]
        if current_data['Artist'] in all_items:
            artist_label.setCurrentText(current_data['Artist'])
        else:
            artist_label.setCurrentText('Undefined')

        # Date Label
        date_label.setText(current_data['Date'])

        # Comment Label
        if not comment_label.hasFocus():
            comment_label.setPlainText(current_data['Comment'])

        # Scene Image
        folder = os.path.split(scene_info_file)[0]
        # if path:
        #     folder = os.path.normpath(os.path.join(
        #         path,
        #         self.data_folder_name
        #     ))
        # else:
        #     self.scene_image_path = None
        #     self.load_image_scene()
        #     return

        snapshot_name = os.path.splitext(self.snapshot_file_name)[0]
        snapshot = [
            filename
            for filename in os.listdir(folder)
            if snapshot_name in filename
        ]
        if snapshot:
            self.scene_image_path = os.path.normpath(os.path.join(
                folder, snapshot[0]
            ))
        else:
            self.scene_image_path = None

        self.load_image_scene()

    def updateBrowserSceneInfo(self):
        """Save info changes for the selected scene."""
        # Find the latest version
        if self.current_scene_path is None:
            return
        version_path = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.version_folder_name
        ))

        # Check if there's a Master scene.
        master_file = [filename for filename in os.listdir(
            self.current_scene_path
        ) if os.path.isfile(os.path.join(self.current_scene_path, filename))]
        last_version = '000'
        if master_file == []:
            if os.path.exists(version_path):
                version_files = os.listdir(version_path)
                if version_files != []:
                    last_version = (
                        str(sorted(version_files)[-1]).rsplit('.', 1)[0]
                    )[-3:]
                else:
                    last_version = '000'
        else:
            last_version = '000'

        # Save information
        self.save_scene_info(
            self.ui.artistAnswerLabel01,
            self.ui.commentAnswerLabel01,
            version_number=last_version,
            saving=False,
        )

        # self.loadCurrentSceneInfo()
        self.updateHistoryTable()

    def updateCurrentSceneInfo(self):
        """Save info changes of the selected scene."""
        current_opened_scene = os.path.split(
            mc.file(query=True, sceneName=True)
        )[0]
        if current_opened_scene is None or current_opened_scene == '':
            return

        version_pattern = str(r'/' + self.version_folder_name)
        if version_pattern in current_opened_scene:
            current_opened_scene = os.path.split(current_opened_scene)[0]
        # scene_name = os.path.split(current_opened_scene)[-1]

        # Find the latest version
        version_path = os.path.normpath(os.path.join(
            current_opened_scene,
            self.version_folder_name
        ))

        # Check if there's a Master scene.
        if os.path.exists(current_opened_scene):
            master_file = [filename for filename in os.listdir(
                current_opened_scene
            ) if os.path.isfile(os.path.join(current_opened_scene, filename))]
        else:
            master_file = []

        last_version = '000'
        if master_file == []:
            if os.path.exists(version_path):
                version_files = os.listdir(version_path)
                if version_files != []:
                    last_version = (
                        str(sorted(version_files)[-1]).rsplit('.', 1)[0]
                    )[-3:]

        # Save information
        self.save_scene_info(
            self.ui.artistAnswerLabel02,
            self.ui.commentAnswerLabel02,
            version_number=last_version,
            saving=False,
            currentScene=current_opened_scene
        )

        self.updateHistoryTable()
        self.updateReferenceTable()

    # ####################################################################### #
    #                                 Header                                  #
    # ####################################################################### #

    def open_directory(self, event):
        """Open the Project directory in Windows."""
        if event.button() == QtCore.Qt.LeftButton:
            if os.path.exists(self.project_path):
                os.startfile(self.project_path)

    def printLabels(self):
        """Change the labels in function of the project settings."""
        if not self.project_path:
            return
        self.ui.projectPathLabel.setText(self.project_path)
        self.ui.projectName.setText(os.path.split(self.full_project_path)[-1])

    def openBackUpDialog(self):
        """Open the Back Up Dialog and return list of selected checkboxes."""
        if not self.full_project_path:
            mc.warning('No Half Pipe project to back up!')
            return
        self.back_up_selected_checkboxes = []
        dialog = BackUp(self)
        return_value = dialog.exec_()
        if return_value:
            for checkbox in dialog.checkboxes:
                if checkbox.isChecked():
                    self.back_up_selected_checkboxes.append(checkbox)
            self.copyFiles(dialog)

    def copyFiles(self, dialog):
        """Copy folders to back up in a given directory."""
        checkedList = self.back_up_selected_checkboxes
        # source_list_paths = None
        today = time.strftime("%Y_%m_%d")
        back_up_string = 'BACK_UP_'
        destination_path = os.path.join(
            dialog.back_up_destination_path, back_up_string + today
        )

        # Create the Back Up Folder
        if os.path.exists(destination_path):
            path = os.path.normpath(
                os.path.join(destination_path, '..', 'OLD')
            )
            if not os.path.exists(path):
                os.makedirs(path)
            folders = os.listdir(path)

            number = 1
            check_for_string = (
                back_up_string + today + '_' + str(number).zfill(3)
            )
            while check_for_string in folders:
                number += 1
                check_for_string = (
                    back_up_string + today + '_' + str(number).zfill(3)
                )
            new_destination_path = os.path.join(
                path, check_for_string
            )
            os.rename(destination_path, new_destination_path)

        os.makedirs(destination_path)

        # Extract the paths from the checkboxes.
        checkedList = [checkbox.text() for checkbox in checkedList]
        for name in checkedList:
            if name in 'PROD':
                continue
            for folder in glob.glob(
                os.path.join(self.full_project_path, '*_' + name)
            ):
                folder_name = os.path.split(folder)[-1]
                shutil.copytree(
                    folder,
                    os.path.join(destination_path, folder_name)
                )
                message = 'print "Successfully copied at {0}"'.format(
                    destination_path
                )
                maya.mel.eval(
                    message.replace('\\', '\\\\')
                )
            for folder in glob.glob(os.path.join(self.project_path, name)):
                folder_name = os.path.join(
                    os.path.split(self.project_path)[-1], name
                )
                shutil.copytree(
                    folder,
                    os.path.join(destination_path, folder_name)
                )
                message = 'print "Successfully copied at {0}"'.format(
                    destination_path
                )
                maya.mel.eval(
                    message.replace('\\', '\\\\')
                )

    # ####################################################################### #
    #                            Project Settings                             #
    # ####################################################################### #

    def setSettingsProject(self):
        """Open the Set Project Dialog Box."""
        self.users_list = []
        dialog = SetProjectDialog(self, self.custom_color)
        return_value = dialog.exec_()

        if not return_value:
            return

        # Tab index = 0 -> create project
        tab_index = dialog.ui.project_settings_tabWidget.currentIndex()
        self.full_project_path = dialog.new_project_path

        if tab_index == 0:
            self.project_fps = dialog.string_command_fps
            mc.currentUnit(time=self.project_fps)
            os.makedirs(self.full_project_path)
            self.project_path = os.path.normpath(
                os.path.join(self.full_project_path, '2_PROD')
            )
            self.hierarchy_folders = [value for value in self.default_folders]
            self.createHierarchy()
            self.create_project()
            self.createMELworkspace()
            self.writeFirstTimeSettings(
                dialog.new_project_name, dialog.users_list,
                dialog.string_command_fps, dialog.user_name
            )

        # Tab index = 1 -> set project
        if tab_index == 1:
            user_name = dialog.user_name
            project_name = os.path.split(self.full_project_path)[-1]
            self.path_settings_file = os.path.join(
                HALFPIPE_PATH_FILE, SETTINGS_FILE
            )
            user_data = []
            with open(self.path_settings_file, 'r') as settings_file:
                user_data = json.loads(settings_file.read())

            user_data['last_project'] = self.full_project_path
            user_data[project_name] = user_name

            os.remove(self.path_settings_file)
            with open(self.path_settings_file, 'w') as settings_file:
                settings_file.write(json.dumps(user_data))

        self.updateProject()
        # self.updateFromProjectSettings()
        self.styleSheetMethods()
        self.loadCurrentSceneInfo()

    def createHierarchy(self):
        """Create a default hierarchy."""
        self.ui.sectorComboBox.clear()

        self.createFoldersList(self.hierarchy_folders, self.project_path)

        folders = os.listdir(self.project_path)
        for folder in folders:
            if folder not in self.hierarchy_folders:
                shutil.rmtree(os.path.join(self.project_path, folder))
                continue
            self.ui.sectorComboBox.addItem(folder)

    # ####################################################################### #
    #                               Project Tab                               #
    # ####################################################################### #

    def listContents(self, path, ui_list):
        """Find folders at the given path and fill the given ui control."""
        self.ui.sceneList.setIconSize(QtCore.QSize(10, 10))
        if not os.path.exists(path):
            mc.warning('Could not find path at {0}'.format(path))
            return
        folders = sorted([
            filename
            for filename in os.listdir(path)
            if os.path.isdir(os.path.join(path, filename))
        ])

        for folder in folders:
            item = QtWidgets.QListWidgetItem(folder)
            whole_path = os.path.join(path, folder)
            files = [
                f
                for f in os.listdir(whole_path)
                if '.ma' in os.path.splitext(f)[-1]
            ]
            if files:
                item.setIcon(self.master_icon)
                item.setForeground(QtGui.QBrush(QtGui.QColor(130, 130, 130)))
            ui_list.addItem(item)

    def listSequences(self):
        """Find sequences on the project path and list them in the UI."""
        self.ui.sequenceList.clear()
        self.listContents(self.current_sector_path, self.ui.sequenceList)

    def openSectorSettings(self):
        """Open the Sector Settings Dialog."""
        count = self.ui.sectorComboBox.count()
        values = []
        for i in range(count):
            values.append(self.ui.sectorComboBox.itemText(i))
        dialog = SectorSettingsDialog(values, self.project_path, self)
        return_value = dialog.exec_()
        if return_value:
            self.hierarchy_folders = [label.text() for label in dialog.labels]
            self.createHierarchy()

    def listScenes(self):
        """Find scene folders on the project path and list them in the UI.

        This is done based on the selected sequence item.
        """
        self.ui.sceneList.clear()
        self.update_scene_info(
            None,
            self.ui.versionAnswerLabel01,
            self.ui.artistAnswerLabel01,
            self.ui.dateAnswerLabel01,
            self.ui.commentAnswerLabel01
        )

        selected_sequences = self.ui.sequenceList.selectedItems()
        self.update()
        if not selected_sequences:
            self.current_sequence_path = None
            self.ui.scenePlusButton.setEnabled(False)
            self.ui.sceneMinusButton.setEnabled(False)
            return

        self.ui.scenePlusButton.setEnabled(True)
        self.ui.sceneMinusButton.setEnabled(True)

        current_sequence = selected_sequences[0].text()
        self.current_sequence_path = os.path.normpath(os.path.join(
            self.current_sector_path, current_sequence
        ))
        self.listContents(self.current_sequence_path, self.ui.sceneList)

    def addItem(self, listDest):
        """Add an item in the list and its folder."""
        path = None
        add_scene = False
        current_dept = self.ui.sectorComboBox.currentText()
        if listDest is self.ui.sequenceList:
            path = self.current_sector_path
        elif listDest is self.ui.sceneList:
            path = self.current_sequence_path
            add_scene = True

        if path is None:
            return

        if add_scene:
            # print 'PREFIX DICT', self.prefix_dict
            # print current_dept
            # print self.prefix_dict[current_dept]
            if (
                not self.prefix_dict or
                self.prefix_dict == {} or
                current_dept not in self.prefix_dict or
                not self.prefix_dict[current_dept]
            ):
                departments = [
                    d for d in os.listdir(self.project_path)
                    if os.path.isdir(os.path.join(self.project_path, d))
                ]
                for dep in departments:
                    self.prefix_dict[dep] = ''

            name, valid = QtWidgets.QInputDialog.getText(
                self,
                'New item name',
                'Enter new item name',
                text=self.prefix_dict[current_dept]
            )
        else:
            name, valid = QtWidgets.QInputDialog.getText(
                self,
                'New item name',
                'Enter new item name',
            )

        if not valid:
            return
        name = formatText(name)

        if name is None or name == '':
            mc.warning('Invalid name.')
            return

        if name not in os.listdir(path):
            listDest.addItem(name)
            newPath = os.path.normpath(os.path.join(
                path, name)
            )
            if not os.path.exists(newPath):
                os.makedirs(newPath)
        else:
            print 'Name already used.'

        self.listScenes()
        self.update()

    def removeItem(self, listDest):
        """Remove an item from the list and its folder."""
        selected_items = listDest.selectedItems()
        current_name = os.path.normpath(mc.file(query=True, sceneName=True))
        current_path = os.path.normpath(
            os.path.split(mc.file(query=True, sceneName=True))[0]
        )
        if os.path.split(current_path)[-1] == '_VERSIONS':
            current_path = os.path.split(current_path)[0]
        if not selected_items:
            return

        path = None
        if listDest is self.ui.sequenceList:
            path = self.current_sequence_path
        elif listDest is self.ui.sceneList:
            path = self.current_scene_path

        if path is None:
            return
        if path == current_path:
            mc.warning("You cannot delete a scene you're working on.")
            return

        # print 'PATH', path
        contents = []
        list_dirs = os.walk(path)
        for root, dirs, files in list_dirs:
            for d in dirs:
                contents.append(os.path.normpath(os.path.join(root, d)))
            for f in files:
                contents.append(os.path.normpath(os.path.join(root, f)))

        data_path = os.path.normpath(os.path.join(path, '_DATA'))
        if not contents == []:
            if current_name in contents:
                mc.warning("You cannot delete a scene you're working on.")
                return
            if not contents == [data_path]:
                for item in selected_items:
                    question = (
                        "Are you sure you want to delete the {0} folder ?"
                    ).format(path)
                    message_box_return_value = \
                        self.delete_confirmation_dialog(question)
                    if not message_box_return_value:
                        return

        for item in selected_items:
            listDest.removeItemWidget(item)
            if os.path.exists(path):
                shutil.rmtree(path)

        if listDest is self.ui.sequenceList:
            self.listSequences()
        elif listDest is self.ui.sceneList:
            self.listScenes()

    def sceneMenu(self):
        """Create a menu for items in the scene table."""
        self.ui.sceneList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.sceneList.connect(
            self.ui.sceneList,
            QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
            self.listItemRightClicked
        )

    def listItemRightClicked(self, QPos):
        """Open the scene menu."""
        self.listMenu = QtWidgets.QMenu()
        self.listMenu.addAction("Rename Item", self.renameItem)
        self.listMenu.addAction("Open Last Autosave", self.openAutosave)
        parentPosition = self.ui.sceneList.mapToGlobal(
            QtCore.QPoint(0, 0)
        )
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def renameItem(self):
        """Rename a scene, its versions and update the scene info."""
        selected_parent = self.ui.sequenceList.currentRow()

        currentItemName = str(self.ui.sceneList.currentItem().text())
        scene_info_file = os.path.join(
            self.current_scene_path,
            self.data_folder_name,
            self.data_file_name
        )

        # Path if working on a Master Scene.
        option1 = os.path.split(os.path.normpath(
            mc.file(query=True, sceneName=True)
        ))[0]
        # Path working on a version.
        option2 = os.path.normpath(os.path.join(
            option1,
            self.version_folder_name
        ))

        if (
            self.current_scene_path == option1 or
            self.current_scene_path == option2
        ):
            mc.warning("You cannot rename a scene that you're working on.")
            return

        input_dialog, valid = QtWidgets.QInputDialog.getText(
            self,
            'Rename a scene',
            str('New name:\n\n' +
                'Warning: All references will be lost.\n'
                'Do not attempt to change the name if the\n'
                'scene is opened on another computer.'
                ),
            QtWidgets.QLineEdit.Normal,
            currentItemName,
        )
        if not valid:
            return
        return_scene_name = input_dialog

        if return_scene_name == currentItemName:
            return

        # Check if the files / directory are opened.
        if not os.access(self.current_scene_path, os.W_OK):
            mc.warning('Permission Denied. Close open folders.')
            return
        if not os.access(scene_info_file, os.W_OK):
            mc.warning('Permission Denied. Close open folders.')
            return

        # Change the scene name in the scene info file.
        scenes_data = []
        with open(scene_info_file, 'r') as settings_file:
                for line in settings_file.readlines():
                    scenes_data.append(json.loads(line.strip()))

        for dictionnary in scenes_data:
            dictionnary['Name'] = return_scene_name

        os.remove(scene_info_file)

        for dictionnary in scenes_data:
            with open(scene_info_file, 'a') as settings_file:
                settings_file.write(json.dumps(dictionnary) + '\n')

        # Rename files
        version_path = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.version_folder_name
        ))

        if os.path.exists(version_path):
            if any(isfile(join(
                version_path, i
            )) for i in listdir(version_path)):
                self.batchRename(
                    version_path,
                    r'*.ma',
                    currentItemName,
                    str(return_scene_name)
                )

        if os.path.exists(self.current_scene_path):
            if any(isfile(join(
                self.current_scene_path, i
            )) for i in listdir(self.current_scene_path)):
                self.batchRename(
                    self.current_scene_path,
                    r'*.ma',
                    currentItemName,
                    str(return_scene_name)
                )

                self.batchRename(
                    self.current_scene_path,
                    r'*.abc',
                    currentItemName,
                    str(return_scene_name)
                )

        # Rename directory
        new_scene_path = os.path.join(
            os.path.split(self.current_scene_path)[0],
            return_scene_name
        )
        os.rename(self.current_scene_path, new_scene_path)
        self.current_scene_path = new_scene_path

        self.updateProject()
        # self.updateFromTab(0)

        # Restore selection
        if self.ui.sequenceList.count() > 0:
            self.ui.sequenceList.setCurrentRow(selected_parent)
        if self.ui.sceneList.count() > 0:
            selected_scenes = self.ui.sceneList.findItems(
                return_scene_name, QtCore.Qt.MatchExactly
            )
            for scene in selected_scenes:
                self.ui.sceneList.setCurrentItem(scene)

    def batchRename(self, directory, pattern, old_name, new_name):
        """Rename files in a given directory."""
        for filepath in glob.iglob(os.path.join(directory, pattern)):
            title, ext = os.path.splitext(os.path.basename(filepath))
            newpath = os.path.normpath(os.path.join(
                directory,
                str(title.replace(old_name, new_name) + ext)
            ))
            os.rename(
                filepath,
                newpath
            )

    def openAutosave(self):
        """Open the latest autosave file."""
        currentItemName = str(self.ui.sceneList.currentItem().text())
        autosave_folder = os.path.normpath(os.path.join(
            self.full_project_path,
            '5_DATA',
            'AUTOSAVE'
        ))

        # Check if there is any autosave file for the current scene name.
        files_list = os.listdir(autosave_folder)
        matching_list = [
            filename for filename in files_list if
            currentItemName in filename
        ]
        if matching_list == []:
            mc.warning('Could not find any autosave file.')
            return

        # Find the latest modified file.
        matching_pattern = str(
            autosave_folder + str('\\') + currentItemName + r'*'
        )
        latest_autosave = max(
            glob.iglob(matching_pattern),
            key=os.path.getctime
        )

        # Open the file.
        # check if there are unsaved changes
        fileCheckState = mc.file(q=True, modified=True)

        # if there are, save them first ... then we can proceed
        if fileCheckState:
            save_dialog = QtWidgets.QMessageBox(self)
            save_dialog.setWindowTitle('Warning: Scene Not Saved')
            save_dialog.setText('Save changes to scene?')
            save_dialog.setStandardButtons(
                QtWidgets.QMessageBox.Save |
                QtWidgets.QMessageBox.Discard |
                QtWidgets.QMessageBox.Cancel
            )
            save_dialog.setDefaultButton(QtWidgets.QMessageBox.Save)
            return_value = save_dialog.exec_()

            # If Cancel is clicked:
            if return_value == QtWidgets.QMessageBox.Cancel:
                return
            # If Don't Save is clicked:
            elif return_value == QtWidgets.QMessageBox.Discard:
                mc.file(force=True, new=True)
            # If Save is clicked:
            else:
                mc.SaveScene()

        mc.file(latest_autosave, open=True, force=True)
        self.loadCurrentSceneInfo()

    def updateMasterPath(self):
        """Find for a scene folder a master path and its latest version."""
        versions_folder = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.version_folder_name
        ))

        if os.path.exists(versions_folder):
            files = (f for f in os.listdir(versions_folder) if os.path.isfile(
                os.path.join(versions_folder, f)
            ))
            last_version = sorted(files)
            if last_version != []:
                last_version = last_version[-1]
                self.last_version_path = os.path.normpath(os.path.join(
                    versions_folder,
                    last_version
                ))

        else:
            self.last_version_path = ''
        # print 'last_version_path', self.last_version_path
        if (self.last_version_path is None or not os.path.exists(
            self.last_version_path
        )):
            self.last_version_path = ''

        self.master_name = os.path.split(
            self.current_scene_path
        )[-1] + ".ma"
        self.master_path = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.master_name
        ))

        abc_name = os.path.split(
            self.current_scene_path
        )[-1] + ".abc"
        self.abc_path = os.path.normpath(
            os.path.join(self.current_scene_path, abc_name)
        )

    def openScene(self):
        """Open a scene."""
        self.updateMasterPath()
        # check if there are unsaved changes
        fileCheckState = mc.file(q=True, modified=True)

        # if there are, save them first ... then we can proceed
        if fileCheckState:
            save_dialog = QtWidgets.QMessageBox(self)
            save_dialog.setWindowTitle('Warning: Scene Not Saved')
            save_dialog.setText('Save changes to scene?')
            save_dialog.setStandardButtons(
                QtWidgets.QMessageBox.Save |
                QtWidgets.QMessageBox.Discard |
                QtWidgets.QMessageBox.Cancel
            )
            save_dialog.setDefaultButton(QtWidgets.QMessageBox.Save)
            return_value = save_dialog.exec_()

            # If Cancel is clicked:
            if return_value == QtWidgets.QMessageBox.Cancel:
                return
            # If Don't Save is clicked:
            elif return_value == QtWidgets.QMessageBox.Discard:
                mc.file(force=True, new=True)
            # If Save is clicked:
            else:
                mc.SaveScene()
        else:
            pass

        if (
            self.last_version_path is None
            or not os.path.exists(self.last_version_path)
        ):
            mc.warning('You need to save at least once...')
        else:
            mc.file(self.last_version_path, open=True, force=True)

        # if self.master_path is None or not os.path.exists(self.master_path):
        #     if self.last_version_path is None or not os.path.exists(
        #         self.last_version_path
        #     ):
        #         mc.warning('You need to save at least once...')
        #     else:
        #         mc.file(self.last_version_path, open=True, force=True)
        # else:
        #     mc.file(self.master_path, open=True, force=True)

        self.loadCurrentSceneInfo()

    def loadCurrentSceneInfo(self):
        """Load information from the opened scene in Maya."""
        self.load_current_image_scene()
        self.updateReferenceTable()
        current_opened_path = mc.file(query=True, sceneName=True)

        if not current_opened_path or current_opened_path == '':
            self.update_scene_info(
                '',
                self.ui.versionAnswerLabel02,
                self.ui.artistAnswerLabel02,
                self.ui.dateAnswerLabel02,
                self.ui.commentAnswerLabel02,
                path='Not Open',
                scene_version=None,
                scene_name_label=self.ui.nameAnswerLabel02
            )
            return

        scene_name = (os.path.split(current_opened_path)[-1]).split('.', 1)[0]
        version_number = scene_name[-3:]
        if version_number.isdigit():
            scene_name = scene_name[:-4]

        if version_number is None or not version_number.isdigit():
            version_number = '000'

        self.update_scene_info(
            scene_name,
            self.ui.versionAnswerLabel02,
            self.ui.artistAnswerLabel02,
            self.ui.dateAnswerLabel02,
            self.ui.commentAnswerLabel02,
            path=current_opened_path,
            scene_version=version_number,
            scene_name_label=self.ui.nameAnswerLabel02
        )

    def importScene(self):
        """Import a selected scene."""
        materials = None
        new_materials = None
        list_all_contents = mc.ls()
        default_nodes = mc.ls(defaultNodes=True)
        list_all_contents = list(set(list_all_contents) - set(default_nodes))
        materials = [
            material for material in mc.ls(materials=1)
            if material in list_all_contents
        ]
        textures = mc.ls(textures=1)
        check = False

        version_path = os.path.normpath(os.path.join(
            self.current_scene_path,
            '_VERSIONS'
        ))

        self.updateMasterPath()
        version_files = (f for f in os.listdir(version_path) if os.path.isfile(
            os.path.join(version_path, f)
        ))
        if version_files == [] and self.master_path is None:
            mc.warning('You need to save at least once...')
            return

        # for dirpath, dirnames, files in os.walk(self.current_scene_path):
        #     if files:
        #         for f in files:
        #             if f.lower().endswith('.ma'):
        #                 check = True
        #         if not check:
        #             mc.warning('You need to save at least once.')
        #             return
        #     if not files:
        #         mc.warning('You need to save at least once.')
        #         return

        if self.master_path is None or not os.path.exists(self.master_path):
            if self.last_version_path is None or not os.path.exists(
                self.last_version_path
            ):
                mc.warning('You need to save at least once...')
            else:
                file_path = self.last_version_path
        else:
            file_path = self.master_path

        scene_name = str(os.path.split(
            self.current_scene_path
        )[-1])

        mc.file(
            file_path,
            i=True,
            type="mayaAscii",
            ignoreVersion=True,
            mergeNamespacesOnClash=False,
            renamingPrefix=scene_name,
            options="v=0;",
            preserveReferences=True,
        )
        self.deleteEmptyNamespace()

        # Delete multiple identical materials.
        # List all materials but the default ones.
        new_materials = []
        list_all_contents = mc.ls()
        default_nodes = mc.ls(defaultNodes=True)
        list_all_contents = list(set(list_all_contents) - set(default_nodes))
        new_materials = [
            material for material in mc.ls(materials=1)
            if material in list_all_contents
        ]
        new = []

        for mat in new_materials:
            if mat not in materials:
                new.append(mat)
        # print 'NEW', new
        duplicates = []

        # Create a list of duplicates.
        for mat in materials:
            matching = [item for item in new_materials if mat in item]
            duplicates.extend(matching)

        # Find the initial materials.
        initials = set(materials) & set(new_materials)
        # print 'INITIALS', initials
        for mat in initials:
            if mat in duplicates:
                duplicates.remove(mat)
        # print 'DUPLICATES 2', duplicates

        # Assign initial materials and delete old ones.
        for mat in duplicates:
            if not mc.referenceQuery(mat, isNodeReferenced=True):
                old_shading_group = mc.listConnections(
                    '{0}.outColor'.format(mat),
                    type='shadingEngine'
                )
                initial_mat = [item for item in initials if item in mat][0]
                initial_shading_grp = mc.listConnections(
                    '{0}.outColor'.format(initial_mat),
                    type='shadingEngine'
                )[0]
                all_textures = mc.ls(textures=1)
                matching = set(textures) & set(all_textures)
                new_textures = [
                    item for item in all_textures if item not in matching
                ]

                meshes = mc.sets(old_shading_group, query=True)
                for mesh in meshes:
                    if not mc.objExists(mesh):
                        continue
                    mc.sets(
                        mesh, edit=True, forceElement=initial_shading_grp
                    )

                mc.delete(mat)
                mc.delete(old_shading_group)
                for texture in new_textures:
                    mc.delete(texture)
        # Delete Unused Nodes
        maya.mel.eval("""
            hyperShadePanelMenuCommand("hyperShadePanel1",
            "deleteUnusedNodes");
        """)

    def referenceScene(self):
        """Create a reference from a selected master scene."""
        self.updateMasterPath()

        # Check if Master scene exists.
        if os.path.exists(self.master_path) or os.path.exists(self.abc_path):
            # If so, let's import it.
            # self.default_sector_namespace = (
            #     self.ui.sectorComboBox.currentText()
            # )[:6]
            sector = self.ui.sectorComboBox.currentText()
            sector = re.sub('[^a-zA-Z_]+', '', sector)
            sector = re.sub(r'\W+', '', sector)
            self.default_sector_namespace = sector[:5]
            dialog = ReferenceDialog(
                self, currentData=self.default_sector_namespace,
                scene=self.current_scene_path
            )
            return_value = dialog.exec_()
            user_namespace = dialog.namespaceUser
            if return_value:
                if dialog.maya_checkbox.isChecked():
                    if os.path.exists(self.master_path):
                        mc.file(
                            self.master_path,
                            reference=True,
                            defaultNamespace=False,
                            namespace=user_namespace
                        )
                    else:
                        mc.warning(
                            "Could not find Master scene at {0}.".format(
                                self.master_path
                            ))
                if dialog.abc_checkbox.isChecked():
                    if os.path.exists(self.abc_path):
                        mc.file(
                            self.abc_path,
                            reference=True,
                            defaultNamespace=False,
                            namespace=user_namespace
                        )
                    else:
                        mc.warning(
                            "Could not find alembic at {0}.".format(
                                self.abc_path
                            ))
                if dialog.loc_checkbox.isChecked():
                    string_namespace = str(user_namespace + ':*')
                    mesh_list = mc.ls(
                        string_namespace,
                        transforms=True,
                        referencedNodes=True,
                        recursive=True
                    )

                    for mesh in mesh_list:
                        loc_name = str('loc_ref_' + mesh.replace(':', '_'))
                        loc_position = mc.xform(
                            mesh,
                            query=True,
                            worldSpace=True,
                            translation=True
                        )
                        mc.spaceLocator(name=loc_name, position=loc_position)
                    list_ref_locators = mc.ls('*loc_ref*', type='locator')
                    parent_group = '|loc_ref_grp'
                    if not mc.objExists(parent_group):
                        parent_group = mc.group(empty=True, name=parent_group)
                    loc_group = '{0}|{1}'.format(
                        parent_group,
                        'loc_ref_' + user_namespace
                    )
                    if not mc.objExists(loc_group):
                        loc_group = mc.group(
                            list_ref_locators,
                            name=('loc_ref_' + user_namespace)
                        )
                        mc.parent(loc_group, parent_group)
                    else:
                        mc.parent(
                            list_ref_locators,
                            loc_group
                        )

        else:
            # Forbid to import.
            if os.path.exists(
                self.last_version_path
            ) or self.last_version_path == '':
                mc.warning('You can only import a Master scene.')

    def deleteEmptyNamespace(self):
        """Delete empty namespaces of a scene."""
        namespace_list = mc.namespaceInfo(listOnlyNamespaces=True)
        contents = []
        for namespace in namespace_list:
            contents = mc.namespaceInfo(listNamespace=True)
            if contents is []:
                mc.namespace(namespace, removeNamespace=True)

    # ####################################################################### #
    #                            Current Scene Tab                            #
    # ####################################################################### #

    def updateScenePath(self):
        """Update the Scene Path according to the user selection."""
        selected_scene = self.ui.sceneList.selectedItems()
        self.current_scene_path = None
        if not selected_scene:
            return

        current_scene_folder = selected_scene[0].text()
        self.current_scene_path = os.path.normpath(os.path.join(
            self.current_sequence_path, current_scene_folder
        ))

        self.update()

    def updateFromTab(self, index):
        """Update UI when changing Tab."""
        if index == 0:
            self.updateToNewScenePath()
            self.ui.commentAnswerLabel02.clearFocus()

            # cat_index = self.ui.sequenceList.currentRow()
            # self.listSequences()
            # self.ui.sequenceList.setCurrentItem(cat_index)

            scene_index = self.ui.sceneList.currentRow()
            self.listScenes()
            self.ui.sceneList.setCurrentRow(scene_index)

        if index == 1:
            self.loadCurrentSceneInfo()
            self.ui.commentAnswerLabel01.clearFocus()

    def updateToNewScenePath(self):
        """Update the Scene Path Label."""
        self.ui.commentAnswerLabel01.clearFocus()
        self.updateScenePath()

        if (
            self.current_scene_path is not None and
            os.path.exists(self.current_scene_path)
        ):
            self.ui.saveVersionButton.setEnabled(True)
            self.ui.saveMasterButton.setEnabled(True)
            self.ui.snapshotButton.setEnabled(True)
            self.ui.currentSnapshotButton.setEnabled(True)
            self.ui.importButton.setEnabled(True)
            self.ui.currentImportButton.setEnabled(True)
            self.ui.currentScenePathLabel.setText(
                'Path Scene: ' + self.current_scene_path
            )
            self.ui.ref_scene_button.setEnabled(True)
            self.ui.import_scene_button.setEnabled(True)
            scene_name = os.path.split(self.current_scene_path)[-1]

        else:
            self.ui.saveVersionButton.setEnabled(False)
            self.ui.saveMasterButton.setEnabled(False)
            self.ui.snapshotButton.setEnabled(False)
            # self.ui.currentSnapshotButton.setEnabled(False)
            self.ui.importButton.setEnabled(False)
            # self.ui.currentImportButton.setEnabled(False)
            self.ui.ref_scene_button.setEnabled(False)
            self.ui.import_scene_button.setEnabled(False)
            self.ui.currentScenePathLabel.setText(
                'Select a Scene in the Project Tab.'
            )
            scene_name = None

        self.update_scene_info(
            scene_name,
            self.ui.versionAnswerLabel01,
            self.ui.artistAnswerLabel01,
            self.ui.dateAnswerLabel01,
            self.ui.commentAnswerLabel01
        )

        self.updateHistoryTable()
        self.updateReferenceTable()

    def updateHistoryTable(self):
        """Update the scene history table."""
        self.ui.sceneHistoryTable.clearContents()
        self.ui.sceneHistoryTable.setRowCount(0)

        if not self.current_scene_path:
            return
        path = os.path.join(
            self.current_scene_path,
            self.version_folder_name
        )
        if not os.path.exists(path):
            return
        files = [f for f in os.listdir(
            path
        ) if os.path.isfile(os.path.join(path, f))]
        files = files[::-1]

        self.ui.sceneHistoryTable.setRowCount(len(files))

        for index, filename in enumerate(files):
            filepath = os.path.normpath(os.path.join(path, filename))
            if not os.path.isfile(filepath):
                continue
            # Scene Name
            # file_name_item = QtWidgets.QTableWidgetItem(filename)
            file_text = str(filename).rsplit('.', 1)[0]
            file_name = file_text.split('_', 1)[0]
            file_version = file_text.rsplit('_')[-1]
            file_text = str('Version ' + file_version)
            file_name_item = QtWidgets.QTableWidgetItem(file_text)
            self.ui.sceneHistoryTable.setItem(index, 0, file_name_item)

            # Date
            file_path = os.path.join(path, filename)
            save_time = os.path.getmtime(file_path)
            file_date = datetime.datetime.fromtimestamp(int(save_time)). \
                strftime('%d %b %Y %H:%M')
            date_item = QtWidgets.QTableWidgetItem(file_date)
            self.ui.sceneHistoryTable.setItem(index, 1, date_item)

            # Load json dictionnary
            scene_info_file = os.path.join(
                self.current_scene_path,
                self.data_folder_name,
                self.data_file_name
            )
            data = []
            current_data = []
            with open(scene_info_file, 'r') as settings_file:
                    for line in settings_file.readlines():
                        data.append(dict(json.loads(line.strip())))

            for item in data:
                if file_name in item['Name']:
                    if int(file_version) == int(item['Version']):
                        if item not in current_data:
                            current_data.append(item)

            if len(current_data) > 1:
                raise ValueError('Too many values in current_data')
            elif len(current_data) == 0:
                raise ValueError('No current_data found')
            current_data = current_data[0]

            # Artist
            combobox = QtWidgets.QComboBox()
            # TODO: Disable scrolling
            combobox.setFocusPolicy(QtCore.Qt.StrongFocus)
            for name in self.users_list:
                combobox.addItem(name)
            if current_data['Artist'] in self.users_list:
                combobox.setCurrentText(current_data['Artist'])
            else:
                combobox.setCurrentText('Undifined')

            combobox.currentIndexChanged.connect(partial(
                self.tableClickedReturnPos,
                row=index, column=2,
                current_artist=combobox
            ))
            self.ui.sceneHistoryTable.setCellWidget(index, 2, combobox)

            # Comment
            text_edit = QtWidgets.QPlainTextEdit()
            if ('Comment' not in current_data or not current_data['Comment']):
                text_edit.setPlainText('')
                lines = 1
            else:
                text_edit.setPlainText(current_data['Comment'])
                lines = int(text_edit.blockCount())
            text_edit.setMinimumSize(50, 30)
            height = text_edit.fontMetrics().lineSpacing()
            self.ui.sceneHistoryTable.setRowHeight(index, height * (lines + 1))

            text_edit.textChanged.connect(partial(
                self.tableClickedReturnPos,
                row=index, column=3,
                comment_text=text_edit
            ))

            self.ui.sceneHistoryTable.setCellWidget(index, 3, text_edit)

            # Trash Image
            trash = QtWidgets.QPushButton()
            trash.setText('T')
            load_icon(trash, r'icons\trash.png')
            trash.setIconSize(QtCore.QSize(16, 16))
            trash.clicked.connect(partial(
                self.tableClickedReturnPos,
                row=index, column=4
            ))
            self.ui.sceneHistoryTable.setCellWidget(index, 4, trash)

    def tableClickedReturnPos(self, *args, **kwargs):
        """Return the position of an item."""
        row = -1
        column = -1
        current_artist = ''
        comment_text = ''
        if 'row' in kwargs:
            row = int(kwargs['row'])
        if 'column' in kwargs:
            column = int(kwargs['column'])
        if 'current_artist' in kwargs:
            current_artist = kwargs['current_artist']
        if 'comment_text' in kwargs:
            comment_text = kwargs['comment_text']

        if column == 4:
            self.tableClickedDelete(row)
            self.updateHistoryTable()
        if column == 2 and current_artist is not None:
            self.tableClickedArtist(
                row, column, artist_text=current_artist.currentText()
            )
        if column == 3 and comment_text is not None:
            self.tableClickedComment(
                row, column, comment=comment_text.toPlainText()
            )

    def deleteAllVersions(self, column):
        """Delete all versions of a scene except the last one."""
        number_of_rows = self.ui.sceneHistoryTable.rowCount()
        if number_of_rows < 1:
            mc.warning('Load a Half Pipe project first.')
            return
        if column == 4:
            question = (
                "Are you sure you want to delete every version?"
                " The last version won't be deleted."
            )
            message_box_return_value = \
                self.delete_confirmation_dialog(question)
            if not message_box_return_value:
                return

            for row in range(number_of_rows)[1:]:
                self.deleting_all = True
                self.tableClickedDelete(row)
            self.updateHistoryTable()

    def tableClickedDelete(self, row):
        """Delete a scene folder."""
        version = (self.ui.sceneHistoryTable.item(row, 0).text())[-3:]
        filename = str(
            os.path.split(self.current_scene_path)[-1] +
            '_' +
            version +
            '.ma')

        if not self.deleting_all:
            question = (
                "Are you sure you want to delete the {0} folder ?"
            ).format(filename[:-3])
            message_box_return_value = \
                self.delete_confirmation_dialog(question)
            if not message_box_return_value:
                return

        path_to_delete = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.version_folder_name,
            filename
        ))

        if os.path.exists(path_to_delete):
            # Remove the file
            current_scene = os.path.normpath(
                mc.file(query=True, sceneName=True)
            )
            if path_to_delete == current_scene:
                mc.warning(
                    'Could not delete the opened scene {0}!'.format(filename)
                )
                return
            else:
                os.remove(path_to_delete)

            # Delete version info in version file
            scene_info_file = os.path.normpath(os.path.join(
                self.current_scene_path,
                self.data_folder_name,
                self.data_file_name
            ))
            scenes_data = []
            updated_scenes_data = []
            if not os.path.exists(scene_info_file):
                mc.warning('Could not find the scene information file.')
                return
            with open(scene_info_file, 'r') as settings_file:
                    for line in settings_file.readlines():
                        scenes_data.append(json.loads(line.strip()))

            for dictionnary in scenes_data:
                if dictionnary['Version'] != version:
                    updated_scenes_data.append(dictionnary)

            os.remove(scene_info_file)

            for dictionnary in updated_scenes_data:
                with open(scene_info_file, 'a') as settings_file:
                    settings_file.write(json.dumps(dictionnary) + '\n')

            # Warn the user
            message = 'print "Scene {0} successfully deleted."'.format(
                filename
            )
            maya.mel.eval(message)
        else:
            mc.warning('Could not delete version. Path does not exist.')

        self.deleting_all = False

    def tableClickedOpen(self, row, column):
        """Open on older version."""
        if column == 0:
            file_text = (self.ui.sceneHistoryTable.item(row, 0).text())[-3:]
            filename = str(
                os.path.split(self.current_scene_path)[-1] +
                '_' +
                file_text +
                '.ma')

        path_to_open = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.version_folder_name,
            filename
        ))

        if os.path.exists(path_to_open):
            # check if there are unsaved changes
            fileCheckState = mc.file(q=True, modified=True)

            # if there are, save them first ... then we can proceed
            if fileCheckState:
                save_dialog = QtWidgets.QMessageBox(self)
                save_dialog.setWindowTitle('Warning: Scene Not Saved')
                save_dialog.setText('Save changes to scene?')
                save_dialog.setStandardButtons(
                    QtWidgets.QMessageBox.Save |
                    QtWidgets.QMessageBox.Discard |
                    QtWidgets.QMessageBox.Cancel
                )
                save_dialog.setDefaultButton(QtWidgets.QMessageBox.Save)
                return_value = save_dialog.exec_()

                # If Cancel is clicked:
                if return_value == QtWidgets.QMessageBox.Cancel:
                    return
                # If Don't Save is clicked:
                elif return_value == QtWidgets.QMessageBox.Discard:
                    mc.file(force=True, new=True)
                # If Save is clicked:
                else:
                    mc.SaveScene()
            else:
                pass

            mc.file(path_to_open, open=True, force=True)
            self.loadCurrentSceneInfo()
            message = 'print "Version {0} successfully opened."'.format(
                file_text
            )
            maya.mel.eval(message)

        else:
            mc.warning('Could not open version. Path does not exist.')

    def tableClickedArtist(self, row, column, artist_text):
        """Change the artist name in the version info."""
        if column == 2:
            version = (self.ui.sceneHistoryTable.item(row, 0).text())[-3:]
        scene_info_file = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.data_folder_name,
            self.data_file_name
        ))

        scenes_data = []
        with open(scene_info_file, 'r') as settings_file:
                for line in settings_file.readlines():
                    scenes_data.append(dict(json.loads(line.strip())))

        for index in range(len(scenes_data)):
            if int(version) == int(scenes_data[index]['Version']):
                scenes_data[index]['Artist'] = artist_text

        os.remove(scene_info_file)

        for dictionnary in scenes_data:
            with open(scene_info_file, 'a') as settings_file:
                settings_file.write(json.dumps(dictionnary) + '\n')

        self.loadCurrentSceneInfo()
        # self.updateHistoryTable()
        self.updateReferenceTable()

    def tableClickedComment(self, row, column, comment):
        """Change the comment in the version info."""
        if column == 3:
            version = (self.ui.sceneHistoryTable.item(row, 0).text())[-3:]
        scene_info_file = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.data_folder_name,
            self.data_file_name
        ))

        scenes_data = []
        with open(scene_info_file, 'r') as settings_file:
                for line in settings_file.readlines():
                    scenes_data.append(json.loads(line.strip()))

        for dictionnary in scenes_data:
            if version in str(dictionnary):
                dictionnary['Comment'] = comment

        os.remove(scene_info_file)

        for dictionnary in scenes_data:
            with open(scene_info_file, 'a') as settings_file:
                settings_file.write(json.dumps(dictionnary) + '\n')

        # self.ui.commentAnswerLabel01.setPlainText(comment)

# ########################################################################### #
#                              Current Scene Tab                              #
# ########################################################################### #

    def updateReferenceTable(self):
        """Update the reference table."""
        selected_items = self.ui.references_table.selectedItems()
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        self.ui.references_table.clearContents()
        self.ui.references_table.setRowCount(0)
        list_name_references = []
        list_path_references = []

        list_name_references = mc.namespaceInfo(':', listOnlyNamespaces=True)

        clean_namespace = []
        # Check if each namespace is empty.
        for namespace in list_name_references:
            contents = mc.namespaceInfo(
                namespace, listOnlyDependencyNodes=True
            )
            if contents is not None:
                clean_namespace.append(contents[0])
        list_name_references = clean_namespace

        # Find for each namespace the referenced file path.
        for namespace in list_name_references:
            if mc.referenceQuery(namespace, isNodeReferenced=True):
                ref_path = mc.referenceQuery(
                    namespace, filename=True
                )
                list_path_references.append(ref_path)

        self.ui.references_table.setRowCount(len(list_path_references))

        # Update the References Table from the scene info
        # of each referenced file.
        for index, full_path in enumerate(list_path_references):
            ref_path = full_path
            if '{' in ref_path:
                ref_path = full_path[:full_path.index('{')]
            # Image
            ref_data_file = os.path.normpath(os.path.join(
                (os.path.split(ref_path)[0]),
                self.data_folder_name
            ))
            if os.path.exists(ref_data_file):
                for file in os.listdir(ref_data_file):
                    if fnmatch.fnmatch(file, 'snapshot*'):
                        self.snapshot_file_name = file

            ref_image_path = os.path.normpath(os.path.join(
                (os.path.split(ref_path)[0]),
                self.data_folder_name,
                self.snapshot_file_name
            ))
            if ref_image_path is None:
                img = ImgWidget(r'icons\default_ref_img.png')
            elif not os.path.exists(ref_image_path):
                img = ImgWidget(r'icons\default_ref_img.png')
            else:
                img = ImgWidget(ref_image_path)

            self.ui.references_table.setCellWidget(index, 0, img)

            # Scene Name
            scene_name = (os.path.split(ref_path)[-1]).rsplit('.', 1)[0]
            namespace = mc.referenceQuery(full_path, namespace=True)
            scene_item = QtWidgets.QTableWidgetItem(
                '{0}\n{1}'.format(scene_name, namespace[1:])
            )
            self.ui.references_table.setItem(index, 1, scene_item)

            # Artist
            self.artist = None
            scene_info_path = os.path.normpath(os.path.join(
                (os.path.split(ref_path)[0]),
                self.data_folder_name,
                self.data_file_name
            ))

            if not os.path.exists(scene_info_path):
                self.artist = 'Undefined'
            else:
                data = []
                current_data = []
                scene_version = '000'
                if os.path.exists(scene_info_path):
                    with open(scene_info_path, 'r') as settings_file:
                        for line in settings_file.readlines():
                            data.append(json.loads(line.strip()))
                for item in data:
                    if scene_name in str(item):
                        if scene_version in str(item):
                            if item not in current_data:
                                current_data.append(item)
                dict_str = (str(current_data)).replace('[', '')
                dict_str = dict_str.replace(']', '')
                dict_str = dict_str.replace('u', '')
                updated_data = eval(dict_str)
                self.artist = updated_data['Artist']

            scene_artist = QtWidgets.QTableWidgetItem(self.artist)
            self.ui.references_table.setItem(index, 2, scene_artist)

            # Date
            save_time = os.path.getmtime(ref_path)
            file_date = datetime.datetime.fromtimestamp(int(save_time)). \
                strftime('%d %b %Y %H:%M')
            date_item = QtWidgets.QTableWidgetItem(file_date)
            self.ui.references_table.setItem(index, 3, date_item)

            if index in selected_rows:
                self.ui.references_table.selectRow(index)

    def referenceItemSelected(self):
        """Update variables from the reference table selection."""
        self.ref_paths = []
        self.selected_ref_names = []
        self.number_of_ref_rows_selected = len(
            self.ui.references_table.selectionModel().selectedRows()
        )
        rows = sorted(set(
            index.row() for index in self.ui.references_table.selectedIndexes()
        ))
        selected_references = []

        # Find all names of the selected rows.
        for row in sorted(rows):
            ref = self.ui.references_table.item(
                row, 1
            ).text()
            selected_references.append(ref.split('\n')[-1])

        # # List all the references path
        # all_paths = mc.file(q=True, list=True)
        #
        # # Find the namespaces for each scene
        # for name in selected_references:
        #     # Find the corresponding path.
        #     for path in all_paths:
        #         if name in str(path):
        #             self.ref_paths.append(path)

        clean_namespace = []
        for ref in selected_references:
            contents = mc.namespaceInfo(
                ref, listOnlyDependencyNodes=True
            )
            if contents is not None:
                clean_namespace.append(contents[0])
        list_name_references = clean_namespace

        # Find for each namespace the referenced file path.
        # full_paths = []
        for namespace in list_name_references:
            if mc.referenceQuery(namespace, isNodeReferenced=True):
                ref_path = mc.referenceQuery(
                    namespace, filename=True
                )
                self.ref_paths.append(ref_path)

            # Find all namespaces linked to the found path.
            for path in self.ref_paths:
                namespace = mc.referenceQuery(path, namespace=True)
                self.selected_ref_names.append(namespace)

        # Select all selected references in the table
        mc.select(clear=True)
        for name_ref in self.selected_ref_names:
            name = str(name_ref + ":*")
            mc.select(name, add=True)

    def namespaceDialog(self):
        """Open a dialog to change the namespace (Reference Table)."""
        self.referenceItemSelected()

        if self.number_of_ref_rows_selected == 0:
            mc.warning('Select one reference.')
        else:
            input_dialog, valid = QtWidgets.QInputDialog.getText(
                self,
                'Change the namespace',
                'Namespace:',
                QtWidgets.QLineEdit.Normal,
                ''
            )
            if not valid:
                return
            return_namespace = input_dialog
            return_namespace = formatName(return_namespace)

            if return_namespace is None or return_namespace == '':
                mc.warning('Invalid namespace.')
                return

            for path in self.ref_paths:
                mc.file(
                    path, edit=True,
                    namespace=return_namespace,
                    mergeNamespacesOnClash=True
                )
            message = """print "Successfully changed the namespace to {0}."
            """.format(
                return_namespace
            )
            maya.mel.eval(message)
            self.updateReferenceTable()

    def reloadReference(self):
        """Reload references (Reference Table)."""
        self.referenceItemSelected()
        if self.number_of_ref_rows_selected == 0:
            mc.warning('Select at least one reference.')
        else:
            for path in self.ref_paths:
                ref_node = mc.file(path, query=True, referenceNode=True)
                mc.file(loadReference=ref_node)
            message = 'print "Successfully reloaded references."'
            maya.mel.eval(message)
            self.updateReferenceTable()

    def importOneReference(self):
        """Import one reference (Reference Table)."""
        self.referenceItemSelected()
        if self.number_of_ref_rows_selected == 0:
            mc.warning('Select at least one reference.')
        else:
            for path in self.ref_paths:
                mc.file(
                    path,
                    importReference=True,
                    mergeNamespaceWithRoot=True
                )

            # Remove Empty Namespaces
            for namespace in self.selected_ref_names:
                if mc.namespace(exists=namespace):
                    mc.namespace(
                        removeNamespace=str(namespace),
                        mergeNamespaceWithRoot=True
                    )

            message = 'print "Successfully imported reference(s)."'
            maya.mel.eval(message)
            self.updateReferenceTable()

    def replaceReference(self):
        """Remove edits on a reference (Reference Table)."""
        self.referenceItemSelected()
        if self.number_of_ref_rows_selected == 0:
            mc.warning('Select at least one reference.')
        else:
            selected_file = QtWidgets.QFileDialog.getOpenFileName(
                    self,
                    "Select a Maya Scene",
                    self.project_path,
                    "Maya files (*.ma *.mb)"
                )

            for ref_name in self.selected_ref_names:
                name = str(ref_name + "RN")
                if not selected_file[0] == ('') is not None:
                    mc.file(selected_file[0], loadReference=name)

            message = 'print "Reference(s) uccessfully replaced."'
            maya.mel.eval(message)
            self.updateReferenceTable()

    def removeOneReference(self):
        """Remove selected reference (Reference Table)."""
        self.referenceItemSelected()
        if self.number_of_ref_rows_selected == 0:
            mc.warning('Select at least one reference.')
        else:
            for path in self.ref_paths:
                mc.file(path, removeReference=True)
            message = 'print "Successfully removed reference(s)."'
            maya.mel.eval(message)
            self.updateReferenceTable()

    def refOrImportAlembic(self):
        ref_or_import_box = QtWidgets.QMessageBox(self)
        ref_or_import_box.setText("What to do?")
        ref_or_import_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Retry
        )
        buttonYes = ref_or_import_box.button(QtWidgets.QMessageBox.Yes)
        buttonYes.setText("Import Alembic")
        buttonRetry = ref_or_import_box.button(QtWidgets.QMessageBox.Retry)
        buttonRetry.setText("Reference Alembic")
        ref_or_import_box.exec_()
        if ref_or_import_box.clickedButton() == buttonYes:
            self.openImportAlembic()
        elif ref_or_import_box.clickedButton() == buttonRetry:
            self.openReferenceAbc()
        else:
            return

    def openExportSelection(self):
        """Open the Maya Export Window."""
        if mc.ls(selection=True) == []:
            mc.warning('Select at least one object.')
        else:
            mel_command = 'ExportSelection;'
            maya.mel.eval(mel_command)
            self.updateReferenceTable()

    def openImportAlembic(self):
        """Open the Import Alembic Maya Window."""
        mel_command = 'AlembicImport;'
        maya.mel.eval(mel_command)
        self.updateReferenceTable()

    def openExportAbc(self):
        """Open the Export Alembic Maya Window."""
        if mc.ls(selection=True) == []:
            mc.warning('Select at least one object.')
        else:
            mel_command = 'AlembicExportSelection;'
            maya.mel.eval(mel_command)
            self.updateReferenceTable()

    def openReferenceAbc(self):
        """Open the Reference Alembic Maya Window."""
        mel_command = 'projectViewer AlembicReference;'
        maya.mel.eval(mel_command)
        self.updateReferenceTable()

    def exportShaders(self):
        """Export a maya scene and the link text."""
        ExportShaders.launch()

    def assembleShaders(self):
        """Assign shaders with the given links file."""
        ImportShaders.launch()

    def incrementalSave(self):
        """Save .ma scene in the selected scene versions folder."""
        # self.deleteUnknownNodes()

        file_name = os.path.split(self.current_scene_path)[-1]
        # SCENE01
        new_file_name = file_name + "_001" + ".ma"
        # SCENE01_v001.ma
        inc_save_folder_name = self.version_folder_name
        inc_save_folder_path = os.path.join(
            self.current_scene_path, inc_save_folder_name
        )
        # C:\RnD\CORGI\2_PROD\ANIMATION\SEQ_05\SCENE01\_VERSIONS
        inc_save_file_path = os.path.join(inc_save_folder_path, new_file_name)
        # C:\RnD\CORGI\2_PROD\ANIMATION\SEQ_05\SCENE01\_VERSIONS\SCENE01.ma

        new_file_path = None
        lastVersionNumber = 1
        if os.path.exists(inc_save_folder_path):
            versions = []
            versionsContent = sorted(os.listdir(inc_save_folder_path))
            for element in versionsContent:
                filename, extension = os.path.splitext(element)
                if extension == '.ma' and element != 'tmp.ma':
                    versions.append(filename[-3:])

            if len(versions):
                lastVersionNumber = int((sorted(versions))[-1]) + 1

            newVersionNumber = str('%03d' % (lastVersionNumber))
            # lastVersion = (sorted(versions))[-1]
            new_file_path = (
                inc_save_folder_path + '/' + file_name + '_' +
                newVersionNumber + '.ma'
            )
            new_file_path = os.path.normpath(new_file_path)
        else:
            os.makedirs(inc_save_folder_path)
            new_file_path = inc_save_file_path

        if new_file_path is None:
            return
        mc.file(rename=new_file_path)
        mc.file(save=True, type='mayaAscii')
        message = 'print "Successfully saved at {0}"'.format(new_file_path)
        maya.mel.eval(
            message.replace('\\', '\\\\')
        )

        self.save_scene_info(
            version_number=lastVersionNumber,
            artist_combox=self.ui.artistAnswerLabel02,
            commentEdit=self.ui.commentAnswerLabel02
        )
        self.autoSnapshot()
        self.blankComments()
        self.updateHistoryTable()

    def autoSnapshot(self):
        """Take a snapshot if there's none assigned to the scene."""
        # Check if there's a snapshot.
        path = os.path.normpath(os.path.join(
            self.current_scene_path,
            self.data_folder_name,
            self.snapshot_file_name
        ))

        if not os.path.exists(path):
            self.takeSnapshot()

    def blankComments(self):
        """Empty the comments."""
        self.ui.commentAnswerLabel01.setPlainText('')
        self.ui.commentAnswerLabel02.setPlainText('')
        self.ui.artistAnswerLabel02.setCurrentText(self.username)

    def deleteUnknownNodes(self):
        """Delete unknown nodes."""
        unknown = mc.ls(type='unknown')
        for node in unknown:
            check_referenced = mc.referenceQuery(node, isNodeReferenced=True)
            if not mc.objExists(node):
                continue
            elif check_referenced is True:
                continue
            mc.delete(node)

    def importMergeRefs(self):
        """Import and merge references."""
        # self.deleteUnknownNodes()

        references = mc.ls(references=True)
        paths = []
        for reference_node in references:
            ref_path = mc.referenceQuery(reference_node, filename=True)
            paths.append(ref_path)
        paths = list(set(paths))
        print 'PATHS', paths

        if not paths:
            print 'RETURN'
            return

        # for path in paths[1:]:
        for path in paths:
            # if not os.path.exists(path):
            #     print 'return'
            #     return
            ref_node = mc.file(path, q=True, referenceNode=True)
            loaded = mc.referenceQuery(ref_node, isLoaded=True)
            if loaded:
                namespace_from_path = mc.referenceQuery(
                    path, namespace=True, shortName=True
                )
                mc.file(path, importReference=True)
                mc.namespace(setNamespace=':')
                mc.namespace(
                    removeNamespace=str(namespace_from_path),
                    mergeNamespaceWithRoot=True
                )

            else:
                mc.file(
                    path, removeReference=True, mergeNamespaceWithRoot=True
                )

    def removeRig(self):
        """Remove all rig referenced in a scene."""
        # Find the reference file containing a bone.
        bone_list = mc.ls(type='joint', long=True)
        reference_file_list = []
        updated_reference_list = []
        for bone in bone_list:
            reference_file = mc.referenceQuery(
                str(bone), filename=True
            )
            reference_file_list.append(reference_file)

        # Kill all doubles in the list.
        for namespace in reference_file_list:
            if namespace not in updated_reference_list:
                updated_reference_list.append(namespace)

        # Remove the reference file.
        for path in updated_reference_list:
            mc.file(path, removeReference=True, mergeNamespaceWithRoot=True)

        self.deleteUnknownNodes()

    def removeShaders(self):
        """Remove all the shaders of the scene and assign Lambert 1."""
        # List all contents but the default shader nodes
        list_all_contents = mc.ls()
        default_nodes = mc.ls(defaultNodes=True)
        list_all_contents = list(set(list_all_contents) - set(default_nodes))

        # Remove Shaders
        shaders = [
            material for material in mc.ls(materials=1)
            if material in list_all_contents
        ]
        for shader in shaders:
            if not mc.referenceQuery(shader, isNodeReferenced=True):
                shading_groups = mc.listConnections(
                    '{0}.outColor'.format(shader),
                    type='shadingEngine'
                )
                for shading_group in shading_groups:
                    assigned_meshes = mc.sets(shading_group, q=True)
                    for mesh in assigned_meshes:
                        if not mc.objExists(mesh):
                            continue
                        mc.sets(
                            mesh, edit=True, forceElement='initialShadingGroup'
                        )
                mc.delete(shader)

        # Remove Shading Groups
        shading_groups = [
            shading_group for shading_group
            in mc.ls(exactType='shadingEngine')
            if shading_group in list_all_contents
        ]
        mc.delete(shading_groups)

        # Remove textures
        mc.delete(mc.ls(textures=1))

        # Delete Unused Nodes
        # maya.mel.eval("""
        #     'hyperShadePanelMenuCommand("hyperShadePanel1",
        #     "deleteUnusedNodes");
        # """)

        # Assign Lambert1 to the meshes in the scene
        # all_meshes = mc.ls(type='mesh', long=True)
        # for mesh in all_meshes:
        #     if not mc.referenceQuery(mesh, isNodeReferenced=True):
        #         mc.sets(
        #             mesh, edit=True, forceElement='initialShadingGroup'
        #         )

        # Exception for Utility Nodes
        utility_nodes = mc.listNodeTypes('utility')

        for node in list_all_contents:
            try:
                node_type = mc.objectType(node)
                if node_type in utility_nodes:
                    print 'Deleting : ' + node
                    mc.delete(node)
            except Exception:
                mc.warning(node + ' could not be cleaned from the master')

        # self.deleteUnknownNodes()

    def saveAbc(self):
        """Save an abc from the current frame of all meshes in the scene."""
        meshes = mc.ls(type="mesh")
        transforms = mc.listRelatives(meshes, parent=True, fullPath=True)
        current_frame = str(mc.currentTime(query=True))
        root = ""
        for transform in transforms:
            root = root + "-root " + transform + " "

        master_file_name = os.path.split(
            self.current_scene_path
        )[-1] + ".abc"
        master_file_path = os.path.normpath(os.path.join(
            self.current_scene_path, master_file_name
        ))
        if not os.path.exists(self.current_scene_path):
            mc.warning(
                "Could not save alembic at {0}.".format(master_file_path)
            )
            return
        command = (
            "-frameRange " + current_frame + " " + current_frame
            + " -uvWrite -worldSpace -dataFormat ogawa"
            + root + " -file " + master_file_path
        )
        mc.AbcExport(j=command)

    def optimizeSceneSize(self):
        """Optimize the scene size using Maya."""
        mel_command = 'OptimizeScene;'
        maya.mel.eval(mel_command)

    def saveMaster(self):
        """Save a master scene file."""
        master_file_name = os.path.split(
            self.current_scene_path
        )[-1] + ".ma"
        master_file_path = os.path.join(
            self.current_scene_path, master_file_name
        )

        if os.path.exists(master_file_path):
            mc.sysFile(master_file_path, delete=True)
            mc.file(rename=master_file_path)
            mc.file(save=True, type='mayaAscii')
            self.blankComments()
            message = 'print "Successfully saved at {0}"'.format(
                master_file_path
            )
            maya.mel.eval(
                message.replace('\\', '\\\\')
            )

        else:
            mc.file(rename=master_file_path)
            mc.file(save=True, type='mayaAscii')
            self.blankComments()
            message = 'print "Successfully saved at {0}"'.format(
                master_file_path
            )
            maya.mel.eval(
                message.replace('\\', '\\\\')
            )

        self.save_scene_info(
            artist_combox=self.ui.artistAnswerLabel02,
            commentEdit=self.ui.commentAnswerLabel02
        )
        self.autoSnapshot()
        self.updateHistoryTable()

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle('Master successfully saved!')
        msg_box.setText('What do you wanna do?')
        msg_box.addButton(
            'Stay in Master scene',
            QtWidgets.QMessageBox.RejectRole
        )
        msg_box.addButton(
            'New Scene',
            QtWidgets.QMessageBox.AcceptRole
        )
        return_value = msg_box.exec_()
        if return_value:
            mc.file(newFile=True)
            self.blankComments()

    def openSaveMasterDialog(self):
        """Open and apply options according to the selection."""
        dialog = SetSaveMasterDialog(self)
        return_value = dialog.exec_()

        checked = [checkbox.isChecked() for checkbox in dialog.checkboxes]
        if return_value is 0:
            return
        elif return_value and True not in checked:
            self.saveMaster()
            return
        if return_value and dialog.ui.checkBox_create_version.isChecked():
            self.incrementalSave()
        if return_value and dialog.ui.checkBox_create_abc.isChecked():
            self.saveAbc()
        if return_value and dialog.ui.checkBox_remove_rig.isChecked():
            self.removeRig()
        if return_value and dialog.ui.checkBox_imp_merge_refs.isChecked():
            self.importMergeRefs()
        if return_value and dialog.ui.checkBox_remove_shaders.isChecked():
            self.removeShaders()

        self.saveMaster()


class PipeToolMainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    """Define methods to launch the tool."""

    name = 'PipeToolWindow'

    def __init__(self, parent=None, dialog=None):
        """Initialize the window."""
        super(PipeToolMainWindow, self).__init__(parent=parent)

        self.setObjectName(self.name)
        self.setWindowTitle('Half Pipe')
        self.setCentralWidget(dialog)

    def closeEvent(self, event):
        """Kill scriptJobs when Half Pipe is closed."""
        central_widget = self.centralWidget()
        central_widget.timer.stop()
        event.accept()
