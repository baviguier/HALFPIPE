"""DOCSTRING."""

from PySide2 import QtCore
from PySide2 import QtWidgets

from functools import partial
import json
import os
import re

from pipe.utils import load_icon

from pipe.utils import PROJECT_SETTINGS_FILE


class Ui_PrefillDialog(object):
    """Code the UI for the Pre Fill Dialog."""

    def setupUi(self, PrefillDialog):
        """Code the UI from Designer."""
        PrefillDialog.setObjectName("PrefillDialog")
        PrefillDialog.resize(259, 344)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PrefillDialog)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.setObjectName("title_layout")
        self.title_icon = QtWidgets.QPushButton(PrefillDialog)
        self.title_icon.setMinimumSize(QtCore.QSize(30, 30))
        self.title_icon.setMaximumSize(QtCore.QSize(30, 30))
        self.title_icon.setObjectName("title_icon")
        self.title_layout.addWidget(self.title_icon)
        self.title_label = QtWidgets.QLabel(PrefillDialog)
        self.title_label.setObjectName("title_label")
        self.title_layout.addWidget(self.title_label)
        self.verticalLayout_2.addLayout(self.title_layout)
        self.use_prefill_checkbox = QtWidgets.QCheckBox(PrefillDialog)
        self.use_prefill_checkbox.setObjectName("use_prefill_checkbox")
        self.verticalLayout_2.addWidget(self.use_prefill_checkbox)
        self.line = QtWidgets.QFrame(PrefillDialog)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.dept_widget = QtWidgets.QWidget()
        self.dept_widget.setMinimumSize(QtCore.QSize(30, 30))
        self.dept_v_layout = QtWidgets.QVBoxLayout(self.dept_widget)
        self.dept_v_layout.setObjectName("dept_v_layout")

        # self.single_dept_layout = QtWidgets.QHBoxLayout()
        # self.single_dept_layout.setObjectName("single_dept_layout")
        # self.dept_label = QtWidgets.QLabel(PrefillDialog)
        # self.dept_label.setMinimumSize(QtCore.QSize(120, 0))
        # self.dept_label.setObjectName("dept_label")
        # self.single_dept_layout.addWidget(self.dept_label)
        # self.dept_lineedit = QtWidgets.QLineEdit(PrefillDialog)
        # self.dept_lineedit.setObjectName("dept_lineedit")
        # self.single_dept_layout.addWidget(self.dept_lineedit)
        # self.dept_edit_button = QtWidgets.QPushButton(PrefillDialog)
        # self.dept_edit_button.setMinimumSize(QtCore.QSize(22, 22))
        # self.dept_edit_button.setMaximumSize(QtCore.QSize(22, 22))
        # self.dept_edit_button.setObjectName("dept_edit_button")
        # self.single_dept_layout.addWidget(self.dept_edit_button)
        # self.dept_v_layout.addLayout(self.single_dept_layout)

        self.verticalLayout_2.addWidget(self.dept_widget)
        # self.verticalLayout_2.addLayout(self.dept_v_layout)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.exit_layout = QtWidgets.QHBoxLayout()
        self.exit_layout.setObjectName("exit_layout")
        self.apply_button = QtWidgets.QPushButton(PrefillDialog)
        self.apply_button.setMinimumSize(QtCore.QSize(0, 40))
        self.apply_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.apply_button.setObjectName("apply_button")
        self.exit_layout.addWidget(self.apply_button)
        self.cancel_button = QtWidgets.QPushButton(PrefillDialog)
        self.cancel_button.setMinimumSize(QtCore.QSize(0, 40))
        self.cancel_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.cancel_button.setObjectName("cancel_button")
        self.exit_layout.addWidget(self.cancel_button)
        self.verticalLayout_2.addLayout(self.exit_layout)

        self.retranslateUi(PrefillDialog)
        QtCore.QMetaObject.connectSlotsByName(PrefillDialog)

    def retranslateUi(self, PrefillDialog):
        """Set UI titles."""
        PrefillDialog.setWindowTitle("Pre Fill Dialog")
        self.title_icon.setText("I")
        self.title_label.setText("Pre Fill Options")
        self.use_prefill_checkbox.setText("Use Pre Fill")
        # self.dept_label.setText("DEPT")
        # self.dept_edit_button.setText("R")
        self.apply_button.setText("APPLY")
        self.cancel_button.setText("CANCEL")


class Prefill(QtWidgets.QDialog):
    """Let the user define prefix."""

    def __init__(self, project_path, parent=None):
        """Initialize the dialog."""
        super(Prefill, self).__init__(parent)
        self.prod_path = os.path.normpath(os.path.join(
            project_path,
            '2_PROD'
        ))
        self.full_project_path = project_path
        self.prefix_dict = {}

        self.ui = Ui_PrefillDialog()
        self.ui.setupUi(self)
        self.setStyle()
        self.mapEvents()
        self.loadprefixjson()
        self.listDept()
        self.checkboxAtStart()

    def mapEvents(self):
        """Connect UI to methods."""
        self.ui.use_prefill_checkbox.clicked.connect(self.setEnabled)
        self.ui.apply_button.clicked.connect(self.returnAndApply)
        self.ui.cancel_button.clicked.connect(self.reject)

    def listDept(self):
        """Update the Department List."""
        departments = [
            d for d in os.listdir(self.prod_path)
            if os.path.isdir(os.path.join(self.prod_path, d))
        ]

        empty = True
        for key in self.data_prefix:
            if self.data_prefix[key] != '':
                empty = False

        for dep in departments:
            if (
                self.data_prefix == {} or
                dep not in self.data_prefix
                # MATHIAS not data[dep]
            ):
                dict_prefix = None
            else:
                dict_prefix = self.data_prefix[dep]

            # print "DICT_PREFIX IN LIST DEP", dict_prefix

            single_dept_layout = QtWidgets.QHBoxLayout()
            single_dept_layout.setObjectName("single_dept_layout")
            dept_label = QtWidgets.QLabel()
            dept_label.setMinimumSize(QtCore.QSize(120, 0))
            dept_label.setObjectName("dept_label")
            dept_label.setText(dep)
            single_dept_layout.addWidget(dept_label)
            dept_lineedit = QtWidgets.QLineEdit()
            dept_lineedit.setObjectName("dept_lineedit")
            single_dept_layout.addWidget(dept_lineedit)

            department = dep
            dep = dep.upper()
            dep = re.sub('[^a-zA-Z_]+', '', dep)
            dep = re.sub(r'\W+', '', dep)
            init_prefix = (dep)[:5]

            if dict_prefix is None or empty:
                dept_lineedit.setText(init_prefix)
            else:
                dept_lineedit.setText(dict_prefix)

            # Init the prefix dictionnary
            self.prefix_dict[department] = dept_lineedit.text()

            dept_lineedit.textChanged.connect(partial(
                self.formatText,
                line_edit=dept_lineedit,
                dept=department
            ))
            dept_edit_button = QtWidgets.QPushButton()
            dept_edit_button.setMinimumSize(QtCore.QSize(22, 22))
            dept_edit_button.setMaximumSize(QtCore.QSize(22, 22))
            dept_edit_button.setObjectName("dept_edit_button")
            load_icon(dept_edit_button, r'icons\reset.png')
            dept_edit_button.setIconSize(QtCore.QSize(16, 16))
            self.setStyleSheetButton(dept_edit_button)
            dept_edit_button.clicked.connect(partial(
                self.resetText,
                dept_lineedit,
                init_prefix
            ))
            single_dept_layout.addWidget(dept_edit_button)
            self.ui.dept_v_layout.addLayout(single_dept_layout)

    def loadprefixjson(self):
        """Load the prefix dictionnary."""
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

        if (
            not data or
            'prefix' not in data or
            not data['prefix']
        ):
            self.data_prefix = {}
        else:
            self.data_prefix = data['prefix']

    def checkboxAtStart(self):
        """Set the initial Use Prefill checkbox state."""
        empty = True
        for key in self.data_prefix:
            if self.data_prefix[key] != '':
                empty = False
        if empty:
            self.ui.use_prefill_checkbox.setChecked(False)
            self.ui.dept_widget.setHidden(True)
        else:
            self.ui.use_prefill_checkbox.setChecked(True)
            self.ui.dept_widget.setHidden(False)

    def setStyle(self):
        """Pimp the UI."""
        load_icon(self.ui.title_icon, r'icons\prefix.png')
        self.ui.title_icon.setIconSize(QtCore.QSize(16, 16))
        self.ui.title_icon.setStyleSheet("""
            background-color: #393939;
            border-radius: 15px;
        """)

    def setStyleSheetButton(self, button):
        """Change the shape and style of a given button."""
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

    def resetText(self, line_edit, text):
        """Reset text to default prefix."""
        line_edit.clear()
        line_edit.setText(text)

    def formatText(self, *args, **kwargs):
        """Change the user text to respect folder name conventions."""
        line_edit = kwargs['line_edit']
        dept = kwargs['dept']

        name = line_edit.text()
        name = re.sub('[^a-zA-Z_]+', '', name)
        name = re.sub(r'\W+', '', name)
        # name = formatText(name)
        line_edit.setText(name)
        self.prefix_dict[dept] = name

    def setEnabled(self):
        """Disable prefill options depending on checkbox."""
        state = self.ui.use_prefill_checkbox.isChecked()
        if state:
            self.ui.dept_widget.setHidden(False)
        else:
            self.ui.dept_widget.setHidden(True)

    def returnAndApply(self):
        """Return the prefix dictionnary."""
        state = self.ui.use_prefill_checkbox.isChecked()
        if not state:
            for key in self.prefix_dict:
                self.prefix_dict[key] = ''
        self.accept()
