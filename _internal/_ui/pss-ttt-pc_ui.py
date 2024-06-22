# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-pc.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QToolButton, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(674, 509)
        self.estMergeCrewButton = QPushButton(Dialog)
        self.estMergeCrewButton.setObjectName(u"estMergeCrewButton")
        self.estMergeCrewButton.setGeometry(QRect(10, 390, 161, 23))
        self.estOneStepRecipeCheckButton = QPushButton(Dialog)
        self.estOneStepRecipeCheckButton.setObjectName(u"estOneStepRecipeCheckButton")
        self.estOneStepRecipeCheckButton.setGeometry(QRect(260, 390, 161, 23))
        self.estAddCrewButton = QPushButton(Dialog)
        self.estAddCrewButton.setObjectName(u"estAddCrewButton")
        self.estAddCrewButton.setGeometry(QRect(10, 420, 161, 23))
        self.estDeleteCrewButton = QPushButton(Dialog)
        self.estDeleteCrewButton.setObjectName(u"estDeleteCrewButton")
        self.estDeleteCrewButton.setGeometry(QRect(10, 450, 161, 23))
        self.currentCrewList = QListWidget(Dialog)
        self.currentCrewList.setObjectName(u"currentCrewList")
        self.currentCrewList.setGeometry(QRect(0, 60, 171, 321))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        self.currentCrewList.setFont(font)
        self.currentCrewList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.currentCrewLabel = QLabel(Dialog)
        self.currentCrewLabel.setObjectName(u"currentCrewLabel")
        self.currentCrewLabel.setGeometry(QRect(0, 39, 171, 21))
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setKerning(True)
        self.currentCrewLabel.setFont(font1)
        self.currentCrewLabel.setAlignment(Qt.AlignCenter)
        self.oneStepPrestigeList = QListWidget(Dialog)
        self.oneStepPrestigeList.setObjectName(u"oneStepPrestigeList")
        self.oneStepPrestigeList.setGeometry(QRect(180, 60, 321, 321))
        self.oneStepPrestigeList.setFont(font)
        self.oneStepPrestigeList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.twoStepPrestigeList = QListWidget(Dialog)
        self.twoStepPrestigeList.setObjectName(u"twoStepPrestigeList")
        self.twoStepPrestigeList.setGeometry(QRect(510, 60, 161, 321))
        self.twoStepPrestigeList.setFont(font)
        self.oneStepPrestigeLabel = QLabel(Dialog)
        self.oneStepPrestigeLabel.setObjectName(u"oneStepPrestigeLabel")
        self.oneStepPrestigeLabel.setGeometry(QRect(180, 40, 321, 21))
        self.oneStepPrestigeLabel.setFont(font1)
        self.oneStepPrestigeLabel.setAlignment(Qt.AlignCenter)
        self.twoStepPrestigeLabel = QLabel(Dialog)
        self.twoStepPrestigeLabel.setObjectName(u"twoStepPrestigeLabel")
        self.twoStepPrestigeLabel.setGeometry(QRect(510, 40, 161, 21))
        self.twoStepPrestigeLabel.setFont(font1)
        self.twoStepPrestigeLabel.setAlignment(Qt.AlignCenter)
        self.estClearCrewListButton = QPushButton(Dialog)
        self.estClearCrewListButton.setObjectName(u"estClearCrewListButton")
        self.estClearCrewListButton.setGeometry(QRect(10, 480, 161, 23))
        self.estCalcButton = QToolButton(Dialog)
        self.estCalcButton.setObjectName(u"estCalcButton")
        self.estCalcButton.setGeometry(QRect(260, 10, 331, 21))
        self.calcTargetCrewButton = QPushButton(Dialog)
        self.calcTargetCrewButton.setObjectName(u"calcTargetCrewButton")
        self.calcTargetCrewButton.setGeometry(QRect(530, 390, 121, 23))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.estMergeCrewButton.setText(QCoreApplication.translate("Dialog", u"Merge Selected", None))
        self.estOneStepRecipeCheckButton.setText(QCoreApplication.translate("Dialog", u"Recipe Check", None))
        self.estAddCrewButton.setText(QCoreApplication.translate("Dialog", u"Add Crew", None))
        self.estDeleteCrewButton.setText(QCoreApplication.translate("Dialog", u"Delete Crew", None))
        self.currentCrewLabel.setText(QCoreApplication.translate("Dialog", u"Current Crew", None))
        self.oneStepPrestigeLabel.setText(QCoreApplication.translate("Dialog", u"1 Step Prestige", None))
        self.twoStepPrestigeLabel.setText(QCoreApplication.translate("Dialog", u"2 Step Prestige", None))
        self.estClearCrewListButton.setText(QCoreApplication.translate("Dialog", u"Clear List", None))
        self.estCalcButton.setText(QCoreApplication.translate("Dialog", u"Estimator", None))
        self.calcTargetCrewButton.setText(QCoreApplication.translate("Dialog", u"Targeted Crew Entry", None))
    # retranslateUi

