# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'atlas_matrix_aim.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_atlas_matrix_aim(object):
    def setupUi(self, atlas_matrix_aim):
        if not atlas_matrix_aim.objectName():
            atlas_matrix_aim.setObjectName(u"atlas_matrix_aim")
        atlas_matrix_aim.resize(774, 347)
        self.verticalLayout = QVBoxLayout(atlas_matrix_aim)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_8.addItem(self.verticalSpacer)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontallayout_aim_offset = QHBoxLayout()
        self.horizontallayout_aim_offset.setObjectName(u"horizontallayout_aim_offset")
        self.label_aim_offset = QLabel(atlas_matrix_aim)
        self.label_aim_offset.setObjectName(u"label_aim_offset")

        self.horizontallayout_aim_offset.addWidget(self.label_aim_offset)

        self.checkbox_aim_offset = QCheckBox(atlas_matrix_aim)
        self.checkbox_aim_offset.setObjectName(u"checkbox_aim_offset")

        self.horizontallayout_aim_offset.addWidget(self.checkbox_aim_offset)


        self.horizontalLayout_7.addLayout(self.horizontallayout_aim_offset)

        self.horizontallayout_aim_hold = QHBoxLayout()
        self.horizontallayout_aim_hold.setObjectName(u"horizontallayout_aim_hold")
        self.label_aim_hold = QLabel(atlas_matrix_aim)
        self.label_aim_hold.setObjectName(u"label_aim_hold")

        self.horizontallayout_aim_hold.addWidget(self.label_aim_hold)

        self.checkbox_aim_hold = QCheckBox(atlas_matrix_aim)
        self.checkbox_aim_hold.setObjectName(u"checkbox_aim_hold")
        self.checkbox_aim_hold.setEnabled(False)
        self.checkbox_aim_hold.setChecked(False)

        self.horizontallayout_aim_hold.addWidget(self.checkbox_aim_hold)


        self.horizontalLayout_7.addLayout(self.horizontallayout_aim_hold)

        self.horizontallayout_aim_enveloppe = QHBoxLayout()
        self.horizontallayout_aim_enveloppe.setObjectName(u"horizontallayout_aim_enveloppe")
        self.label_aim_enveloppe = QLabel(atlas_matrix_aim)
        self.label_aim_enveloppe.setObjectName(u"label_aim_enveloppe")

        self.horizontallayout_aim_enveloppe.addWidget(self.label_aim_enveloppe)

        self.checkbox_aim_enveloppe = QCheckBox(atlas_matrix_aim)
        self.checkbox_aim_enveloppe.setObjectName(u"checkbox_aim_enveloppe")
        self.checkbox_aim_enveloppe.setChecked(True)

        self.horizontallayout_aim_enveloppe.addWidget(self.checkbox_aim_enveloppe)


        self.horizontalLayout_7.addLayout(self.horizontallayout_aim_enveloppe)


        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8.setStretch(1, 80)

        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticallayout_aim_global = QVBoxLayout()
        self.verticallayout_aim_global.setObjectName(u"verticallayout_aim_global")
        self.separator_aim_01 = QFrame(atlas_matrix_aim)
        self.separator_aim_01.setObjectName(u"separator_aim_01")
        self.separator_aim_01.setFrameShape(QFrame.Shape.HLine)
        self.separator_aim_01.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticallayout_aim_global.addWidget(self.separator_aim_01)

        self.group_aim_primary = QGroupBox(atlas_matrix_aim)
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
        self.combobox_primary_vector_mode = QComboBox(self.group_aim_primary)
        self.combobox_primary_vector_mode.addItem("")
        self.combobox_primary_vector_mode.addItem("")
        self.combobox_primary_vector_mode.addItem("")
        self.combobox_primary_vector_mode.setObjectName(u"combobox_primary_vector_mode")

        self.horizontallayout_primary_aim_vector.addWidget(self.combobox_primary_vector_mode)

        self.lineedit_primary_aim_vector_x = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_aim_vector_x.setObjectName(u"lineedit_primary_aim_vector_x")

        self.horizontallayout_primary_aim_vector.addWidget(self.lineedit_primary_aim_vector_x)

        self.lineedit_primary_aim_vector_y = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_aim_vector_y.setObjectName(u"lineedit_primary_aim_vector_y")

        self.horizontallayout_primary_aim_vector.addWidget(self.lineedit_primary_aim_vector_y)

        self.lineedit_primary_aim_vector_z = QLineEdit(self.group_aim_primary)
        self.lineedit_primary_aim_vector_z.setObjectName(u"lineedit_primary_aim_vector_z")

        self.horizontallayout_primary_aim_vector.addWidget(self.lineedit_primary_aim_vector_z)

        self.horizontallayout_primary_aim_vector.setStretch(0, 1)
        self.horizontallayout_primary_aim_vector.setStretch(1, 1)
        self.horizontallayout_primary_aim_vector.setStretch(2, 1)
        self.horizontallayout_primary_aim_vector.setStretch(3, 1)

        self.form_aim_primary.setLayout(0, QFormLayout.FieldRole, self.horizontallayout_primary_aim_vector)

        self.label_primary_target_vector = QLabel(self.group_aim_primary)
        self.label_primary_target_vector.setObjectName(u"label_primary_target_vector")

        self.form_aim_primary.setWidget(1, QFormLayout.LabelRole, self.label_primary_target_vector)

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


        self.form_aim_primary.setLayout(1, QFormLayout.FieldRole, self.horizontallayout_primary_target_vector)


        self.formLayout_6.setLayout(0, QFormLayout.FieldRole, self.form_aim_primary)


        self.verticallayout_aim_global.addWidget(self.group_aim_primary)

        self.group_aim_secondary = QGroupBox(atlas_matrix_aim)
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
        self.combobox_secondary_vector_mode = QComboBox(self.group_aim_secondary)
        self.combobox_secondary_vector_mode.addItem("")
        self.combobox_secondary_vector_mode.addItem("")
        self.combobox_secondary_vector_mode.addItem("")
        self.combobox_secondary_vector_mode.setObjectName(u"combobox_secondary_vector_mode")

        self.horizontallayout_secondary_up_vector.addWidget(self.combobox_secondary_vector_mode)

        self.lineedit_secondary_up_vector_x = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_up_vector_x.setObjectName(u"lineedit_secondary_up_vector_x")

        self.horizontallayout_secondary_up_vector.addWidget(self.lineedit_secondary_up_vector_x)

        self.lineedit_secondary_up_vector_y = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_up_vector_y.setObjectName(u"lineedit_secondary_up_vector_y")

        self.horizontallayout_secondary_up_vector.addWidget(self.lineedit_secondary_up_vector_y)

        self.lineedit_secondary_up_vector_z = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_up_vector_z.setObjectName(u"lineedit_secondary_up_vector_z")

        self.horizontallayout_secondary_up_vector.addWidget(self.lineedit_secondary_up_vector_z)

        self.horizontallayout_secondary_up_vector.setStretch(0, 1)
        self.horizontallayout_secondary_up_vector.setStretch(1, 1)
        self.horizontallayout_secondary_up_vector.setStretch(2, 1)
        self.horizontallayout_secondary_up_vector.setStretch(3, 1)

        self.form_aim_secondary.setLayout(0, QFormLayout.FieldRole, self.horizontallayout_secondary_up_vector)

        self.label_secondary_target_mode = QLabel(self.group_aim_secondary)
        self.label_secondary_target_mode.setObjectName(u"label_secondary_target_mode")

        self.form_aim_secondary.setWidget(1, QFormLayout.LabelRole, self.label_secondary_target_mode)

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


        self.form_aim_secondary.setLayout(1, QFormLayout.FieldRole, self.horizontallayout_secondary_target_vector)

        self.label_secondary_world_up_type = QLabel(self.group_aim_secondary)
        self.label_secondary_world_up_type.setObjectName(u"label_secondary_world_up_type")

        self.form_aim_secondary.setWidget(2, QFormLayout.LabelRole, self.label_secondary_world_up_type)

        self.combobox_secondary_world_up_type = QComboBox(self.group_aim_secondary)
        self.combobox_secondary_world_up_type.addItem("")
        self.combobox_secondary_world_up_type.addItem("")
        self.combobox_secondary_world_up_type.addItem("")
        self.combobox_secondary_world_up_type.setObjectName(u"combobox_secondary_world_up_type")

        self.form_aim_secondary.setWidget(2, QFormLayout.FieldRole, self.combobox_secondary_world_up_type)

        self.label_secondary_world_up_obj = QLabel(self.group_aim_secondary)
        self.label_secondary_world_up_obj.setObjectName(u"label_secondary_world_up_obj")

        self.form_aim_secondary.setWidget(3, QFormLayout.LabelRole, self.label_secondary_world_up_obj)

        self.lineedit_secondary_world_up_obj = QLineEdit(self.group_aim_secondary)
        self.lineedit_secondary_world_up_obj.setObjectName(u"lineedit_secondary_world_up_obj")

        self.form_aim_secondary.setWidget(3, QFormLayout.FieldRole, self.lineedit_secondary_world_up_obj)


        self.formLayout_5.setLayout(0, QFormLayout.FieldRole, self.form_aim_secondary)


        self.verticallayout_aim_global.addWidget(self.group_aim_secondary)


        self.verticalLayout.addLayout(self.verticallayout_aim_global)


        self.retranslateUi(atlas_matrix_aim)

        QMetaObject.connectSlotsByName(atlas_matrix_aim)
    # setupUi

    def retranslateUi(self, atlas_matrix_aim):
        atlas_matrix_aim.setWindowTitle(QCoreApplication.translate("atlas_matrix_aim", u"Form", None))
        self.label_aim_offset.setText(QCoreApplication.translate("atlas_matrix_aim", u"Maintain offset:", None))
        self.checkbox_aim_offset.setText("")
        self.label_aim_hold.setText(QCoreApplication.translate("atlas_matrix_aim", u"Keep hold:", None))
        self.checkbox_aim_hold.setText("")
        self.label_aim_enveloppe.setText(QCoreApplication.translate("atlas_matrix_aim", u"Enveloppe:", None))
        self.checkbox_aim_enveloppe.setText("")
        self.group_aim_primary.setTitle(QCoreApplication.translate("atlas_matrix_aim", u"Primary axis:", None))
        self.label_primary_aim_vector.setText(QCoreApplication.translate("atlas_matrix_aim", u"Aim vector:", None))
        self.combobox_primary_vector_mode.setItemText(0, QCoreApplication.translate("atlas_matrix_aim", u"Aim", None))
        self.combobox_primary_vector_mode.setItemText(1, QCoreApplication.translate("atlas_matrix_aim", u"Lock Axis", None))
        self.combobox_primary_vector_mode.setItemText(2, QCoreApplication.translate("atlas_matrix_aim", u"Align", None))

        self.lineedit_primary_aim_vector_x.setText(QCoreApplication.translate("atlas_matrix_aim", u"1.000", None))
        self.lineedit_primary_aim_vector_y.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.lineedit_primary_aim_vector_z.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.label_primary_target_vector.setText(QCoreApplication.translate("atlas_matrix_aim", u"Target vector:", None))
        self.lineedit_primary_target_vector_x.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.lineedit_primary_target_vector_y.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.lineedit_primary_target_vector_z.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.group_aim_secondary.setTitle(QCoreApplication.translate("atlas_matrix_aim", u"Secondary axis:", None))
        self.label_secondary_up_vector.setText(QCoreApplication.translate("atlas_matrix_aim", u"Up vector:", None))
        self.combobox_secondary_vector_mode.setItemText(0, QCoreApplication.translate("atlas_matrix_aim", u"Aim", None))
        self.combobox_secondary_vector_mode.setItemText(1, QCoreApplication.translate("atlas_matrix_aim", u"Align", None))
        self.combobox_secondary_vector_mode.setItemText(2, QCoreApplication.translate("atlas_matrix_aim", u"None", None))

        self.lineedit_secondary_up_vector_x.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.lineedit_secondary_up_vector_y.setText(QCoreApplication.translate("atlas_matrix_aim", u"1.000", None))
        self.lineedit_secondary_up_vector_z.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.label_secondary_target_mode.setText(QCoreApplication.translate("atlas_matrix_aim", u"Target  vector :", None))
        self.lineedit_secondary_target_vector_x.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.lineedit_secondary_target_vector_y.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.lineedit_secondary_target_vector_z.setText(QCoreApplication.translate("atlas_matrix_aim", u"0.000", None))
        self.label_secondary_world_up_type.setText(QCoreApplication.translate("atlas_matrix_aim", u"World up type:", None))
        self.combobox_secondary_world_up_type.setItemText(0, QCoreApplication.translate("atlas_matrix_aim", u"Constrained Up", None))
        self.combobox_secondary_world_up_type.setItemText(1, QCoreApplication.translate("atlas_matrix_aim", u"Object Up", None))
        self.combobox_secondary_world_up_type.setItemText(2, QCoreApplication.translate("atlas_matrix_aim", u"None", None))

        self.label_secondary_world_up_obj.setText(QCoreApplication.translate("atlas_matrix_aim", u"World up obj:", None))
    # retranslateUi
