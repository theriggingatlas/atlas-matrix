"""
Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
About: Create window for the Atlas Matrix Tool
"""

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui

from ui.script.main_ui import ui_window_main

def get_maya_main_window():
    """
    Get a reference to Maya's main window.

    Uses `shiboken6` and Maya's OpenMayaUI to wrap the pointer to Maya's main window
    so it can be used as a parent for custom Qt windows.

    Returns:
        QWidget: A wrapped instance of Maya's main window.
    """
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QWidget)


class AtlasMatrixWindow(QMainWindow):
    """
    Custom QMainWindow for the Atlas Matrix tool in Maya.

    This class ensures only one instance of the window exists at a time and sets up
    the user interface using the `ui_window_main` class. It connects UI signals
    and integrates cleanly into Maya's main window as its parent.
    """
    _instances = {}  # dict to track by class

    def __init__(self, parent=None):
        """
        Initialize the AtlasMatrixWindow.

        Args:
            parent (QWidget, optional): The parent widget. If None, Maya's main window is used.
        """
        super().__init__(parent or get_maya_main_window())
        self.setObjectName("AtlasMatrixWindow")
        self.setWindowTitle("Atlas Matrix")
        self.setWindowFlag(Qt.Window)

        self.ui = ui_window_main()
        self.ui.setupUi(self)

        self.setup_connections()

    def setup_connections(self):
        """
        Connect UI elements to their corresponding slots (functions).

        Currently connects the 'Close' button to the window's `close()` method.

        Returns:
            None
        """
        self.ui.button_parent_close.clicked.connect(self.close)

    @classmethod
    def show_window(cls):
        """
        Show the Atlas Matrix window.

        Ensures only one instance is open at a time. If an existing instance is
        found, it is closed and deleted before creating a new one.

        Returns:
            None
        """
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
