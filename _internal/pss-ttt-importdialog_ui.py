# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-importdialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QWidget)

class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        if not ImportDialog.objectName():
            ImportDialog.setObjectName(u"ImportDialog")
        ImportDialog.resize(380, 169)
        self.importDialogLabel = QLabel(ImportDialog)
        self.importDialogLabel.setObjectName(u"importDialogLabel")
        self.importDialogLabel.setGeometry(QRect(10, 60, 311, 71))
        self.importFilenameBox = QPlainTextEdit(ImportDialog)
        self.importFilenameBox.setObjectName(u"importFilenameBox")
        self.importFilenameBox.setGeometry(QRect(20, 20, 181, 31))
        self.importFilenameBox.setTabChangesFocus(True)
        self.importFilenameLabel = QLabel(ImportDialog)
        self.importFilenameLabel.setObjectName(u"importFilenameLabel")
        self.importFilenameLabel.setGeometry(QRect(20, 0, 181, 21))
        self.importFilenameLabel.setAlignment(Qt.AlignCenter)
        self.importTargetsButton = QPushButton(ImportDialog)
        self.importTargetsButton.setObjectName(u"importTargetsButton")
        self.importTargetsButton.setGeometry(QRect(210, 0, 101, 23))
        self.importProgressBar = QProgressBar(ImportDialog)
        self.importProgressBar.setObjectName(u"importProgressBar")
        self.importProgressBar.setGeometry(QRect(10, 140, 361, 23))
        self.importProgressBar.setValue(0)
        self.importBrowse = QPushButton(ImportDialog)
        self.importBrowse.setObjectName(u"importBrowse")
        self.importBrowse.setGeometry(QRect(210, 30, 101, 23))
        self.importSeeChanges = QPushButton(ImportDialog)
        self.importSeeChanges.setObjectName(u"importSeeChanges")
        self.importSeeChanges.setGeometry(QRect(310, 0, 71, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importSeeChanges.sizePolicy().hasHeightForWidth())
        self.importSeeChanges.setSizePolicy(sizePolicy)
        font = QFont()
        font.setStrikeOut(False)
        font.setKerning(True)
        self.importSeeChanges.setFont(font)
        self.importSeeChanges.setFocusPolicy(Qt.TabFocus)
        self.importSeeChanges.setLayoutDirection(Qt.LeftToRight)

        self.retranslateUi(ImportDialog)

        QMetaObject.connectSlotsByName(ImportDialog)
    # setupUi

    def retranslateUi(self, ImportDialog):
        ImportDialog.setWindowTitle(QCoreApplication.translate("ImportDialog", u"Import Targets Data", None))
        self.importDialogLabel.setText("")
        self.importFilenameLabel.setText(QCoreApplication.translate("ImportDialog", u"Import file name", None))
        self.importTargetsButton.setText(QCoreApplication.translate("ImportDialog", u"Import targets", None))
        self.importBrowse.setText(QCoreApplication.translate("ImportDialog", u"Browse", None))
        self.importSeeChanges.setText(QCoreApplication.translate("ImportDialog", u"See Changes", None))
    # retranslateUi

