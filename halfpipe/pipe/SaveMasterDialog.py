# -*- coding: utf-8 -*-
"""DOCSTRING."""

from PySide2 import QtCore
from PySide2 import QtWidgets


class Ui_save_master_dialog(object):
    """Define the UI of the Save Master Dialog."""

    def setupUi(self, save_master_dialog):
        """Set up the Save Master UI."""
        save_master_dialog.setObjectName("save_master_dialog")
        save_master_dialog.resize(259, 175)
        save_master_dialog.setMaximumSize(QtCore.QSize(16777215, 180))
        save_master_dialog.setAutoFillBackground(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(save_master_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_create_version = QtWidgets.QCheckBox(save_master_dialog)
        self.checkBox_create_version.setObjectName("checkBox_create_version")
        self.verticalLayout.addWidget(self.checkBox_create_version)

        self.checkBox_create_abc = QtWidgets.QCheckBox(save_master_dialog)
        self.checkBox_create_abc.setObjectName("checkBox_create_abc")
        self.verticalLayout.addWidget(self.checkBox_create_abc)

        self.checkBox_imp_merge_refs = QtWidgets.QCheckBox(save_master_dialog)
        self.checkBox_imp_merge_refs.setObjectName("checkBox_imp_merge_refs")
        self.verticalLayout.addWidget(self.checkBox_imp_merge_refs)
        self.checkBox_remove_rig = QtWidgets.QCheckBox(save_master_dialog)
        self.checkBox_remove_rig.setObjectName("checkBox_remove_rig")
        self.verticalLayout.addWidget(self.checkBox_remove_rig)
        self.checkBox_remove_shaders = QtWidgets.QCheckBox(save_master_dialog)
        self.checkBox_remove_shaders.setObjectName("checkBox_remove_shaders")
        self.verticalLayout.addWidget(self.checkBox_remove_shaders)
        self.smd_hl = QtWidgets.QHBoxLayout()
        self.smd_hl.setSpacing(6)
        self.smd_hl.setObjectName("smd_hl")
        self.save_master_dialog_button = QtWidgets.QPushButton(
            save_master_dialog
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.save_master_dialog_button.sizePolicy().hasHeightForWidth()
        )
        self.save_master_dialog_button.setSizePolicy(sizePolicy)
        self.save_master_dialog_button.setObjectName(
            "save_master_dialog_button"
        )
        self.smd_hl.addWidget(self.save_master_dialog_button)
        self.cancel_master_dialog_button = QtWidgets.QPushButton(
            save_master_dialog
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_master_dialog_button.sizePolicy().hasHeightForWidth()
        )
        self.cancel_master_dialog_button.setSizePolicy(sizePolicy)
        self.cancel_master_dialog_button.setObjectName(
            "cancel_master_dialog_button"
        )
        self.smd_hl.addWidget(self.cancel_master_dialog_button)
        self.verticalLayout.addLayout(self.smd_hl)

        self.retranslateUi(save_master_dialog)
        QtCore.QMetaObject.connectSlotsByName(save_master_dialog)

    def retranslateUi(self, save_master_dialog):
        """Retranslate the Save Master Dialog UI."""
        _translate = QtCore.QCoreApplication.translate
        save_master_dialog.setWindowTitle(_translate(
            "save_master_dialog", "Save Master")
        )
        self.checkBox_create_version.setText(_translate(
            "save_master_dialog", "Create Version Before")
        )
        self.checkBox_create_abc.setText("Create Alembic")
        self.checkBox_imp_merge_refs.setText(_translate(
            "save_master_dialog", "Import / Merge References")
        )
        self.checkBox_remove_rig.setText(_translate(
            "save_master_dialog", "Remove RIG")
        )
        self.checkBox_remove_shaders.setText(_translate(
            "save_master_dialog", "Remove Shaders")
        )
        self.save_master_dialog_button.setText(_translate(
            "save_master_dialog", "Save Master")
        )
        self.cancel_master_dialog_button.setText(_translate(
            "save_master_dialog", "Cancel")
        )


class SetSaveMasterDialog(QtWidgets.QDialog):
    """Connect the Save Master Dialog to the UI and methods."""

    def __init__(self, parent=None):
        """Initialize default variables and functions."""
        super(SetSaveMasterDialog, self).__init__(parent)

        self.ui = Ui_save_master_dialog()
        self.ui.setupUi(self)

        self.checkboxes = [
            self.ui.checkBox_create_version,
            self.ui.checkBox_create_abc,
            self.ui.checkBox_imp_merge_refs,
            self.ui.checkBox_remove_rig,
            self.ui.checkBox_remove_shaders
        ]

        self.mapEvents()

    def mapEvents(self):
        """Connect UI to methods."""
        self.ui.save_master_dialog_button.clicked.connect(self.accept)
        self.ui.cancel_master_dialog_button.clicked.connect(self.reject)
        # self.ui.checkBox_create_version.setChecked(True)
        self.ui.checkBox_imp_merge_refs.setChecked(True)
        # self.ui.checkBox_create_abc.setChecked(True)
