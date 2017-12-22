# -*- coding: utf-8 -*-
"""DOCSTRING."""

from PySide2 import QtCore
from PySide2 import QtWidgets

from functools import partial
from pipe.utils import load_icon


class Ui_back_up_dialog(object):
    """Define the Back Up Dialog UI."""

    def setupUi(self, back_up_dialog):
        """Set the Back Up Dialog UI from Designer."""
        back_up_dialog.setObjectName("back_up_dialog")
        back_up_dialog.resize(300, 350)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(back_up_dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.back_up_hl_1 = QtWidgets.QHBoxLayout()
        self.back_up_hl_1.setObjectName("back_up_hl_1")
        self.back_up_label = QtWidgets.QLabel(back_up_dialog)
        self.back_up_label.setObjectName("back_up_label")
        self.back_up_label.setMinimumSize(QtCore.QSize(0, 25))
        self.back_up_hl_1.addWidget(self.back_up_label)
        self.directory_back_up_button = QtWidgets.QPushButton(back_up_dialog)
        self.directory_back_up_button.setMinimumSize(QtCore.QSize(20, 0))
        self.directory_back_up_button.setMaximumSize(QtCore.QSize(20, 20))
        self.directory_back_up_button.setObjectName("directory_back_up_button")
        self.back_up_hl_1.addWidget(self.directory_back_up_button)
        self.verticalLayout_2.addLayout(self.back_up_hl_1)
        self.everything_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.everything_checkBox.setObjectName("everything_checkBox")
        self.verticalLayout_2.addWidget(self.everything_checkBox)
        self.preprod_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.preprod_checkBox.setObjectName("preprod_checkBox")
        self.verticalLayout_2.addWidget(self.preprod_checkBox)
        self.prod_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.prod_checkBox.setObjectName("prod_checkBox")
        self.verticalLayout_2.addWidget(self.prod_checkBox)
        self.back_up_hl_2 = QtWidgets.QHBoxLayout()
        self.back_up_hl_2.setSpacing(0)
        self.back_up_hl_2.setObjectName("back_up_hl_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.back_up_hl_2.addItem(spacerItem)
        self.prod_layout = QtWidgets.QVBoxLayout()
        self.prod_layout.setObjectName("prod_layout")
        self.back_up_hl_2.addLayout(self.prod_layout)
        self.verticalLayout_2.addLayout(self.back_up_hl_2)
        self.post_prod_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.post_prod_checkBox.setObjectName("post_prod_checkBox")
        self.verticalLayout_2.addWidget(self.post_prod_checkBox)
        self.input_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.input_checkBox.setObjectName("input_checkBox")
        self.verticalLayout_2.addWidget(self.input_checkBox)
        self.data_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.data_checkBox.setObjectName("data_checkBox")
        self.verticalLayout_2.addWidget(self.data_checkBox)
        self.output_checkBox = QtWidgets.QCheckBox(back_up_dialog)
        self.output_checkBox.setObjectName("output_checkBox")
        self.verticalLayout_2.addWidget(self.output_checkBox)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.back_up_hl_3 = QtWidgets.QHBoxLayout()
        self.back_up_hl_3.setObjectName("back_up_hl_3")
        self.backUp_pushButton = QtWidgets.QPushButton(back_up_dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.backUp_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.backUp_pushButton.setSizePolicy(sizePolicy)
        self.backUp_pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.backUp_pushButton.setObjectName("backUp_pushButton")
        self.back_up_hl_3.addWidget(self.backUp_pushButton)
        self.cancel_back_up_pushButton = QtWidgets.QPushButton(back_up_dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_back_up_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.cancel_back_up_pushButton.setSizePolicy(sizePolicy)
        self.cancel_back_up_pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.cancel_back_up_pushButton.setObjectName(
            "cancel_back_up_pushButton"
        )
        self.back_up_hl_3.addWidget(self.cancel_back_up_pushButton)
        self.verticalLayout_2.addLayout(self.back_up_hl_3)

        self.retranslateUi(back_up_dialog)
        QtCore.QMetaObject.connectSlotsByName(back_up_dialog)

    def retranslateUi(self, back_up_dialog):
        """Retranslate the UI of the Back Up Dialog."""
        _translate = QtCore.QCoreApplication.translate
        back_up_dialog.setWindowTitle(
            _translate("back_up_dialog", "Back Up")
        )
        self.back_up_label.setText(_translate(
            "back_up_dialog", "   Select a destination path for the Back Up.")
        )
        self.directory_back_up_button.setText(
            _translate("back_up_dialog", "F")
        )
        self.everything_checkBox.setText(
            _translate("back_up_dialog", "EVERYTHING")
        )
        self.preprod_checkBox.setText(
            _translate("back_up_dialog", "PREPROD")
        )
        self.prod_checkBox.setText(
            _translate("back_up_dialog", "PROD")
        )
        self.post_prod_checkBox.setText(
            _translate("back_up_dialog", "POST PROD")
        )
        self.input_checkBox.setText(
            _translate("back_up_dialog", "INPUT")
        )
        self.data_checkBox.setText(
            _translate("back_up_dialog", "DATA")
        )
        self.output_checkBox.setText(
            _translate("back_up_dialog", "OUTPUT")
        )
        self.backUp_pushButton.setText(
            _translate("back_up_dialog", "Back Up")
        )
        self.cancel_back_up_pushButton.setText(
            _translate("back_up_dialog", "Cancel")
        )


class BackUp (QtWidgets.QDialog):
    """Connect the Back Up Dialog to the UI and methods."""

    def __init__(self, parent=None):
        """Initialize default variables and functions."""
        super(BackUp, self).__init__(parent)
        self.parent = parent

        self.ui = Ui_back_up_dialog()
        self.ui.setupUi(self)

        load_icon(
            self.ui.directory_back_up_button, r'icons\look.png'
        )
        self.ui.directory_back_up_button.setIconSize(QtCore.QSize(12, 12))

        self.custom_checkboxes = []
        self.checkboxes = [
            self.ui.preprod_checkBox,
            self.ui.prod_checkBox,
            self.ui.post_prod_checkBox,
            self.ui.input_checkBox,
            self.ui.data_checkBox,
            self.ui.output_checkBox
        ]
        self.back_up_destination_path = None

        self.addCheckboxes()
        self.mapEvents()
        self.styleSheetUi()

    def styleSheetUi(self):
        """Make rounded background for label."""
        self.ui.back_up_label.setStyleSheet("""
            background-color: #393939;
            border-radius: 10px;
        """)

    def addCheckboxes(self):
        """Add a checkbox for every sector."""
        layout = self.ui.prod_layout
        items = [
            self.parent.ui.sectorComboBox.itemText(index)
            for index in range(self.parent.ui.sectorComboBox.count())
        ]
        for item in items:
            checkbox = QtWidgets.QCheckBox(item)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
            self.custom_checkboxes.append(checkbox)

    def mapEvents(self):
        """Connect UI to methods."""
        self.ui.backUp_pushButton.setEnabled(False)
        self.ui.backUp_pushButton.clicked.connect(self.accept)
        self.ui.cancel_back_up_pushButton.clicked.connect(self.reject)
        self.ui.everything_checkBox.clicked.connect(self.setStates)
        self.ui.prod_checkBox.clicked.connect(self.setAllProdStates)
        self.ui.directory_back_up_button.clicked.connect(self.fileDialog)

        for checkbox in self.checkboxes:
            checkbox.clicked.connect(partial(
                self.setEverythingState,
                checkbox=checkbox
            ))

        for checkbox in self.custom_checkboxes:
            checkbox.clicked.connect(partial(
                self.setProdState,
                checkbox=checkbox
            ))

    def setEverythingState(self, checkbox=None):
        """Set if Everything is checked or not."""
        state = checkbox.isChecked()
        everything_state = self.ui.everything_checkBox.isChecked()
        if not state and everything_state:
            self.ui.everything_checkBox.setChecked(False)

    def setStates(self):
        """Set all the boxes checked if Everything is checked."""
        state = self.ui.everything_checkBox.isChecked()
        for checkbox in self.checkboxes:
            checkbox.setChecked(state)

    def setProdState(self, checkbox=None):
        """Set if Production is checked or not."""
        state = checkbox.isChecked()
        prod_state = self.ui.prod_checkBox.isChecked()
        if not state and prod_state:
            self.ui.prod_checkBox.setChecked(False)

    def setAllProdStates(self):
        """Set all the production checkboxes if Production is checked."""
        state = self.ui.prod_checkBox.isChecked()
        for checkbox in self.custom_checkboxes:
            checkbox.setChecked(state)

    def fileDialog(self):
        """Open a File Dialog and return the selected folder path."""
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select a Destination",
            "C:/RnD"
        )

        self.back_up_destination_path = selected_folder
        self.ui.back_up_label.setText('  ' + self.back_up_destination_path)

        if self.back_up_destination_path is None:
            self.ui.backUp_pushButton.setEnabled(False)
        else:
            self.ui.backUp_pushButton.setEnabled(True)
