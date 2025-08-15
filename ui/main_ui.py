# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class ui_window_main(object):
    def setupUi(self, window_main):
        if not window_main.objectName():
            window_main.setObjectName(u"window_main")
        window_main.resize(694, 665)
        self.action_reset_preferences = QAction(window_main)
        self.action_reset_preferences.setObjectName(u"action_reset_preferences")
        self.action_help = QAction(window_main)
        self.action_help.setObjectName(u"action_help")
        self.action_the_rigging_atlas = QAction(window_main)
        self.action_the_rigging_atlas.setObjectName(u"action_the_rigging_atlas")
        self.action_contact = QAction(window_main)
        self.action_contact.setObjectName(u"action_contact")
        self.action_author = QAction(window_main)
        self.action_author.setObjectName(u"action_author")
        self.centralwidget = QWidget(window_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tab_main = QTabWidget(self.centralwidget)
        self.tab_main.setObjectName(u"tab_main")
        self.page_parent_con = QWidget()
        self.page_parent_con.setObjectName(u"page_parent_con")
        self.verticalLayout_2 = QVBoxLayout(self.page_parent_con)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticallayout_parent_global = QVBoxLayout()
        self.verticallayout_parent_global.setObjectName(u"verticallayout_parent_global")
        self.horizontallayout_parent_offset = QHBoxLayout()
        self.horizontallayout_parent_offset.setObjectName(u"horizontallayout_parent_offset")
        self.label_parent_offset = QLabel(self.page_parent_con)
        self.label_parent_offset.setObjectName(u"label_parent_offset")

        self.horizontallayout_parent_offset.addWidget(self.label_parent_offset)

        self.checkbox_parent_offset = QCheckBox(self.page_parent_con)
        self.checkbox_parent_offset.setObjectName(u"checkbox_parent_offset")
        self.checkbox_parent_offset.setChecked(False)

        self.horizontallayout_parent_offset.addWidget(self.checkbox_parent_offset)

        self.horizontallayout_parent_offset.setStretch(0, 1)
        self.horizontallayout_parent_offset.setStretch(1, 5)

        self.verticallayout_parent_global.addLayout(self.horizontallayout_parent_offset)

        self.horizontallayout_parent_hold = QHBoxLayout()
        self.horizontallayout_parent_hold.setObjectName(u"horizontallayout_parent_hold")
        self.label_parent_hold = QLabel(self.page_parent_con)
        self.label_parent_hold.setObjectName(u"label_parent_hold")

        self.horizontallayout_parent_hold.addWidget(self.label_parent_hold)

        self.checkbox_parent_hold = QCheckBox(self.page_parent_con)
        self.checkbox_parent_hold.setObjectName(u"checkbox_parent_hold")
        self.checkbox_parent_hold.setEnabled(False)
        self.checkbox_parent_hold.setChecked(False)

        self.horizontallayout_parent_hold.addWidget(self.checkbox_parent_hold)

        self.horizontallayout_parent_hold.setStretch(0, 1)
        self.horizontallayout_parent_hold.setStretch(1, 5)

        self.verticallayout_parent_global.addLayout(self.horizontallayout_parent_hold)

        self.separator_parent_00 = QFrame(self.page_parent_con)
        self.separator_parent_00.setObjectName(u"separator_parent_00")
        self.separator_parent_00.setFrameShape(QFrame.Shape.HLine)
        self.separator_parent_00.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticallayout_parent_global.addWidget(self.separator_parent_00)

        self.group_parent_constraint_axis = QGroupBox(self.page_parent_con)
        self.group_parent_constraint_axis.setObjectName(u"group_parent_constraint_axis")
        self.formLayout_2 = QFormLayout(self.group_parent_constraint_axis)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.form_parent_constraint_axis = QFormLayout()
        self.form_parent_constraint_axis.setObjectName(u"form_parent_constraint_axis")
        self.label_parent_translate_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_translate_axis.setObjectName(u"label_parent_translate_axis")

        self.form_parent_constraint_axis.setWidget(0, QFormLayout.LabelRole, self.label_parent_translate_axis)

        self.checkbox_parent_translate_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_all.setObjectName(u"checkbox_parent_translate_all")
        self.checkbox_parent_translate_all.setChecked(True)

        self.form_parent_constraint_axis.setWidget(0, QFormLayout.FieldRole, self.checkbox_parent_translate_all)

        self.horizontallayout_parent_translate_axis = QHBoxLayout()
        self.horizontallayout_parent_translate_axis.setObjectName(u"horizontallayout_parent_translate_axis")
        self.checkbox_parent_translate_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_x.setObjectName(u"checkbox_parent_translate_x")
        self.checkbox_parent_translate_x.setEnabled(False)
        self.checkbox_parent_translate_x.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_x)

        self.checkbox_parent_translate_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_y.setObjectName(u"checkbox_parent_translate_y")
        self.checkbox_parent_translate_y.setEnabled(False)
        self.checkbox_parent_translate_y.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_y)

        self.checkbox_parent_translate_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_z.setObjectName(u"checkbox_parent_translate_z")
        self.checkbox_parent_translate_z.setEnabled(False)
        self.checkbox_parent_translate_z.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_z)


        self.form_parent_constraint_axis.setLayout(1, QFormLayout.FieldRole, self.horizontallayout_parent_translate_axis)

        self.label_parent_translate_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_translate_weight.setObjectName(u"label_parent_translate_weight")

        self.form_parent_constraint_axis.setWidget(2, QFormLayout.LabelRole, self.label_parent_translate_weight)

        self.horizontallayout_parent_translate_weight = QHBoxLayout()
        self.horizontallayout_parent_translate_weight.setObjectName(u"horizontallayout_parent_translate_weight")
        self.lineedit_parent_translate_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_translate_weight.setObjectName(u"lineedit_parent_translate_weight")
        self.lineedit_parent_translate_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_translate_weight.addWidget(self.lineedit_parent_translate_weight)

        self.horizontalslider_parent_translate_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_translate_weight.setObjectName(u"horizontalslider_parent_translate_weight")
        self.horizontalslider_parent_translate_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_translate_weight.addWidget(self.horizontalslider_parent_translate_weight)

        self.horizontallayout_parent_translate_weight.setStretch(0, 1)
        self.horizontallayout_parent_translate_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(2, QFormLayout.FieldRole, self.horizontallayout_parent_translate_weight)

        self.separator_parent_01 = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_01.setObjectName(u"separator_parent_01")
        self.separator_parent_01.setFrameShape(QFrame.Shape.HLine)
        self.separator_parent_01.setFrameShadow(QFrame.Shadow.Sunken)

        self.form_parent_constraint_axis.setWidget(3, QFormLayout.FieldRole, self.separator_parent_01)

        self.label_parent_rotates_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_rotates_axis.setObjectName(u"label_parent_rotates_axis")

        self.form_parent_constraint_axis.setWidget(4, QFormLayout.LabelRole, self.label_parent_rotates_axis)

        self.checkbox_parent_rotate_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_all.setObjectName(u"checkbox_parent_rotate_all")
        self.checkbox_parent_rotate_all.setChecked(True)

        self.form_parent_constraint_axis.setWidget(4, QFormLayout.FieldRole, self.checkbox_parent_rotate_all)

        self.horizontallayout_parent_rotate_axis = QHBoxLayout()
        self.horizontallayout_parent_rotate_axis.setObjectName(u"horizontallayout_parent_rotate_axis")
        self.checkbox_parent_rotate_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_x.setObjectName(u"checkbox_parent_rotate_x")
        self.checkbox_parent_rotate_x.setEnabled(False)
        self.checkbox_parent_rotate_x.setCheckable(True)
        self.checkbox_parent_rotate_x.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_x)

        self.checkbox_parent_rotate_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_y.setObjectName(u"checkbox_parent_rotate_y")
        self.checkbox_parent_rotate_y.setEnabled(False)
        self.checkbox_parent_rotate_y.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_y)

        self.checkbox_parent_rotate_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_z.setObjectName(u"checkbox_parent_rotate_z")
        self.checkbox_parent_rotate_z.setEnabled(False)
        self.checkbox_parent_rotate_z.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_z)


        self.form_parent_constraint_axis.setLayout(5, QFormLayout.FieldRole, self.horizontallayout_parent_rotate_axis)

        self.label_parent_rotate_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_rotate_weight.setObjectName(u"label_parent_rotate_weight")

        self.form_parent_constraint_axis.setWidget(6, QFormLayout.LabelRole, self.label_parent_rotate_weight)

        self.horizontallayout_parent_rotate_weight = QHBoxLayout()
        self.horizontallayout_parent_rotate_weight.setObjectName(u"horizontallayout_parent_rotate_weight")
        self.lineedit_parent_rotate_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_rotate_weight.setObjectName(u"lineedit_parent_rotate_weight")
        self.lineedit_parent_rotate_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_rotate_weight.addWidget(self.lineedit_parent_rotate_weight)

        self.horizontalslider_parent_rotate_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_rotate_weight.setObjectName(u"horizontalslider_parent_rotate_weight")
        self.horizontalslider_parent_rotate_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_rotate_weight.addWidget(self.horizontalslider_parent_rotate_weight)

        self.horizontallayout_parent_rotate_weight.setStretch(0, 1)
        self.horizontallayout_parent_rotate_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(6, QFormLayout.FieldRole, self.horizontallayout_parent_rotate_weight)

        self.separator_parent_02 = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_02.setObjectName(u"separator_parent_02")
        self.separator_parent_02.setFrameShape(QFrame.Shape.HLine)
        self.separator_parent_02.setFrameShadow(QFrame.Shadow.Sunken)

        self.form_parent_constraint_axis.setWidget(7, QFormLayout.FieldRole, self.separator_parent_02)

        self.label_parent_scale_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_scale_axis.setObjectName(u"label_parent_scale_axis")

        self.form_parent_constraint_axis.setWidget(8, QFormLayout.LabelRole, self.label_parent_scale_axis)

        self.checkbox_parent_scale_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_all.setObjectName(u"checkbox_parent_scale_all")
        self.checkbox_parent_scale_all.setChecked(True)

        self.form_parent_constraint_axis.setWidget(8, QFormLayout.FieldRole, self.checkbox_parent_scale_all)

        self.checkbox_parent_scale_axis = QHBoxLayout()
        self.checkbox_parent_scale_axis.setObjectName(u"checkbox_parent_scale_axis")
        self.checkbox_parent_scale_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_x.setObjectName(u"checkbox_parent_scale_x")
        self.checkbox_parent_scale_x.setEnabled(False)
        self.checkbox_parent_scale_x.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_x)

        self.checkbox_parent_scale_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_y.setObjectName(u"checkbox_parent_scale_y")
        self.checkbox_parent_scale_y.setEnabled(False)
        self.checkbox_parent_scale_y.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_y)

        self.checkbox_parent_scale_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_z.setObjectName(u"checkbox_parent_scale_z")
        self.checkbox_parent_scale_z.setEnabled(False)
        self.checkbox_parent_scale_z.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_z)


        self.form_parent_constraint_axis.setLayout(9, QFormLayout.FieldRole, self.checkbox_parent_scale_axis)

        self.label_parent_scale_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_scale_weight.setObjectName(u"label_parent_scale_weight")

        self.form_parent_constraint_axis.setWidget(10, QFormLayout.LabelRole, self.label_parent_scale_weight)

        self.horizontallayout_parent_scale_weight = QHBoxLayout()
        self.horizontallayout_parent_scale_weight.setObjectName(u"horizontallayout_parent_scale_weight")
        self.lineedit_parent_scale_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_scale_weight.setObjectName(u"lineedit_parent_scale_weight")
        self.lineedit_parent_scale_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_scale_weight.addWidget(self.lineedit_parent_scale_weight)

        self.horizontalslider_parent_scale_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_scale_weight.setObjectName(u"horizontalslider_parent_scale_weight")
        self.horizontalslider_parent_scale_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_scale_weight.addWidget(self.horizontalslider_parent_scale_weight)

        self.horizontallayout_parent_scale_weight.setStretch(0, 1)
        self.horizontallayout_parent_scale_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(10, QFormLayout.FieldRole, self.horizontallayout_parent_scale_weight)

        self.checkbox_parent_shear_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_all.setObjectName(u"checkbox_parent_shear_all")
        self.checkbox_parent_shear_all.setChecked(True)

        self.form_parent_constraint_axis.setWidget(12, QFormLayout.FieldRole, self.checkbox_parent_shear_all)

        self.separator_parent_03 = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_03.setObjectName(u"separator_parent_03")
        self.separator_parent_03.setFrameShape(QFrame.Shape.HLine)
        self.separator_parent_03.setFrameShadow(QFrame.Shadow.Sunken)

        self.form_parent_constraint_axis.setWidget(11, QFormLayout.FieldRole, self.separator_parent_03)

        self.label_parent_shear_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_shear_weight.setObjectName(u"label_parent_shear_weight")

        self.form_parent_constraint_axis.setWidget(14, QFormLayout.LabelRole, self.label_parent_shear_weight)

        self.horizontallayout_parent_shear_weight = QHBoxLayout()
        self.horizontallayout_parent_shear_weight.setObjectName(u"horizontallayout_parent_shear_weight")
        self.lineedit_parent_scale_shear_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_scale_shear_weight.setObjectName(u"lineedit_parent_scale_shear_weight")
        self.lineedit_parent_scale_shear_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_shear_weight.addWidget(self.lineedit_parent_scale_shear_weight)

        self.horizontalslider_parent_shear_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_shear_weight.setObjectName(u"horizontalslider_parent_shear_weight")
        self.horizontalslider_parent_shear_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_shear_weight.addWidget(self.horizontalslider_parent_shear_weight)

        self.horizontallayout_parent_shear_weight.setStretch(0, 1)
        self.horizontallayout_parent_shear_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(14, QFormLayout.FieldRole, self.horizontallayout_parent_shear_weight)

        self.checkbox_parent_shear_axis = QHBoxLayout()
        self.checkbox_parent_shear_axis.setObjectName(u"checkbox_parent_shear_axis")
        self.checkbox_parent_shear_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_x.setObjectName(u"checkbox_parent_shear_x")
        self.checkbox_parent_shear_x.setEnabled(False)
        self.checkbox_parent_shear_x.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_x)

        self.checkbox_parent_shear_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_y.setObjectName(u"checkbox_parent_shear_y")
        self.checkbox_parent_shear_y.setEnabled(False)
        self.checkbox_parent_shear_y.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_y)

        self.checkbox_parent_shear_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_z.setObjectName(u"checkbox_parent_shear_z")
        self.checkbox_parent_shear_z.setEnabled(False)
        self.checkbox_parent_shear_z.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_z)


        self.form_parent_constraint_axis.setLayout(13, QFormLayout.FieldRole, self.checkbox_parent_shear_axis)

        self.label_parent_shear_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_shear_axis.setObjectName(u"label_parent_shear_axis")

        self.form_parent_constraint_axis.setWidget(12, QFormLayout.LabelRole, self.label_parent_shear_axis)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.form_parent_constraint_axis)


        self.verticallayout_parent_global.addWidget(self.group_parent_constraint_axis)

        self.horizontallayout_parent_dialog = QHBoxLayout()
        self.horizontallayout_parent_dialog.setObjectName(u"horizontallayout_parent_dialog")
        self.button_parent_add = QPushButton(self.page_parent_con)
        self.button_parent_add.setObjectName(u"button_parent_add")

        self.horizontallayout_parent_dialog.addWidget(self.button_parent_add)

        self.button_parent_apply = QPushButton(self.page_parent_con)
        self.button_parent_apply.setObjectName(u"button_parent_apply")

        self.horizontallayout_parent_dialog.addWidget(self.button_parent_apply)

        self.button_parent_close = QPushButton(self.page_parent_con)
        self.button_parent_close.setObjectName(u"button_parent_close")

        self.horizontallayout_parent_dialog.addWidget(self.button_parent_close)


        self.verticallayout_parent_global.addLayout(self.horizontallayout_parent_dialog)

        self.verticallayout_parent_global.setStretch(0, 1)
        self.verticallayout_parent_global.setStretch(2, 1)
        self.verticallayout_parent_global.setStretch(3, 25)

        self.verticalLayout_2.addLayout(self.verticallayout_parent_global)

        self.tab_main.addTab(self.page_parent_con, "")
        self.page_aim_con = QWidget()
        self.page_aim_con.setObjectName(u"page_aim_con")
        self.verticalLayout_4 = QVBoxLayout(self.page_aim_con)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticallayout_aim_global = QVBoxLayout()
        self.verticallayout_aim_global.setObjectName(u"verticallayout_aim_global")
        self.horizontallayout_aim_offset = QHBoxLayout()
        self.horizontallayout_aim_offset.setObjectName(u"horizontallayout_aim_offset")
        self.label_aim_offset = QLabel(self.page_aim_con)
        self.label_aim_offset.setObjectName(u"label_aim_offset")

        self.horizontallayout_aim_offset.addWidget(self.label_aim_offset)

        self.checkbox_aim_offset = QCheckBox(self.page_aim_con)
        self.checkbox_aim_offset.setObjectName(u"checkbox_aim_offset")

        self.horizontallayout_aim_offset.addWidget(self.checkbox_aim_offset)

        self.horizontallayout_aim_offset.setStretch(0, 1)
        self.horizontallayout_aim_offset.setStretch(1, 5)

        self.verticallayout_aim_global.addLayout(self.horizontallayout_aim_offset)

        self.horizontallayout_aim_hold = QHBoxLayout()
        self.horizontallayout_aim_hold.setObjectName(u"horizontallayout_aim_hold")
        self.label_aim_hold = QLabel(self.page_aim_con)
        self.label_aim_hold.setObjectName(u"label_aim_hold")

        self.horizontallayout_aim_hold.addWidget(self.label_aim_hold)

        self.checkbox_aim_hold = QCheckBox(self.page_aim_con)
        self.checkbox_aim_hold.setObjectName(u"checkbox_aim_hold")
        self.checkbox_aim_hold.setEnabled(False)
        self.checkbox_aim_hold.setChecked(False)

        self.horizontallayout_aim_hold.addWidget(self.checkbox_aim_hold)

        self.horizontallayout_aim_hold.setStretch(0, 1)
        self.horizontallayout_aim_hold.setStretch(1, 5)

        self.verticallayout_aim_global.addLayout(self.horizontallayout_aim_hold)

        self.separator_aim_01 = QFrame(self.page_aim_con)
        self.separator_aim_01.setObjectName(u"separator_aim_01")
        self.separator_aim_01.setFrameShape(QFrame.Shape.HLine)
        self.separator_aim_01.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticallayout_aim_global.addWidget(self.separator_aim_01)

        self.group_aim_primary = QGroupBox(self.page_aim_con)
        self.group_aim_primary.setObjectName(u"group_aim_primary")
        self.formLayout_6 = QFormLayout(self.group_aim_primary)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.form_aim_primary = QFormLayout()
        self.form_aim_primary.setObjectName(u"form_aim_primary")
        self.label_primary_aim_vector = QLabel(self.group_aim_primary)
        self.label_primary_aim_vector.setObjectName(u"label_primary_aim_vector")

        self.form_aim_primary.setWidget(0, QFormLayout.LabelRole, self.label_primary_aim_vector)

        self.horizontallayout_primary_aim_vector = QHBoxLayout()
        self.horizontallayout_primary_aim_vector.setObjectName(u"horizontallayout_primary_aim_vector")
        self.lineedit_primary_aim_vector_x = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_aim_vector_x.setObjectName(u"lineedit_primary_aim_vector_x")

        self.horizontallayout_primary_aim_vector.addWidget(self.lineedit_primary_aim_vector_x)

        self.lineedit_primary_aim_vector_y = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_aim_vector_y.setObjectName(u"lineedit_primary_aim_vector_y")

        self.horizontallayout_primary_aim_vector.addWidget(self.lineedit_primary_aim_vector_y)

        self.lineedit_primary_aim_vector_z = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_aim_vector_z.setObjectName(u"lineedit_primary_aim_vector_z")

        self.horizontallayout_primary_aim_vector.addWidget(self.lineedit_primary_aim_vector_z)


        self.form_aim_primary.setLayout(0, QFormLayout.FieldRole, self.horizontallayout_primary_aim_vector)

        self.label_primary_vector_mode = QLabel(self.group_aim_primary)
        self.label_primary_vector_mode.setObjectName(u"label_primary_vector_mode")

        self.form_aim_primary.setWidget(1, QFormLayout.LabelRole, self.label_primary_vector_mode)

        self.label_primary_target_vector = QLabel(self.group_aim_primary)
        self.label_primary_target_vector.setObjectName(u"label_primary_target_vector")

        self.form_aim_primary.setWidget(2, QFormLayout.LabelRole, self.label_primary_target_vector)

        self.combobox_primary_vector_mode = QComboBox(self.group_aim_primary)
        self.combobox_primary_vector_mode.addItem("")
        self.combobox_primary_vector_mode.addItem("")
        self.combobox_primary_vector_mode.addItem("")
        self.combobox_primary_vector_mode.setObjectName(u"combobox_primary_vector_mode")

        self.form_aim_primary.setWidget(1, QFormLayout.FieldRole, self.combobox_primary_vector_mode)

        self.horizontallayout_primary_target_vector = QHBoxLayout()
        self.horizontallayout_primary_target_vector.setObjectName(u"horizontallayout_primary_target_vector")
        self.lineedit_primary_target_vector_x = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_target_vector_x.setObjectName(u"lineedit_primary_target_vector_x")

        self.horizontallayout_primary_target_vector.addWidget(self.lineedit_primary_target_vector_x)

        self.lineedit_primary_target_vector_y = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_target_vector_y.setObjectName(u"lineedit_primary_target_vector_y")

        self.horizontallayout_primary_target_vector.addWidget(self.lineedit_primary_target_vector_y)

        self.lineedit_primary_target_vector_z = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_target_vector_z.setObjectName(u"lineedit_primary_target_vector_z")

        self.horizontallayout_primary_target_vector.addWidget(self.lineedit_primary_target_vector_z)


        self.form_aim_primary.setLayout(2, QFormLayout.FieldRole, self.horizontallayout_primary_target_vector)


        self.formLayout_6.setLayout(0, QFormLayout.FieldRole, self.form_aim_primary)


        self.verticallayout_aim_global.addWidget(self.group_aim_primary)

        self.separator_aim_02 = QFrame(self.page_aim_con)
        self.separator_aim_02.setObjectName(u"separator_aim_02")
        self.separator_aim_02.setFrameShape(QFrame.Shape.HLine)
        self.separator_aim_02.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticallayout_aim_global.addWidget(self.separator_aim_02)

        self.group_aim_secondary = QGroupBox(self.page_aim_con)
        self.group_aim_secondary.setObjectName(u"group_aim_secondary")
        self.formLayout_5 = QFormLayout(self.group_aim_secondary)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.form_aim_secondary = QFormLayout()
        self.form_aim_secondary.setObjectName(u"form_aim_secondary")
        self.label_secondary_up_vector = QLabel(self.group_aim_secondary)
        self.label_secondary_up_vector.setObjectName(u"label_secondary_up_vector")

        self.form_aim_secondary.setWidget(0, QFormLayout.LabelRole, self.label_secondary_up_vector)

        self.horizontallayout_secondary_up_vector = QHBoxLayout()
        self.horizontallayout_secondary_up_vector.setObjectName(u"horizontallayout_secondary_up_vector")
        self.lineedit_secondary_up_vector_x = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_up_vector_x.setObjectName(u"lineedit_secondary_up_vector_x")

        self.horizontallayout_secondary_up_vector.addWidget(self.lineedit_secondary_up_vector_x)

        self.lineedit_secondary_up_vector_y = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_up_vector_y.setObjectName(u"lineedit_secondary_up_vector_y")

        self.horizontallayout_secondary_up_vector.addWidget(self.lineedit_secondary_up_vector_y)

        self.lineedit_secondary_up_vector_z = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_up_vector_z.setObjectName(u"lineedit_secondary_up_vector_z")

        self.horizontallayout_secondary_up_vector.addWidget(self.lineedit_secondary_up_vector_z)


        self.form_aim_secondary.setLayout(0, QFormLayout.FieldRole, self.horizontallayout_secondary_up_vector)

        self.combobox_secondary_vector_mode = QComboBox(self.group_aim_secondary)
        self.combobox_secondary_vector_mode.addItem("")
        self.combobox_secondary_vector_mode.addItem("")
        self.combobox_secondary_vector_mode.addItem("")
        self.combobox_secondary_vector_mode.setObjectName(u"combobox_secondary_vector_mode")

        self.form_aim_secondary.setWidget(1, QFormLayout.FieldRole, self.combobox_secondary_vector_mode)

        self.label_secondary_vector_mode = QLabel(self.group_aim_secondary)
        self.label_secondary_vector_mode.setObjectName(u"label_secondary_vector_mode")

        self.form_aim_secondary.setWidget(1, QFormLayout.LabelRole, self.label_secondary_vector_mode)

        self.horizontallayout_secondary_target_vector = QHBoxLayout()
        self.horizontallayout_secondary_target_vector.setObjectName(u"horizontallayout_secondary_target_vector")
        self.lineedit_secondary_target_vector_x = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_target_vector_x.setObjectName(u"lineedit_secondary_target_vector_x")

        self.horizontallayout_secondary_target_vector.addWidget(self.lineedit_secondary_target_vector_x)

        self.lineedit_secondary_target_vector_y = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_target_vector_y.setObjectName(u"lineedit_secondary_target_vector_y")

        self.horizontallayout_secondary_target_vector.addWidget(self.lineedit_secondary_target_vector_y)

        self.lineedit_secondary_target_vector_z = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_target_vector_z.setObjectName(u"lineedit_secondary_target_vector_z")

        self.horizontallayout_secondary_target_vector.addWidget(self.lineedit_secondary_target_vector_z)


        self.form_aim_secondary.setLayout(2, QFormLayout.FieldRole, self.horizontallayout_secondary_target_vector)

        self.label_secondary_target_mode = QLabel(self.group_aim_secondary)
        self.label_secondary_target_mode.setObjectName(u"label_secondary_target_mode")

        self.form_aim_secondary.setWidget(2, QFormLayout.LabelRole, self.label_secondary_target_mode)

        self.combobox_secondary_world_up_type = QComboBox(self.group_aim_secondary)
        self.combobox_secondary_world_up_type.addItem("")
        self.combobox_secondary_world_up_type.addItem("")
        self.combobox_secondary_world_up_type.addItem("")
        self.combobox_secondary_world_up_type.setObjectName(u"combobox_secondary_world_up_type")

        self.form_aim_secondary.setWidget(3, QFormLayout.FieldRole, self.combobox_secondary_world_up_type)

        self.lineedit_secondary_world_up_obj = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_world_up_obj.setObjectName(u"lineedit_secondary_world_up_obj")

        self.form_aim_secondary.setWidget(4, QFormLayout.FieldRole, self.lineedit_secondary_world_up_obj)

        self.label_secondary_world_up_type = QLabel(self.group_aim_secondary)
        self.label_secondary_world_up_type.setObjectName(u"label_secondary_world_up_type")

        self.form_aim_secondary.setWidget(3, QFormLayout.LabelRole, self.label_secondary_world_up_type)

        self.label_secondary_world_up_obj = QLabel(self.group_aim_secondary)
        self.label_secondary_world_up_obj.setObjectName(u"label_secondary_world_up_obj")

        self.form_aim_secondary.setWidget(4, QFormLayout.LabelRole, self.label_secondary_world_up_obj)


        self.formLayout_5.setLayout(0, QFormLayout.FieldRole, self.form_aim_secondary)


        self.verticallayout_aim_global.addWidget(self.group_aim_secondary)


        self.verticalLayout_4.addLayout(self.verticallayout_aim_global)

        self.horizontallayout_aim_dialog = QHBoxLayout()
        self.horizontallayout_aim_dialog.setObjectName(u"horizontallayout_aim_dialog")
        self.button_aim_add = QPushButton(self.page_aim_con)
        self.button_aim_add.setObjectName(u"button_aim_add")

        self.horizontallayout_aim_dialog.addWidget(self.button_aim_add)

        self.button_aim_apply = QPushButton(self.page_aim_con)
        self.button_aim_apply.setObjectName(u"button_aim_apply")

        self.horizontallayout_aim_dialog.addWidget(self.button_aim_apply)

        self.button_aim_close = QPushButton(self.page_aim_con)
        self.button_aim_close.setObjectName(u"button_aim_close")

        self.horizontallayout_aim_dialog.addWidget(self.button_aim_close)


        self.verticalLayout_4.addLayout(self.horizontallayout_aim_dialog)

        self.tab_main.addTab(self.page_aim_con, "")
        self.manager_con_page = QWidget()
        self.manager_con_page.setObjectName(u"manager_con_page")
        self.tab_main.addTab(self.manager_con_page, "")

        self.horizontalLayout.addWidget(self.tab_main)

        window_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(window_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 694, 23))
        self.menu_atlas = QMenu(self.menubar)
        self.menu_atlas.setObjectName(u"menu_atlas")
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        window_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(window_main)
        self.statusbar.setObjectName(u"statusbar")
        window_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_atlas.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_atlas.addAction(self.action_the_rigging_atlas)
        self.menu_atlas.addAction(self.action_author)
        self.menu_atlas.addAction(self.action_contact)
        self.menu_edit.addAction(self.action_reset_preferences)
        self.menu_help.addAction(self.action_help)

        self.retranslateUi(window_main)
        self.checkbox_parent_translate_all.toggled.connect(self.checkbox_parent_translate_x.setDisabled)
        self.checkbox_parent_translate_all.toggled.connect(self.checkbox_parent_translate_y.setDisabled)
        self.checkbox_parent_translate_all.toggled.connect(self.checkbox_parent_translate_z.setDisabled)
        self.checkbox_parent_rotate_all.clicked["bool"].connect(self.checkbox_parent_rotate_x.setDisabled)
        self.checkbox_parent_rotate_all.toggled.connect(self.checkbox_parent_rotate_y.setDisabled)
        self.checkbox_parent_rotate_all.toggled.connect(self.checkbox_parent_rotate_z.setDisabled)
        self.checkbox_parent_scale_all.toggled.connect(self.checkbox_parent_scale_x.setDisabled)
        self.checkbox_parent_scale_all.toggled.connect(self.checkbox_parent_scale_y.setDisabled)
        self.checkbox_parent_scale_all.toggled.connect(self.checkbox_parent_scale_z.setDisabled)
        self.checkbox_parent_translate_all.toggled.connect(self.checkbox_parent_translate_x.setChecked)
        self.checkbox_parent_translate_all.toggled.connect(self.checkbox_parent_translate_y.setChecked)
        self.checkbox_parent_translate_all.toggled.connect(self.checkbox_parent_translate_z.setChecked)
        self.checkbox_parent_rotate_all.toggled.connect(self.checkbox_parent_rotate_x.setChecked)
        self.checkbox_parent_rotate_all.toggled.connect(self.checkbox_parent_rotate_y.setChecked)
        self.checkbox_parent_rotate_all.toggled.connect(self.checkbox_parent_rotate_z.setChecked)
        self.checkbox_parent_scale_all.toggled.connect(self.checkbox_parent_scale_x.setChecked)
        self.checkbox_parent_scale_all.toggled.connect(self.checkbox_parent_scale_y.setChecked)
        self.checkbox_parent_scale_all.toggled.connect(self.checkbox_parent_scale_z.setChecked)
        self.checkbox_parent_offset.toggled.connect(self.checkbox_parent_hold.setEnabled)
        self.checkbox_parent_offset.toggled.connect(self.checkbox_parent_hold.setChecked)
        self.checkbox_aim_offset.toggled.connect(self.checkbox_aim_hold.setChecked)
        self.checkbox_aim_offset.toggled.connect(self.checkbox_aim_hold.setEnabled)

        self.tab_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(window_main)
    # setupUi

    def retranslateUi(self, window_main):
        window_main.setWindowTitle(QCoreApplication.translate("window_main", u"Atlas Matrix - V.1.0.0", None))
        self.action_reset_preferences.setText(QCoreApplication.translate("window_main", u"Reset Preferences", None))
        self.action_help.setText(QCoreApplication.translate("window_main", u"Help", None))
        self.action_the_rigging_atlas.setText(QCoreApplication.translate("window_main", u"Atlas Matrix by @theriggingatlas", None))
        self.action_contact.setText(QCoreApplication.translate("window_main", u"Contact : clementdaures.contact@gmail.com", None))
        self.action_author.setText(QCoreApplication.translate("window_main", u"Author : Clement Daures - 2025 - V.1.0.0", None))
        self.label_parent_offset.setText(QCoreApplication.translate("window_main", u"Maintain offset:", None))
        self.checkbox_parent_offset.setText("")
        self.label_parent_hold.setText(QCoreApplication.translate("window_main", u"Keep hold:", None))
        self.checkbox_parent_hold.setText("")
        self.group_parent_constraint_axis.setTitle(QCoreApplication.translate("window_main", u"Constraint axes:", None))
        self.label_parent_translate_axis.setText(QCoreApplication.translate("window_main", u"Translate:", None))
        self.checkbox_parent_translate_all.setText(QCoreApplication.translate("window_main", u"All", None))
        self.checkbox_parent_translate_x.setText(QCoreApplication.translate("window_main", u"X", None))
        self.checkbox_parent_translate_y.setText(QCoreApplication.translate("window_main", u"Y", None))
        self.checkbox_parent_translate_z.setText(QCoreApplication.translate("window_main", u"Z", None))
        self.label_parent_translate_weight.setText(QCoreApplication.translate("window_main", u"Weight:", None))
        self.lineedit_parent_translate_weight.setText(QCoreApplication.translate("window_main", u"0.500", None))
        self.label_parent_rotates_axis.setText(QCoreApplication.translate("window_main", u"Rotate:", None))
        self.checkbox_parent_rotate_all.setText(QCoreApplication.translate("window_main", u"All", None))
        self.checkbox_parent_rotate_x.setText(QCoreApplication.translate("window_main", u"X", None))
        self.checkbox_parent_rotate_y.setText(QCoreApplication.translate("window_main", u"Y", None))
        self.checkbox_parent_rotate_z.setText(QCoreApplication.translate("window_main", u"Z", None))
        self.label_parent_rotate_weight.setText(QCoreApplication.translate("window_main", u"Weight:", None))
        self.lineedit_parent_rotate_weight.setText(QCoreApplication.translate("window_main", u"0.500", None))
        self.label_parent_scale_axis.setText(QCoreApplication.translate("window_main", u"Scale:", None))
        self.checkbox_parent_scale_all.setText(QCoreApplication.translate("window_main", u"All", None))
        self.checkbox_parent_scale_x.setText(QCoreApplication.translate("window_main", u"X", None))
        self.checkbox_parent_scale_y.setText(QCoreApplication.translate("window_main", u"Y", None))
        self.checkbox_parent_scale_z.setText(QCoreApplication.translate("window_main", u"Z", None))
        self.label_parent_scale_weight.setText(QCoreApplication.translate("window_main", u"Weight:", None))
        self.lineedit_parent_scale_weight.setText(QCoreApplication.translate("window_main", u"0.500", None))
        self.checkbox_parent_shear_all.setText(QCoreApplication.translate("window_main", u"All", None))
        self.label_parent_shear_weight.setText(QCoreApplication.translate("window_main", u"Weight:", None))
        self.lineedit_parent_scale_shear_weight.setText(QCoreApplication.translate("window_main", u"0.500", None))
        self.checkbox_parent_shear_x.setText(QCoreApplication.translate("window_main", u"X", None))
        self.checkbox_parent_shear_y.setText(QCoreApplication.translate("window_main", u"Y", None))
        self.checkbox_parent_shear_z.setText(QCoreApplication.translate("window_main", u"Z", None))
        self.label_parent_shear_axis.setText(QCoreApplication.translate("window_main", u"Shear:", None))
        self.button_parent_add.setText(QCoreApplication.translate("window_main", u"Add", None))
        self.button_parent_apply.setText(QCoreApplication.translate("window_main", u"Apply", None))
        self.button_parent_close.setText(QCoreApplication.translate("window_main", u"Close", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.page_parent_con), QCoreApplication.translate("window_main", u"Parent", None))
        self.label_aim_offset.setText(QCoreApplication.translate("window_main", u"Maintain offset:", None))
        self.checkbox_aim_offset.setText("")
        self.label_aim_hold.setText(QCoreApplication.translate("window_main", u"Keep hold:", None))
        self.checkbox_aim_hold.setText("")
        self.group_aim_primary.setTitle(QCoreApplication.translate("window_main", u"Primary axis:", None))
        self.label_primary_aim_vector.setText(QCoreApplication.translate("window_main", u"Aim vector:", None))
        self.lineedit_primary_aim_vector_x.setText(QCoreApplication.translate("window_main", u"1.000", None))
        self.lineedit_primary_aim_vector_y.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.lineedit_primary_aim_vector_z.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.label_primary_vector_mode.setText(QCoreApplication.translate("window_main", u"Vector mode:", None))
        self.label_primary_target_vector.setText(QCoreApplication.translate("window_main", u"Target vector:", None))
        self.combobox_primary_vector_mode.setItemText(0, QCoreApplication.translate("window_main", u"Aim", None))
        self.combobox_primary_vector_mode.setItemText(1, QCoreApplication.translate("window_main", u"Lock Axis", None))
        self.combobox_primary_vector_mode.setItemText(2, QCoreApplication.translate("window_main", u"Align", None))

        self.lineedit_primary_target_vector_x.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.lineedit_primary_target_vector_y.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.lineedit_primary_target_vector_z.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.group_aim_secondary.setTitle(QCoreApplication.translate("window_main", u"Secondary axis:", None))
        self.label_secondary_up_vector.setText(QCoreApplication.translate("window_main", u"Up vector:", None))
        self.lineedit_secondary_up_vector_x.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.lineedit_secondary_up_vector_y.setText(QCoreApplication.translate("window_main", u"1.000", None))
        self.lineedit_secondary_up_vector_z.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.combobox_secondary_vector_mode.setItemText(0, QCoreApplication.translate("window_main", u"Aim", None))
        self.combobox_secondary_vector_mode.setItemText(1, QCoreApplication.translate("window_main", u"Align", None))
        self.combobox_secondary_vector_mode.setItemText(2, QCoreApplication.translate("window_main", u"None", None))

        self.label_secondary_vector_mode.setText(QCoreApplication.translate("window_main", u"Vector mode:", None))
        self.lineedit_secondary_target_vector_x.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.lineedit_secondary_target_vector_y.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.lineedit_secondary_target_vector_z.setText(QCoreApplication.translate("window_main", u"0.000", None))
        self.label_secondary_target_mode.setText(QCoreApplication.translate("window_main", u"Target  vector :", None))
        self.combobox_secondary_world_up_type.setItemText(0, QCoreApplication.translate("window_main", u"Constrained Up", None))
        self.combobox_secondary_world_up_type.setItemText(1, QCoreApplication.translate("window_main", u"Object Up", None))
        self.combobox_secondary_world_up_type.setItemText(2, QCoreApplication.translate("window_main", u"None", None))

        self.label_secondary_world_up_type.setText(QCoreApplication.translate("window_main", u"World up type:", None))
        self.label_secondary_world_up_obj.setText(QCoreApplication.translate("window_main", u"World up obj:", None))
        self.button_aim_add.setText(QCoreApplication.translate("window_main", u"Add", None))
        self.button_aim_apply.setText(QCoreApplication.translate("window_main", u"Apply", None))
        self.button_aim_close.setText(QCoreApplication.translate("window_main", u"Close", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.page_aim_con), QCoreApplication.translate("window_main", u"Aim", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.manager_con_page), QCoreApplication.translate("window_main", u"Manager", None))
        self.menu_atlas.setTitle(QCoreApplication.translate("window_main", u"Atlas", None))
        self.menu_edit.setTitle(QCoreApplication.translate("window_main", u"Edit", None))
        self.menu_help.setTitle(QCoreApplication.translate("window_main", u"Help", None))
