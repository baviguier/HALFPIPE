# -*- coding: utf-8 -*-
"""DOCSTRING."""

from PySide2 import QtWidgets

from functools import partial
import os

from pipe.utils import formatText


class SectorSettingsDialog(QtWidgets.QDialog):
    """Open the Sector Settings Box Dialog."""

    # ####################################################################### #
    #                         SECTOR SETTINGS DIALOG                          #
    # ####################################################################### #

    def __init__(self, item_list, project_path, parent=None):
        """Initialize the methods of the Sector Settings Dialog Box."""
        super(SectorSettingsDialog, self).__init__(parent)
        self.item_list = item_list
        self.project_path = project_path
        self.labels = []
        self.buildUi()
        self.createList()

    def buildUi(self):
        """UI of the Sector Settings Dialog Box."""
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.item_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.item_layout)
        self.line_edit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.line_edit)
        layout = QtWidgets.QHBoxLayout()
        spacer = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.apply_button = QtWidgets.QPushButton('Apply')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        layout.addItem(spacer)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.cancel_button)
        self.main_layout.addLayout(layout)

        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.line_edit.textChanged.connect(self.formatText)
        self.line_edit.returnPressed.connect(self.addItem)

        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def formatText(self):
        """Change the user text to respect folder name conventions."""
        name = self.line_edit.text()
        name = formatText(name)
        self.line_edit.setText(name)

    def createNewItem(self, label_text):
        """Create a label and button for a given name."""
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(widget)
        label = QtWidgets.QLabel(label_text)
        spacer = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        button = QtWidgets.QPushButton('X')
        if not len(self.labels):
            button.setEnabled(False)
        else:
            parent_widget = self.labels[0].parentWidget()
            label_button = filter(
                lambda button: isinstance(button, QtWidgets.QPushButton),
                parent_widget.children()
            )[0]
            label_button.setEnabled(True)
        button.clicked.connect(partial(
            self.removeItem, widget=widget, label=label
        ))
        layout.addWidget(label)
        layout.addItem(spacer)
        layout.addWidget(button)

        self.labels.append(label)
        self.item_layout.addWidget(widget)

    def removeItem(self, widget, label):
        """Delete Confirmation Dialog Box."""
        folders = os.listdir(self.project_path)
        for folder in folders:
            path = os.path.normpath(os.path.join(self.project_path, folder))
            if os.listdir(path) == []:
                continue
            else:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setText(
                    "Are you sure you want to delete the {0} folder ?".format(
                        label.text()
                    )
                )
                message_box.setInformativeText(
                    "All contents and references will be lost."
                )
                message_box.setStandardButtons(
                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
                )
                message_box.setDefaultButton(QtWidgets.QMessageBox.Cancel)
                return_value = message_box.exec_()
                if return_value == QtWidgets.QMessageBox.Cancel:
                    return

        if label in self.labels:
            self.labels.remove(label)
        if len(self.labels) <= 1:
            parent_widget = self.labels[0].parentWidget()
            button = filter(
                lambda button: isinstance(button, QtWidgets.QPushButton),
                parent_widget.children()
            )[0]
            button.setEnabled(False)
        self.main_layout.removeWidget(widget)
        widget.deleteLater()

    def createList(self):
        """Create a Label/Button for existing folders."""
        for item in self.item_list:
            self.createNewItem(item)

    def addItem(self):
        """When pressed Enter, add name to the list of folders."""
        name = self.line_edit.text()
        if not name.strip():
            return
        try:
            name = str(name).strip()
        except UnicodeEncodeError:
            return

        names = [label.text() for label in self.labels]
        if name in names:
            return

        self.createNewItem(name)
        self.line_edit.clear()

    def accepted(self, event):
        """Accept the entry."""
        # print 'accept'
        event.accept()
