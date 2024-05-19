# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-crewtrainer.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTableView,
    QWidget)

class Ui_CrewTrainer(object):
    def setupUi(self, CrewTrainer):
        if not CrewTrainer.objectName():
            CrewTrainer.setObjectName(u"CrewTrainer")
        CrewTrainer.resize(803, 337)
        self.crewStatTable = QTableView(CrewTrainer)
        self.crewStatTable.setObjectName(u"crewStatTable")
        self.crewStatTable.setGeometry(QRect(100, 10, 181, 301))
        self.crewStatTable.setAlternatingRowColors(True)
        self.trainingPointsBox = QComboBox(CrewTrainer)
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.addItem("")
        self.trainingPointsBox.setObjectName(u"trainingPointsBox")
        self.trainingPointsBox.setGeometry(QRect(10, 20, 81, 22))
        self.trainingStatBox = QComboBox(CrewTrainer)
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.addItem("")
        self.trainingStatBox.setObjectName(u"trainingStatBox")
        self.trainingStatBox.setGeometry(QRect(10, 60, 81, 22))
        self.mergeTierBox = QComboBox(CrewTrainer)
        self.mergeTierBox.addItem("")
        self.mergeTierBox.addItem("")
        self.mergeTierBox.addItem("")
        self.mergeTierBox.addItem("")
        self.mergeTierBox.setObjectName(u"mergeTierBox")
        self.mergeTierBox.setGeometry(QRect(10, 100, 81, 22))
        self.fatigueBox = QComboBox(CrewTrainer)
        self.fatigueBox.addItem("")
        self.fatigueBox.addItem("")
        self.fatigueBox.addItem("")
        self.fatigueBox.addItem("")
        self.fatigueBox.setObjectName(u"fatigueBox")
        self.fatigueBox.setGeometry(QRect(10, 140, 81, 22))
        self.label = QLabel(CrewTrainer)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 81, 21))
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(CrewTrainer)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 81, 20))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(CrewTrainer)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 80, 81, 20))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(CrewTrainer)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 120, 81, 21))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.testPushButton = QPushButton(CrewTrainer)
        self.testPushButton.setObjectName(u"testPushButton")
        self.testPushButton.setGeometry(QRect(10, 170, 71, 23))
        self.trainingChartTable = QTableView(CrewTrainer)
        self.trainingChartTable.setObjectName(u"trainingChartTable")
        self.trainingChartTable.setGeometry(QRect(290, 0, 511, 331))
        self.openPresetsButton = QPushButton(CrewTrainer)
        self.openPresetsButton.setObjectName(u"openPresetsButton")
        self.openPresetsButton.setGeometry(QRect(10, 210, 75, 23))
        self.maxTPLabel = QLabel(CrewTrainer)
        self.maxTPLabel.setObjectName(u"maxTPLabel")
        self.maxTPLabel.setGeometry(QRect(10, 250, 81, 20))
        self.maxTPLabel.setAlignment(Qt.AlignCenter)

        self.retranslateUi(CrewTrainer)

        QMetaObject.connectSlotsByName(CrewTrainer)
    # setupUi

    def retranslateUi(self, CrewTrainer):
        CrewTrainer.setWindowTitle(QCoreApplication.translate("CrewTrainer", u"Crew Training", None))
        self.trainingPointsBox.setItemText(0, QCoreApplication.translate("CrewTrainer", u"200", None))
        self.trainingPointsBox.setItemText(1, QCoreApplication.translate("CrewTrainer", u"110", None))
        self.trainingPointsBox.setItemText(2, QCoreApplication.translate("CrewTrainer", u"100", None))
        self.trainingPointsBox.setItemText(3, QCoreApplication.translate("CrewTrainer", u"90", None))
        self.trainingPointsBox.setItemText(4, QCoreApplication.translate("CrewTrainer", u"80", None))
        self.trainingPointsBox.setItemText(5, QCoreApplication.translate("CrewTrainer", u"70", None))
        self.trainingPointsBox.setItemText(6, QCoreApplication.translate("CrewTrainer", u"60", None))
        self.trainingPointsBox.setItemText(7, QCoreApplication.translate("CrewTrainer", u"50", None))

        self.trainingStatBox.setItemText(0, QCoreApplication.translate("CrewTrainer", u"HP", None))
        self.trainingStatBox.setItemText(1, QCoreApplication.translate("CrewTrainer", u"ATK", None))
        self.trainingStatBox.setItemText(2, QCoreApplication.translate("CrewTrainer", u"RPR", None))
        self.trainingStatBox.setItemText(3, QCoreApplication.translate("CrewTrainer", u"ABL", None))
        self.trainingStatBox.setItemText(4, QCoreApplication.translate("CrewTrainer", u"STA", None))
        self.trainingStatBox.setItemText(5, QCoreApplication.translate("CrewTrainer", u"PLT", None))
        self.trainingStatBox.setItemText(6, QCoreApplication.translate("CrewTrainer", u"SCI", None))
        self.trainingStatBox.setItemText(7, QCoreApplication.translate("CrewTrainer", u"ENG", None))
        self.trainingStatBox.setItemText(8, QCoreApplication.translate("CrewTrainer", u"WPN", None))

        self.mergeTierBox.setItemText(0, QCoreApplication.translate("CrewTrainer", u"None", None))
        self.mergeTierBox.setItemText(1, QCoreApplication.translate("CrewTrainer", u"Bronze", None))
        self.mergeTierBox.setItemText(2, QCoreApplication.translate("CrewTrainer", u"Silver", None))
        self.mergeTierBox.setItemText(3, QCoreApplication.translate("CrewTrainer", u"Gold", None))

        self.fatigueBox.setItemText(0, QCoreApplication.translate("CrewTrainer", u"0", None))
        self.fatigueBox.setItemText(1, QCoreApplication.translate("CrewTrainer", u"1-50", None))
        self.fatigueBox.setItemText(2, QCoreApplication.translate("CrewTrainer", u"51-99", None))
        self.fatigueBox.setItemText(3, QCoreApplication.translate("CrewTrainer", u"100", None))

        self.label.setText(QCoreApplication.translate("CrewTrainer", u"Training Points", None))
        self.label_2.setText(QCoreApplication.translate("CrewTrainer", u"Target Stat", None))
        self.label_3.setText(QCoreApplication.translate("CrewTrainer", u"Merge Tier", None))
        self.label_4.setText(QCoreApplication.translate("CrewTrainer", u"Fatigue", None))
        self.testPushButton.setText(QCoreApplication.translate("CrewTrainer", u"Reset", None))
        self.openPresetsButton.setText(QCoreApplication.translate("CrewTrainer", u"Presets", None))
        self.maxTPLabel.setText("")
    # retranslateUi

