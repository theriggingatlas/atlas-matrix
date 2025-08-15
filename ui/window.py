from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui

from main_ui import ui_window_main

def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QWidget)


class AtlasMatrixWindow(QMainWindow):
    _instances = {}  # dict to track by class

    def __init__(self, parent=None):
        super().__init__(parent or get_maya_main_window())
        self.setObjectName("AtlasMatrixWindow")
        self.setWindowTitle("Atlas Matrix")
        self.setWindowFlag(Qt.Window)

        self.ui = ui_window_main()
        self.ui.setupUi(self)

        self.setup_connections()

    def setup_connections(self):
        self.ui.button_parent_close.clicked.connect(self.close)

    @classmethod
    def show_window(cls):
        # Close any existing instance
        if cls in cls._instances and cls._instances[cls] is not None:
            instance = cls._instances[cls]
            if instance.isVisible():
                instance.close()
                instance.deleteLater()

        # Create new instance
        window = cls()
        cls._instances[cls] = window
        window.show()
        window.raise_()
        window.activateWindow()
