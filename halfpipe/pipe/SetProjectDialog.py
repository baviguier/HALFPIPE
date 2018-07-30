# -*- coding: utf-8 -*-
"""DOCSTRING."""

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from functools import partial
import json
import maya.cmds as mc
import os

from pipe.utils import HALFPIPE_PATH_FILE
from pipe.utils import SETTINGS_FILE

from pipe.utils import formatName
from pipe.utils import formatText
from pipe.utils import load_icon


class Ui_project_settings_dialog(object):
    """Define the interface of the Project Settings Dialog."""

    def setupUi(self, project_settings_dialog):
        """Set the interface generated by Designer."""
        project_settings_dialog.setObjectName("project_settings_dialog")
        project_settings_dialog.resize(400, 500)
        project_settings_dialog.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(project_settings_dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.project_settings_tabWidget = QtWidgets.QTabWidget(
            project_settings_dialog
        )
        self.project_settings_tabWidget.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.project_settings_tabWidget.setLayoutDirection(
            QtCore.Qt.LeftToRight
        )
        self.project_settings_tabWidget.setTabPosition(
            QtWidgets.QTabWidget.North
        )
        self.project_settings_tabWidget.setTabShape(
            QtWidgets.QTabWidget.Rounded
        )
        self.project_settings_tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.project_settings_tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.project_settings_tabWidget.setObjectName(
            "project_settings_tabWidget"
        )
        self.create_project_tab = QtWidgets.QWidget()
        self.create_project_tab.setObjectName("create_project_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.create_project_tab)
        self.verticalLayout.setContentsMargins(3, 3, 3, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cp_hl_project_name = QtWidgets.QHBoxLayout()
        self.cp_hl_project_name.setObjectName("cp_hl_project_name")
        self.project_name_icon = QtWidgets.QPushButton(self.create_project_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.project_name_icon.sizePolicy().hasHeightForWidth()
        )
        self.project_name_icon.setSizePolicy(sizePolicy)
        self.project_name_icon.setMinimumSize(QtCore.QSize(30, 30))
        self.project_name_icon.setObjectName("project_name_icon")
        self.cp_hl_project_name.addWidget(self.project_name_icon)
        self.project_name_title_label = QtWidgets.QLabel(
            self.create_project_tab
        )
        self.project_name_title_label.setObjectName("project_name_title_label")
        self.cp_hl_project_name.addWidget(self.project_name_title_label)
        self.project_name_line = QtWidgets.QLineEdit(self.create_project_tab)
        self.project_name_line.setObjectName("project_name_line")
        self.project_name_line.setMinimumSize(QtCore.QSize(0, 25))
        self.cp_hl_project_name.addWidget(self.project_name_line)
        self.verticalLayout.addLayout(self.cp_hl_project_name)
        self.cp_hl_project_path = QtWidgets.QHBoxLayout()
        self.cp_hl_project_path.setSpacing(6)
        self.cp_hl_project_path.setObjectName("cp_hl_project_path")
        self.directory_icon = QtWidgets.QPushButton(self.create_project_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.directory_icon.sizePolicy().hasHeightForWidth()
        )
        self.directory_icon.setSizePolicy(sizePolicy)
        self.directory_icon.setMinimumSize(QtCore.QSize(30, 30))
        self.directory_icon.setObjectName("directory_icon")
        self.cp_hl_project_path.addWidget(self.directory_icon)
        self.cp_file_directory_label = QtWidgets.QLabel(
            self.create_project_tab
        )
        self.cp_file_directory_label.setObjectName("cp_file_directory_label")
        self.cp_hl_project_path.addWidget(self.cp_file_directory_label)
        self.create_project_path_label = QtWidgets.QLabel(
            self.create_project_tab
        )
        self.create_project_path_label.setObjectName(
            "create_project_path_label"
        )
        self.cp_hl_project_path.addWidget(self.create_project_path_label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.cp_hl_project_path.addItem(spacerItem)
        self.find_create_project_button = QtWidgets.QPushButton(
            self.create_project_tab
        )
        self.find_create_project_button.setMaximumSize(QtCore.QSize(25, 25))
        self.find_create_project_button.setObjectName(
            "find_create_project_button"
        )
        self.cp_hl_project_path.addWidget(self.find_create_project_button)
        self.verticalLayout.addLayout(self.cp_hl_project_path)
        self.fps_layout_hl = QtWidgets.QHBoxLayout()
        self.fps_layout_hl.setObjectName("fps_layout_hl")
        self.fps_icon = QtWidgets.QPushButton(self.create_project_tab)
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
        self.fps_layout_hl.addWidget(self.fps_icon)
        self.fps_label = QtWidgets.QLabel(self.create_project_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fps_label.sizePolicy().hasHeightForWidth()
        )
        self.fps_label.setSizePolicy(sizePolicy)
        self.fps_label.setMaximumSize(QtCore.QSize(30, 16777215))
        self.fps_label.setObjectName("fps_label")
        self.fps_layout_hl.addWidget(self.fps_label)
        self.fps_comboBox = QtWidgets.QComboBox(self.create_project_tab)
        self.fps_comboBox.setObjectName("fps_comboBox")
        self.fps_layout_hl.addWidget(self.fps_comboBox)
        self.verticalLayout.addLayout(self.fps_layout_hl)
        self.line = QtWidgets.QFrame(self.create_project_tab)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.teammates_hl = QtWidgets.QHBoxLayout()
        self.teammates_hl.setObjectName("teammates_hl")
        self.people_icon = QtWidgets.QPushButton(self.create_project_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.people_icon.sizePolicy().hasHeightForWidth()
        )
        self.people_icon.setSizePolicy(sizePolicy)
        self.people_icon.setMinimumSize(QtCore.QSize(30, 30))
        self.people_icon.setObjectName("people_icon")
        self.teammates_hl.addWidget(self.people_icon)
        self.teammates_label = QtWidgets.QLabel(self.create_project_tab)
        self.teammates_label.setObjectName("teammates_label")
        self.teammates_hl.addWidget(self.teammates_label)
        self.verticalLayout.addLayout(self.teammates_hl)
        self.name_hl = QtWidgets.QHBoxLayout()
        self.name_hl.setObjectName("name_hl")
        self.name_label = QtWidgets.QLabel(self.create_project_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.name_label.sizePolicy().hasHeightForWidth()
        )
        self.name_label.setSizePolicy(sizePolicy)
        self.name_label.setMaximumSize(QtCore.QSize(50, 16777215))
        self.name_label.setObjectName("name_label")
        self.name_hl.addWidget(self.name_label)
        self.name_line_edit = QtWidgets.QLineEdit(self.create_project_tab)
        self.name_line_edit.setObjectName("name_line_edit")
        self.name_line_edit.setMinimumSize(QtCore.QSize(0, 25))
        self.name_hl.addWidget(self.name_line_edit)
        self.verticalLayout.addLayout(self.name_hl)

        # Empty Layout
        self.layout_names = QtWidgets.QVBoxLayout()
        self.layout_names.setObjectName("layout_names")
        self.verticalLayout.addLayout(self.layout_names)

        self.your_name_hl = QtWidgets.QHBoxLayout()
        self.your_name_hl.setObjectName("your_name_hl")
        self.your_name_label = QtWidgets.QLabel(self.create_project_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.your_name_label.sizePolicy().hasHeightForWidth()
        )
        self.your_name_label.setSizePolicy(sizePolicy)
        self.your_name_label.setMinimumSize(QtCore.QSize(60, 0))
        self.your_name_label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.your_name_label.setObjectName("your_name_label")
        self.your_name_hl.addWidget(self.your_name_label)
        self.names_comboBox = QtWidgets.QComboBox(self.create_project_tab)
        self.names_comboBox.setObjectName("names_comboBox")
        self.your_name_hl.addWidget(self.names_comboBox)
        self.verticalLayout.addLayout(self.your_name_hl)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        self.cp_hl_output_buttons = QtWidgets.QHBoxLayout()
        self.cp_hl_output_buttons.setSpacing(6)
        self.cp_hl_output_buttons.setObjectName("cp_hl_output_buttons")
        self.apply_create_project_button = QtWidgets.QPushButton(
            self.create_project_tab
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_create_project_button.sizePolicy().hasHeightForWidth()
        )
        self.apply_create_project_button.setSizePolicy(sizePolicy)
        self.apply_create_project_button.setMinimumSize(QtCore.QSize(0, 40))
        self.apply_create_project_button.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.apply_create_project_button.setObjectName(
            "apply_create_project_button"
        )
        self.cp_hl_output_buttons.addWidget(self.apply_create_project_button)
        self.cancel_create_project_button = QtWidgets.QPushButton(
            self.create_project_tab
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_create_project_button.sizePolicy().hasHeightForWidth()
        )
        self.cancel_create_project_button.setSizePolicy(sizePolicy)
        self.cancel_create_project_button.setMinimumSize(QtCore.QSize(0, 40))
        self.cancel_create_project_button.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.cancel_create_project_button.setObjectName(
            "cancel_create_project_button"
        )
        self.cp_hl_output_buttons.addWidget(self.cancel_create_project_button)
        self.verticalLayout.addLayout(self.cp_hl_output_buttons)
        self.project_settings_tabWidget.addTab(self.create_project_tab, "")
        self.select_project_tab = QtWidgets.QWidget()
        self.select_project_tab.setObjectName("select_project_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.select_project_tab)
        self.verticalLayout_3.setContentsMargins(3, 6, 3, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sp_hl_path = QtWidgets.QHBoxLayout()
        self.sp_hl_path.setObjectName("sp_hl_path")
        self.selected_project_path_label = QtWidgets.QLabel(
            self.select_project_tab
        )
        self.selected_project_path_label.setObjectName(
            "selected_project_path_label"
        )
        self.sp_hl_path.addWidget(self.selected_project_path_label)
        self.find_select_project_button = QtWidgets.QPushButton(
            self.select_project_tab
        )
        self.find_select_project_button.setMaximumSize(QtCore.QSize(25, 25))
        self.find_select_project_button.setObjectName(
            "find_select_project_button"
        )
        self.sp_hl_path.addWidget(self.find_select_project_button)
        self.verticalLayout_3.addLayout(self.sp_hl_path)
        self.error_label = QtWidgets.QLabel(self.select_project_tab)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.error_label.setFont(font)
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setObjectName("error_label")
        self.verticalLayout_3.addWidget(self.error_label)

        self.set_username_layout = QtWidgets.QHBoxLayout()
        self.set_username_layout.setObjectName("set_username_layout")
        self.set_yourname_label = QtWidgets.QLabel(self.select_project_tab)
        self.set_yourname_label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.set_yourname_label.setObjectName("set_yourname_label")
        self.set_username_layout.addWidget(self.set_yourname_label)
        self.set_user_combo = QtWidgets.QComboBox(self.select_project_tab)
        self.set_user_combo.setMinimumSize(QtCore.QSize(150, 0))
        self.set_user_combo.setMaximumSize(QtCore.QSize(150, 50))
        self.set_user_combo.setObjectName("set_user_combo")
        self.set_username_layout.addWidget(self.set_user_combo)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.set_username_layout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.set_username_layout)

        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_3.addItem(spacerItem2)
        self.sp_hl_output_buttons = QtWidgets.QHBoxLayout()
        self.sp_hl_output_buttons.setObjectName("sp_hl_output_buttons")
        self.apply_select_project_button = QtWidgets.QPushButton(
            self.select_project_tab
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_select_project_button.sizePolicy().hasHeightForWidth()
        )
        self.apply_select_project_button.setSizePolicy(sizePolicy)
        self.apply_select_project_button.setMinimumSize(QtCore.QSize(0, 40))
        self.apply_select_project_button.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.apply_select_project_button.setObjectName(
            "apply_select_project_button"
        )
        self.sp_hl_output_buttons.addWidget(
            self.apply_select_project_button
        )
        self.cancel_select_project_button = QtWidgets.QPushButton(
            self.select_project_tab
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_select_project_button.sizePolicy().hasHeightForWidth()
        )
        self.cancel_select_project_button.setSizePolicy(sizePolicy)
        self.cancel_select_project_button.setMinimumSize(QtCore.QSize(0, 40))
        self.cancel_select_project_button.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.cancel_select_project_button.setObjectName(
            "cancel_select_project_button"
        )
        self.sp_hl_output_buttons.addWidget(self.cancel_select_project_button)
        self.verticalLayout_3.addLayout(self.sp_hl_output_buttons)
        self.project_settings_tabWidget.addTab(self.select_project_tab, "")
        self.verticalLayout_2.addWidget(self.project_settings_tabWidget)

        self.retranslateUi(project_settings_dialog)
        self.project_settings_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(project_settings_dialog)

    def retranslateUi(self, project_settings_dialog):
        """Retranslate the UI."""
        _translate = QtCore.QCoreApplication.translate
        project_settings_dialog.setWindowTitle(
            _translate("project_settings_dialog", "Set Project")
        )
        self.project_name_icon.setText(
            _translate("project_settings_dialog", "I")
        )
        self.project_name_title_label.setText(
            _translate("project_settings_dialog", "Project Name:")
        )
        self.directory_icon.setText(
            _translate("project_settings_dialog", "I")
        )
        self.cp_file_directory_label.setText(
            _translate("project_settings_dialog", "File Directory:")
        )
        self.create_project_path_label.setText(
            _translate("project_settings_dialog", "Project Path")
        )
        self.find_create_project_button.setText(
            _translate("project_settings_dialog", "F")
        )
        self.fps_icon.setText(
            _translate("project_settings_dialog", "I")
        )
        self.fps_label.setText(
            _translate("project_settings_dialog", "FPS:")
        )
        self.people_icon.setText(
            _translate("project_settings_dialog", "I")
        )
        self.teammates_label.setText(
            _translate("project_settings_dialog", "Teammates:")
        )
        self.name_label.setText(
            _translate("project_settings_dialog", "Name:")
        )
        self.your_name_label.setText(
            _translate("project_settings_dialog", "Your name:")
        )
        self.apply_create_project_button.setText(
            _translate("project_settings_dialog", "Apply")
        )
        self.cancel_create_project_button.setText(
            _translate("project_settings_dialog", "Cancel")
        )
        self.project_settings_tabWidget.setTabText(
            self.project_settings_tabWidget.indexOf(self.create_project_tab),
            _translate("project_settings_dialog", "Create Project")
        )
        self.selected_project_path_label.setText(
            _translate("project_settings_dialog", "Project Path")
        )
        self.find_select_project_button.setText(
            _translate("project_settings_dialog", "F")
        )
        self.error_label.setText(
            _translate("project_settings_dialog", "Error Information")
        )
        self.apply_select_project_button.setText(
            _translate("project_settings_dialog", "Apply")
        )
        self.cancel_select_project_button.setText(
            _translate("project_settings_dialog", "Cancel")
        )
        self.project_settings_tabWidget.setTabText(
            self.project_settings_tabWidget.indexOf(self.select_project_tab),
            _translate("project_settings_dialog", "Select Project")
        )
        self.set_yourname_label.setText("Your name:")


class SetProjectDialog(QtWidgets.QDialog):
    """Connect the Set Project Dialog to the UI and methods."""

    def __init__(self, parent=None, color=None):
        """Initialize default variables and functions."""
        super(SetProjectDialog, self).__init__(parent)
        self.parent = parent

        self.selected_folder = None
        self.create_folder = None
        self.string_command_fps = None
        self.artist_name = None
        self.user_name = None
        self.color = color
        self.users_list = []
        self.fps_list = [
            '15',
            '24',
            '25',
            '30',
            '48',
            '50',
            '60',
        ]

        self.ui = Ui_project_settings_dialog()
        self.ui.setupUi(self)

        self.mapEvents()
        self.styleSheetTab()
        self.changeIcons()
        self.updateFpsList()

        self.new_project_name = None
        self.new_project_path = None
        self.old_name = None
        self.ui.apply_create_project_button.setEnabled(False)

    def updateFpsList(self):
        """Add contents to fps list and set the Maya framerate."""
        self.ui.fps_comboBox.clear()
        for item in self.fps_list:
            self.ui.fps_comboBox.addItem(item)
        self.ui.fps_comboBox.setCurrentIndex(1)

    def mapEvents(self):
        """Connect UI to methods."""
        checked = self.checkDirectory()
        self.ui.apply_select_project_button.setEnabled(checked)

        self.ui.project_name_line.textEdited.connect(self.updateProjectName)

        self.ui.apply_create_project_button.clicked.connect(
            self.newProjectName
        )
        self.ui.apply_create_project_button.clicked.connect(self.team_info)

        self.ui.cancel_select_project_button.clicked.connect(self.reject)
        self.ui.cancel_create_project_button.clicked.connect(self.reject)

        self.ui.find_create_project_button.clicked.connect(
            self.returnCreateDirectoryPath
        )
        self.ui.find_select_project_button.clicked.connect(
            self.returnSelectDirectoryPath
        )

        self.ui.apply_select_project_button.clicked.connect(
            self.acceptSelectProject
        )

        self.ui.fps_comboBox.currentIndexChanged.connect(self.setFramerate)
        # self.ui.name_line_edit.textEdited.connect(
        #     self.updateArtistName(self.ui.name_line_edit)
        # )
        self.ui.name_line_edit.returnPressed.connect(self.addNewName)

    def styleSheetTab(self):
        """Change the UI."""
        self.ui.project_settings_tabWidget.setStyleSheet("""
            QTabWidget::pane { /* The tab widget frame */
                border-top: 0px;
            }

            QTabBar::tab {
                /* Text color */
                color: #888888;
                border: 0px solid #000000;
                border-bottom: 2px solid #333333;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 3px 5px 3px 5px;
                margin: 7px 10px 0px 7px;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                border-bottom-color: """ + self.color + """;
            }
        """)

        self.ui.project_name_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

        self.ui.directory_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

        self.ui.fps_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

        self.ui.people_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

    def load_image(self, labelToChange, image_path):
        """Replace a label by an image."""
        full_image_path = os.path.join(
            os.path.split(__file__)[0],
            "..",
            image_path
        )
        pixmap = QtGui.QPixmap(full_image_path)
        pixmap_resized = pixmap.scaled(12, 12)
        labelToChange.setPixmap(pixmap_resized)

    def changeIcons(self):
        """Change the Find Icons."""
        load_icon(
            self.ui.find_create_project_button, r'icons\look.png'
        )
        self.ui.find_create_project_button.setIconSize(QtCore.QSize(12, 12))
        load_icon(
            self.ui.find_select_project_button, r'icons\look.png'
        )
        self.ui.find_select_project_button.setIconSize(QtCore.QSize(12, 12))

        load_icon(self.ui.project_name_icon, r'icons\home.png')
        self.ui.project_name_icon.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.directory_icon, r'icons\folder.png')
        self.ui.directory_icon.setIconSize(QtCore.QSize(12, 12))
        load_icon(self.ui.fps_icon, r'icons\chrono.png')
        load_icon(self.ui.people_icon, r'icons\people_2.png')
        self.ui.directory_icon.setIconSize(QtCore.QSize(12, 12))

    def setFramerate(self):
        """Write the chosen fps on the disk and set the Maya fps."""
        fps_dict = dict([
            ('15', 'game'),
            ('24', 'film'),
            ('25', 'pal'),
            ('30', 'ntsc'),
            ('48', 'show'),
            ('50', 'palf'),
            ('60', 'ntscf')
        ])
        fps = self.ui.fps_comboBox.currentText()
        if not fps:
            return
        self.string_command_fps = str(fps_dict[fps])

    def fileDialog(self):
        """Open a File Dialog and return the selected folder path."""
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select a Half Pipe Project",
            "C:/"
        )

        return selected_folder

    def returnCreateDirectoryPath(self):
        """Return the path needed for the creation of the project."""
        self.create_folder = self.fileDialog()

        if self.create_folder is None:
            self.ui.create_project_path_label.setText('  No selected folder.')
            self.ui.apply_create_project_button.setEnabled(False)
            return

        for folder in self.parent.workspace_folder_list.values():
            category_path = os.path.normpath(
                os.path.join(self.create_folder, folder)
            )
            if os.path.exists(category_path):
                self.ui.create_project_path_label.setText(
                    r"  There's already a project!"
                )
                self.ui.apply_create_project_button.setEnabled(False)
            else:
                self.ui.create_project_path_label.setText(
                    self.create_folder
                )
                self.ui.apply_create_project_button.setEnabled(True)

        self.updateProjectName()

    def returnSelectDirectoryPath(self):
        """Return the path needed to select a project."""
        self.selected_folder = self.fileDialog()
        checked = self.checkDirectory()
        self.new_project_path = self.selected_folder
        self.ui.apply_select_project_button.setEnabled(checked)
        self.printPath()
        self.fillUserCombobox()

    # ####################################################################### #
    #                             Create Project                              #
    # ####################################################################### #

    def newProjectName(self):
        """Create a path with the given folder name."""
        self.new_project_name = self.ui.project_name_line.text()
        self.new_project_path = os.path.normpath(
            os.path.join(self.create_folder, self.new_project_name)
        )

        if os.path.exists(self.new_project_path):
            mc.warning(
                'Folder already exists at {0}'.format(self.new_project_path)
            )
            return

        self.accept()

    def updateProjectName(self):
        """Update the format of the Project Name line edit."""
        valid_text = formatText(self.ui.project_name_line.text())
        self.ui.project_name_line.setText(valid_text)
        text = self.ui.names_comboBox.currentText()
        valid = bool(valid_text) and bool(self.create_folder) and text != ""
        self.ui.apply_create_project_button.setEnabled(valid)

    def printPath(self):
        """Change the project path labels."""
        self.ui.create_project_path_label.setText('')
        self.ui.selected_project_path_label.setText('')

        self.ui.create_project_path_label.setText(self.create_folder)
        self.ui.selected_project_path_label.setText(self.selected_folder)

    def updateArtistName(self, line_edit):
        """Update the format of the Artist Name."""
        line_edit.setMaxLength(10)
        valid_text = formatName(line_edit.text())
        line_edit.setText(valid_text)

    def addNewName(self):
        """Add a custom name."""
        self.users_list = []
        self.users_list = [
            self.ui.names_comboBox.itemText(i)
            for i in range(self.ui.names_comboBox.count())
        ]

        new_name = self.ui.name_line_edit.text()

        if new_name in self.users_list:
            self.ui.name_line_edit.clear()
            return
        else:
            self.addArtistLayout(new_name)
        self.ui.name_line_edit.clear()
        self.updateProjectName()

    def addArtistLayout(self, name):
        """Add a line edit, modify and delete button to the UI."""
        self.artist_name = name
        layout_name = str(self.artist_name + '_horizontal_layout')
        edit_str = str(self.artist_name + '_line_edit')
        modify_name = str(self.artist_name + '_modify_button')
        # delete_button = str(self.artist_name + '_delete_button')
        delete_name = 'delete_button'
        artist_widget = QtWidgets.QWidget(self)
        # artist_widget.setObjectName(self.artist_name + '_widget')

        layout = QtWidgets.QHBoxLayout(artist_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.setObjectName(layout_name)
        edit_name = QtWidgets.QLineEdit(
            self.ui.create_project_tab
        )
        edit_name.setObjectName(edit_str)
        layout.addWidget(edit_name)
        edit_name.setMinimumSize(QtCore.QSize(0, 25))
        modify_button = QtWidgets.QPushButton(
            self.ui.create_project_tab
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            modify_button.sizePolicy().hasHeightForWidth()
        )
        modify_button.setSizePolicy(sizePolicy)
        modify_button.setMaximumSize(QtCore.QSize(
            30, 1677721
        ))
        modify_button.setObjectName(modify_name)
        layout.addWidget(modify_button)
        delete_button = QtWidgets.QPushButton(
            self.ui.create_project_tab
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            delete_button.sizePolicy().hasHeightForWidth()
        )
        delete_button.setSizePolicy(sizePolicy)
        delete_button.setMaximumSize(QtCore.QSize(
            30, 1677721)
        )
        delete_button.setObjectName(delete_name)
        delete_button.clicked.connect(partial(
            self.removeArtistItem,
            widget=artist_widget,
            lineEdit=edit_name
        ))

        # Connect Modify button
        modify_button.clicked.connect(partial(
            self.modifyArtistLineEdit,
            lineEdit=edit_name
        ))

        layout.addWidget(delete_button)
        self.ui.layout_names.addWidget(artist_widget)

        self.ui.name_line_edit.setText('')
        edit_name.setText(self.artist_name)
        edit_name.setEnabled(False)
        load_icon(
            modify_button, r'icons\edit.png'
        )
        load_icon(
            delete_button, r'icons\cross.png'
        )
        self.ui.names_comboBox.addItem(self.artist_name)
        self.team_info()

        self.ui.apply_create_project_button.setEnabled(True)

    def removeArtistItem(self, widget, lineEdit):
        """Remove an artist item from the layout."""
        self.team_info()
        name = lineEdit.text()
        if name in self.users_list:
            index = self.ui.names_comboBox.findText(str(name))
            self.ui.names_comboBox.removeItem(index)
        self.ui.layout_names.removeWidget(widget)
        widget.deleteLater()
        self.ui.name_line_edit.clear()
        if self.ui.names_comboBox.count() < 1:
            self.ui.apply_create_project_button.setEnabled(False)

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
            index = self.ui.names_comboBox.findText(self.old_name)
            self.ui.names_comboBox.removeItem(index)
            self.ui.names_comboBox.addItem(new_name)
            self.users_list.remove(self.old_name)
            self.users_list.append(new_name)
        self.disableLineEdits(lineEdit)

    def disableLineEdits(self, lineEdit):
        """Disable Artists line edits."""
        self.team_info()
        for name in self.users_list:
            # lineEdit = 'self.ui.' + name + '_line_edit'
            lineEdit.setEnabled(False)

    def team_info(self):
        """Return all the team information."""
        self.user_name = self.ui.names_comboBox.currentText()
        self.users_list = [
            self.ui.names_comboBox.itemText(i)
            for i in range(self.ui.names_comboBox.count())
        ]

    # ####################################################################### #
    #                             Select Project                              #
    # ####################################################################### #

    def fillUserCombobox(self):
        """Fill the user combo box so he can pick his name."""
        self.ui.set_user_combo.clear()
        checked = self.checkDirectory()
        user = None
        if checked:
            # Load Project Data
            project_settings_path = os.path.normpath(os.path.join(
                self.selected_folder,
                "project_settings.json"
            ))
            if os.path.exists(project_settings_path):
                with open(project_settings_path, 'r') as settings_file:
                    project_data = json.loads(settings_file.read())

                if (
                    not project_data or
                    'users_list' not in project_data or
                    not project_data['users_list']
                ):
                    self.ui.set_user_combo.clear()
                else:
                    users = project_data['users_list']
                    for user in users:
                        self.ui.set_user_combo.addItem(user)
            else:
                self.ui.set_user_combo.clear()

            # Load User Data
            user_settings_path = os.path.join(
                HALFPIPE_PATH_FILE, SETTINGS_FILE
            )
            if os.path.exists(user_settings_path):
                with open(user_settings_path, 'r') as settings_file:
                    user_data = json.loads(settings_file.read())

                project_name = os.path.split(self.selected_folder)[-1]
                if (
                    project_name not in user_data or
                    not user_data[project_name]
                ):
                    user = None
                else:
                    user = user_data[project_name]
                    self.ui.set_user_combo.setCurrentText(user)
            else:
                user = None

            if user is None:
                self.ui.set_user_combo.setCurrentText('Undefined')

    def checkDirectory(self):
        """Check if the selected directory contains a project."""
        self.ui.error_label.setText('')

        if self.selected_folder is None:
            self.ui.error_label.setText('No selected folder.')
            return False

        for folder in self.parent.workspace_folder_list.values():
            category_path = os.path.normpath(
                os.path.join(self.selected_folder, folder)
            )
            if not os.path.exists(category_path):
                self.ui.error_label.setText('Could not find project.')
                return False

        if not os.path.exists(os.path.normpath(
            os.path.join(self.selected_folder, 'workspace.mel')
        )):
            self.parent.createMELworkspace(path=self.selected_folder)

        # print os.path.join(os.path.normpath(
        #     os.path.join(self.selected_folder, 'workspace.mel')
        # ))
        return True

    def acceptSelectProject(self):
        """Update the username and close the window."""
        self.user_name = self.ui.set_user_combo.currentText()
        self.accept()
