# -*- coding: utf-8 -*-
"""
PySide compatibility layer for Maya 2020+
Automatically detects and imports the correct PySide version

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""

import sys
import maya.cmds as cmds

# Detect Maya version
maya_version = int(cmds.about(version=True))

# Import the appropriate PySide version
if maya_version >= 2025:
    # Maya 2025+ uses PySide6
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import QDoubleValidator

    import maya.OpenMayaUI as omui
    from shiboken6 import wrapInstance

    PYSIDE_VERSION = 6

else:
    # Maya 2017-2024 uses PySide2
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtCore import Signal, Slot
    from PySide2.QtGui import QDoubleValidator

    import maya.OpenMayaUI as omui
    from shiboken2 import wrapInstance

    PYSIDE_VERSION = 2


def get_maya_main_window():
    """
    Get Maya's main window as a Qt widget.
    Compatible with both PySide2 and PySide6.

    Returns:
        QWidget: Maya's main window widget or None
    """
    ptr = omui.MQtUtil.mainWindow()
    if ptr:
        return wrapInstance(int(ptr), QtWidgets.QWidget)
    return None


# Export commonly used classes for easy imports
__all__ = [
    'QtWidgets',
    'QtCore',
    'QtGui',
    'Signal',
    'Slot',
    'QDoubleValidator',
    'get_maya_main_window',
    'wrapInstance',
    'PYSIDE_VERSION'
]