# -*- coding: utf-8 -*-
"""Change the settings of the current project."""

from PySide2 import QtCore
from PySide2 import QtWidgets

from functools import partial
import json
import maya.cmds as mc
import os

from pipe.utils import HALFPIPE_PATH_FILE
from pipe.utils import PROJECT_SETTINGS_FILE
from pipe.utils import SETTINGS_FILE

from pipe.utils import formatName
from pipe.utils import load_icon


class Ui_ProjectSettingsDialog(object):
    """Define the UI of the Project Settings Dialog."""

    def setupUi(self, ProjectSettingsDialog):
        """Generate the UI from Designer."""
        ProjectSettingsDialog.setObjectName("ProjectSettingsDialog")
        ProjectSettingsDialog.resize(400, 375)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ProjectSettingsDialog)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fps_layout = QtWidgets.QHBoxLayout()
        self.fps_layout.setObjectName("fps_layout")
        self.fps_icon = QtWidgets.QPushButton(ProjectSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fps_icon.sizePolicy().hasHeightForWidth()
        )
        self.fps_icon.setSizePolicy(sizePolicy)
        self.fps_icon.setMinimumSize(QtCore.QSize(30, 30))
        self.fps_icon.setObjectName("fps_icon")
        self.fps_layout.addWidget(self.fps_icon)
        self.fps_label = QtWidgets.QLabel(ProjectSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fps_label.sizePolicy().hasHeightForWidth()
        )
        self.fps_label.setSizePolicy(sizePolicy)
        self.fps_label.setMinimumSize(QtCore.QSize(30, 0))
        self.fps_label.setMaximumSize(QtCore.QSize(30, 16777215))
        self.fps_label.setObjectName("fps_label")
        self.fps_layout.addWidget(self.fps_label)
        self.fps_combobox = QtWidgets.QComboBox(ProjectSettingsDialog)
        self.fps_combobox.setMinimumSize(QtCore.QSize(0, 25))
        self.fps_combobox.setObjectName("fps_combobox")
        self.fps_layout.addWidget(self.fps_combobox)
        self.verticalLayout_2.addLayout(self.fps_layout)
        self.team_title_layout = QtWidgets.QHBoxLayout()
        self.team_title_layout.setObjectName("team_title_layout")
        self.team_icon = QtWidgets.QPushButton(ProjectSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.team_icon.sizePolicy().hasHeightForWidth()
        )
        self.team_icon.setSizePolicy(sizePolicy)
        self.team_icon.setMinimumSize(QtCore.QSize(30, 30))
        self.team_icon.setObjectName("team_icon")
        self.team_title_layout.addWidget(self.team_icon)
        self.teammates_label = QtWidgets.QLabel(ProjectSettingsDialog)
        self.teammates_label.setObjectName("teammates_label")
        self.team_title_layout.addWidget(self.teammates_label)
        self.verticalLayout_2.addLayout(self.team_title_layout)
        self.new_name_layout = QtWidgets.QHBoxLayout()
        self.new_name_layout.setObjectName("new_name_layout")
        self.new_name_label = QtWidgets.QLabel(ProjectSettingsDialog)
        self.new_name_label.setObjectName("new_name_label")
        self.new_name_layout.addWidget(self.new_name_label)
        self.new_name_line_edit = QtWidgets.QLineEdit(ProjectSettingsDialog)
        self.new_name_line_edit.setMinimumSize(QtCore.QSize(0, 25))
        self.new_name_line_edit.setObjectName("new_name_line_edit")
        self.new_name_layout.addWidget(self.new_name_line_edit)
        self.verticalLayout_2.addLayout(self.new_name_layout)
        self.list_name_layout = QtWidgets.QVBoxLayout()
        self.list_name_layout.setObjectName("list_name_layout")

        self.verticalLayout_2.addLayout(self.list_name_layout)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)

        self.your_name_layout = QtWidgets.QHBoxLayout()
        self.your_name_layout.setObjectName("your_name_layout")
        self.your_name_label = QtWidgets.QLabel(ProjectSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.your_name_label.sizePolicy().hasHeightForWidth()
        )
        self.your_name_label.setSizePolicy(sizePolicy)
        self.your_name_label.setMinimumSize(QtCore.QSize(70, 0))
        self.your_name_label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.your_name_label.setObjectName("your_name_label")
        self.your_name_layout.addWidget(self.your_name_label)
        self.names_combobox = QtWidgets.QComboBox(ProjectSettingsDialog)
        self.names_combobox.setMinimumSize(QtCore.QSize(0, 25))
        self.names_combobox.setObjectName("names_combobox")
        self.your_name_layout.addWidget(self.names_combobox)
        self.verticalLayout_2.addLayout(self.your_name_layout)
        self.no_turning_back_label = QtWidgets.QLabel(ProjectSettingsDialog)
        self.no_turning_back_label.setObjectName("no_turning_back_label")
        self.verticalLayout_2.addWidget(self.no_turning_back_label)
        self.exit_layout = QtWidgets.QHBoxLayout()
        self.exit_layout.setSpacing(9)
        self.exit_layout.setObjectName("exit_layout")
        self.apply_button = QtWidgets.QPushButton(ProjectSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_button.sizePolicy().hasHeightForWidth()
        )
        self.apply_button.setSizePolicy(sizePolicy)
        self.apply_button.setMinimumSize(QtCore.QSize(0, 40))
        self.apply_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.apply_button.setObjectName("apply_button")
        self.exit_layout.addWidget(self.apply_button)
        self.cancel_button = QtWidgets.QPushButton(ProjectSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_button.sizePolicy().hasHeightForWidth()
        )
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMinimumSize(QtCore.QSize(0, 40))
        self.cancel_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.cancel_button.setObjectName("cancel_button")
        self.exit_layout.addWidget(self.cancel_button)
        self.verticalLayout_2.addLayout(self.exit_layout)

        self.retranslateUi(ProjectSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(ProjectSettingsDialog)

    def retranslateUi(self, ProjectSettingsDialog):
        """Retranslate the UI of the Project Settings Dialog."""
        ProjectSettingsDialog.setWindowTitle("Project Settings")
        self.fps_icon.setText("I")
        self.fps_label.setText("FPS:")
        self.team_icon.setText("I")
        self.teammates_label.setText("Teammates:")
        self.new_name_label.setText("New Name:")
        self.your_name_label.setText("Your Name:")
        self.no_turning_back_label.setText("There are no turning back!")
        self.apply_button.setText("Apply")
        self.cancel_button.setText("Cancel")


class ProjectSettings(QtWidgets.QDialog):
    """Connect the Set Project Dialog to the UI and methods."""

    def __init__(self, parent=None, project=None):
        """Initialize default variables and functions."""
        super(ProjectSettings, self).__init__(parent)
        self.parent = parent

        self.default_fps = '24'
        self.fps_list = [
            '15',
            '24',
            '25',
            '30',
            '48',
            '50',
            '60',
        ]

        self.fps_dict = dict([
            ('15', 'game'),
            ('24', 'film'),
            ('25', 'pal'),
            ('30', 'ntsc'),
            ('48', 'show'),
            ('50', 'palf'),
            ('60', 'ntscf')
        ])

        self.string_command_fps = None
        self.users_list = []
        self.username = None
        self.project_name = project

        self.ui = Ui_ProjectSettingsDialog()
        self.ui.setupUi(self)
        self.pimpUI()
        self.loadProjectSettings()
        self.loadComputerSettings()
        self.updateFpsList()
        self.loadArtistsInUI()
        self.updateUserCombobox()
        self.mapEvents()

    def mapEvents(self):
        """Connect methods to the UI."""
        self.ui.apply_button.clicked.connect(self.returnInfo)
        self.ui.cancel_button.clicked.connect(self.reject)

        self.ui.fps_combobox.currentIndexChanged.connect(self.setFramerate)
        self.ui.new_name_line_edit.textEdited.connect(self.updateArtistName)
        self.ui.new_name_line_edit.returnPressed.connect(self.addNewName)

    def pimpUI(self):
        """Add images and stylesheet."""
        load_icon(self.ui.fps_icon, r'icons\people_2.png')
        self.ui.fps_icon.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.team_icon, r'icons\chrono.png')
        self.ui.team_icon.setIconSize(QtCore.QSize(12, 12))

        self.ui.fps_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

        self.ui.team_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

    def loadProjectSettings(self):
        """Load the json file containing fps and users info."""
        project_file_path = os.path.normpath(os.path.join(
            mc.workspace(fullName=True),
            PROJECT_SETTINGS_FILE
        ))

        self.project_data = []

        if os.path.exists(project_file_path):
            with open(project_file_path, 'r') as settings_file:
                self.project_data = json.loads(settings_file.read())
        else:
            return

        self.default_fps = self.project_data['fps']
        self.users_list = sorted(self.project_data['users_list'])

    def loadComputerSettings(self):
        """Load the user file containing the name of the user."""
        computer_settings_file = os.path.normpath(os.path.join(
            HALFPIPE_PATH_FILE,
            SETTINGS_FILE
        ))

        self.user_data = []

        if os.path.exists(computer_settings_file):
            with open(computer_settings_file, 'r') as settings_file:
                self.user_data = json.loads(settings_file.read())
        else:
            return

        self.username = self.user_data[self.project_name]

    def updateFpsList(self):
        """Add contents to fps list and set the Maya framerate."""
        self.ui.fps_combobox.clear()
        for number, string in self.fps_dict.items():
            if string == self.default_fps:
                fps_number = number

        for item in self.fps_list:
            self.ui.fps_combobox.addItem(item)
        index = self.ui.fps_combobox.findText(fps_number)
        if index == -1:
            self.ui.fps_combobox.setCurrentIndex(1)
        else:
            self.ui.fps_combobox.setCurrentIndex(index)

    def setFramerate(self):
        """Return the chosen fps."""
        fps = self.ui.fps_combobox.currentText()
        if not fps:
            return
        self.string_command_fps = str(self.fps_dict[fps])

    def addArtistItem(self, name):
        """Add a layout for a given name."""
        artist_widget = QtWidgets.QWidget(self)
        artist_widget.setMinimumSize(QtCore.QSize(30, 30))

        artist_layout = QtWidgets.QHBoxLayout(artist_widget)
        artist_layout.setContentsMargins(0, 0, 0, 0)
        artist_layout.setSpacing(6)
        artist_layout.setObjectName("artist_layout")

        artist_line_edit = QtWidgets.QLineEdit(artist_widget)
        artist_line_edit.setMinimumSize(QtCore.QSize(0, 25))
        artist_line_edit.setObjectName("artist_line_edit")
        artist_line_edit.setText(name)
        artist_line_edit.setEnabled(False)
        artist_layout.addWidget(artist_line_edit)

        artist_edit_button = QtWidgets.QPushButton(artist_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            artist_edit_button.sizePolicy().hasHeightForWidth()
        )
        artist_edit_button.setSizePolicy(sizePolicy)
        artist_edit_button.setMinimumSize(QtCore.QSize(25, 25))
        artist_edit_button.setMaximumSize(QtCore.QSize(25, 25))
        artist_edit_button.setObjectName("artist_edit_button")

        # Connect Modify button
        artist_edit_button.clicked.connect(partial(
            self.modifyArtistLineEdit,
            lineEdit=artist_line_edit
        ))

        load_icon(artist_edit_button, r'icons\edit.png')
        artist_layout.addWidget(artist_edit_button)

        artist_delete_button = QtWidgets.QPushButton(
            artist_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            artist_delete_button.sizePolicy().hasHeightForWidth()
        )
        artist_delete_button.setSizePolicy(sizePolicy)
        artist_delete_button.setMinimumSize(QtCore.QSize(25, 25))
        artist_delete_button.setMaximumSize(QtCore.QSize(25, 25))
        artist_delete_button.setObjectName("artist_delete_button")
        load_icon(artist_delete_button, r'icons\cross.png')

        artist_delete_button.clicked.connect(partial(
            self.removeArtistItem, widget=artist_widget, name=name
        ))

        artist_layout.addWidget(artist_delete_button)
        self.ui.list_name_layout.addWidget(artist_widget)
        self.ui.apply_button.setEnabled(True)

    def removeArtistItem(self, widget, name):
        """Remove an artist."""
        self.users_list = [
            self.ui.names_combobox.itemText(i)
            for i in range(self.ui.names_combobox.count())
        ]
        if len(self.users_list) <= 1:
            parent_widget = self.labels[0].parentWidget()
            temp_button = filter(
                lambda button: isinstance(
                    self.ui.artist_delete_button, QtWidgets.QPushButton
                ),
                parent_widget.children()
            )[0]
            temp_button.setEnabled(False)
        self.ui.list_name_layout.removeWidget(widget)
        widget.deleteLater()

        index = self.ui.names_combobox.findText(name)
        self.ui.names_combobox.removeItem(index)
        if self.ui.names_combobox.count() == 1:
            self.ui.apply_button.setEnabled(False)

    def modifyArtistLineEdit(self, lineEdit):
        """Enable and connect the Modify Line Edit."""
        self.old_name = lineEdit.text()
        lineEdit.setEnabled(True)

        lineEdit.returnPressed.connect(partial(
            self.editArtist,
            lineEdit=lineEdit
        ))

    def editArtist(self, lineEdit):
        """Change the artist name and update the UI and users_list."""
        self.team_info()
        new_name = lineEdit.text()
        if self.old_name in self.users_list:
            index = self.ui.names_combobox.findText(self.old_name)
            self.ui.names_combobox.removeItem(index)
            self.ui.names_combobox.addItem(new_name)
            self.users_list.remove(self.old_name)
            self.users_list.append(new_name)
        self.disableLineEdits(lineEdit)

    def disableLineEdits(self, lineEdit):
        """Disable Artists line edits."""
        self.team_info()
        for name in self.users_list:
            lineEdit.setEnabled(False)

    def loadArtistsInUI(self):
        """Create a layout for each name."""
        self.ui.names_combobox.clear()
        self.users_list.remove('Undefined')
        for name in self.users_list:
            self.addArtistItem(name)
            self.ui.names_combobox.addItem(name)
        self.ui.names_combobox.addItem('Undefined')

    def updateArtistName(self):
        """Update the format of the Artist Name."""
        line_edit = self.ui.new_name_line_edit
        line_edit.setMaxLength(10)
        valid_text = formatName(line_edit.text())
        line_edit.setText(valid_text)

    def addNewName(self):
        """Add a custom name."""
        self.users_list = [
            self.ui.names_combobox.itemText(i)
            for i in range(self.ui.names_combobox.count())
        ]

        new_name = self.ui.new_name_line_edit.text()
        self.ui.new_name_line_edit.clear()

        if new_name in self.users_list:
            return
        else:
            self.addArtistItem(new_name)
            self.ui.names_combobox.addItem(new_name)

    def updateUserCombobox(self):
        """Set the combobox to the current User."""
        if self.username is None or self.username not in self.users_list:
            index = self.ui.names_combobox.findText('Undefined')
            self.ui.names_combobox.setCurrentIndex(index)
        else:
            index = self.ui.names_combobox.findText(self.username)
            self.ui.names_combobox.setCurrentIndex(index)

    def team_info(self):
        """Return the Users Information."""
        self.username = self.ui.names_combobox.currentText()
        self.users_list = [
            self.ui.names_combobox.itemText(i)
            for i in range(self.ui.names_combobox.count())
        ]

    def returnInfo(self):
        """Accept the dialog and return mandatory information."""
        self.team_info()
        self.setFramerate()
        if self.username == 'Undefined':
            mc.warning('Pick your name!')
        else:
            self.accept()
