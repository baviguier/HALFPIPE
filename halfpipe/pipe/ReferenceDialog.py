# -*- coding: utf-8 -*-
"""DOCSTRING."""

from PySide2 import QtCore
from PySide2 import QtWidgets

import os
import re

# from pipe.utils import formatText


class Ui_Dialog(object):
    """Define the UI of the reference dialog."""

    def setupUi(self, Dialog):
        """Coding the UI from Designer."""
        Dialog.setObjectName("Dialog")
        Dialog.resize(340, 165)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.found_label = QtWidgets.QLabel(Dialog)
        self.found_label.setObjectName("found_label")
        self.verticalLayout.addWidget(self.found_label)
        self.ref_layout = QtWidgets.QHBoxLayout()
        self.ref_layout.setObjectName("ref_layout")
        self.maya_checkbox = QtWidgets.QCheckBox(Dialog)
        self.maya_checkbox.setObjectName("maya_checkbox")
        self.ref_layout.addWidget(self.maya_checkbox)
        self.alembic_checkbox = QtWidgets.QCheckBox(Dialog)
        self.alembic_checkbox.setObjectName("alembic_checkbox")
        self.ref_layout.addWidget(self.alembic_checkbox)
        self.verticalLayout.addLayout(self.ref_layout)
        self.ref_label = QtWidgets.QLabel(Dialog)
        self.ref_label.setObjectName("ref_label")
        self.verticalLayout.addWidget(self.ref_label)
        self.namespace_line_edit = QtWidgets.QLineEdit(Dialog)
        self.namespace_line_edit.setObjectName("namespace_line_edit")
        self.verticalLayout.addWidget(self.namespace_line_edit)
        self.add_locator_checkbox = QtWidgets.QCheckBox(Dialog)
        self.add_locator_checkbox.setObjectName("add_locator_checkbox")
        self.verticalLayout.addWidget(self.add_locator_checkbox)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        self.return_layout = QtWidgets.QHBoxLayout()
        self.return_layout.setSpacing(6)
        self.return_layout.setObjectName("return_layout")
        self.accept_ref_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.accept_ref_button.sizePolicy().hasHeightForWidth()
        )
        self.accept_ref_button.setSizePolicy(sizePolicy)
        self.accept_ref_button.setMinimumSize(QtCore.QSize(0, 40))
        self.accept_ref_button.setMaximumSize(QtCore.QSize(16777215, 45))
        self.accept_ref_button.setObjectName("accept_ref_button")
        self.return_layout.addWidget(self.accept_ref_button)
        self.cancel_ref_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_ref_button.sizePolicy().hasHeightForWidth()
        )
        self.cancel_ref_button.setSizePolicy(sizePolicy)
        self.cancel_ref_button.setMinimumSize(QtCore.QSize(0, 40))
        self.cancel_ref_button.setMaximumSize(QtCore.QSize(16777215, 45))
        self.cancel_ref_button.setObjectName("cancel_ref_button")
        self.return_layout.addWidget(self.cancel_ref_button)
        self.verticalLayout.addLayout(self.return_layout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        """Set texts in the UI."""
        Dialog.setWindowTitle("Reference Scene")
        self.found_label.setText("Nothing found.")
        self.maya_checkbox.setText("Reference Maya Scene")
        self.alembic_checkbox.setText("Reference Alembic")
        self.ref_label.setText("Namespace:")
        self.namespace_line_edit.setText("You cannot put nothing.")
        self.add_locator_checkbox.setText("Add locators")
        self.accept_ref_button.setText("Reference")
        self.cancel_ref_button.setText("Cancel")


class ReferenceDialog(QtWidgets.QDialog):
    """Connect the Save Master Dialog to the UI and methods."""

    def __init__(self, parent=None, currentData=None, scene=None):
        """Initialize default variables and functions."""
        super(ReferenceDialog, self).__init__(parent)
        self.currentData = currentData
        print 'CURRENT DATA', currentData
        self.current_scene_path = scene

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.mapEvents()
        self.findAvailable()

        self.namespaceUser = self.currentData
        self.loc_checkbox = self.ui.add_locator_checkbox
        self.maya_checkbox = self.ui.maya_checkbox
        self.abc_checkbox = self.ui.alembic_checkbox
        self.ui.namespace_line_edit.setText(self.currentData)

    def mapEvents(self):
        """Connect UI to methods."""
        self.ui.accept_ref_button.clicked.connect(self.accept)
        self.ui.cancel_ref_button.clicked.connect(self.reject)
        self.ui.namespace_line_edit.textEdited.connect(self.namespaceEdit)
        self.ui.maya_checkbox.clicked.connect(self.setAbcUnchecked)
        self.ui.alembic_checkbox.clicked.connect(self.setMayaUnchecked)

    def findAvailable(self):
        """Check if there is a Maya Scene and an alambic file."""
        basename = os.path.split(self.current_scene_path)[-1]
        maya_name = basename + ".ma"
        maya_path = os.path.normpath(
            os.path.join(self.current_scene_path, maya_name)
        )
        abc_name = basename + ".abc"
        abc_path = os.path.normpath(
            os.path.join(self.current_scene_path, abc_name)
        )
        maya_check = os.path.exists(maya_path)
        abc_check = os.path.exists(abc_path)
        if maya_check and abc_check:
            self.ui.found_label.setText("Maya scene and alembic found.")
        elif maya_check and not abc_check:
            self.ui.found_label.setText("Maya scene found.")
        elif not maya_check and abc_check:
            self.ui.found_label.setText("Alembic found.")
        elif not maya_check and not abc_check:
            self.ui.found_label.setText("Nothing found.")

        self.ui.maya_checkbox.setEnabled(maya_check)
        self.ui.alembic_checkbox.setEnabled(abc_check)

        if abc_check:
            self.ui.alembic_checkbox.setChecked(True)
        else:
            self.ui.maya_checkbox.setChecked(True)

    def setMayaUnchecked(self):
        """Set the Maya checkbox unchecked."""
        self.ui.maya_checkbox.setChecked(False)

    def setAbcUnchecked(self):
        """Set the alembic checkbox unchecked."""
        self.ui.alembic_checkbox.setChecked(False)

    def namespaceEdit(self):
        """Change the format of the edit and return its value."""
        text = self.ui.namespace_line_edit.text()
        valid_text = re.sub('[^a-zA-Z_]+', '', text)
        valid_text = re.sub(r'\W+', '', valid_text)
        # valid_text = formatText(self.ui.namespace_line_edit.text())
        self.ui.namespace_line_edit.setText(valid_text)
        valid = bool(valid_text)

        self.ui.accept_ref_button.setEnabled(valid)
        self.namespaceUser = self.ui.namespace_line_edit.text()
