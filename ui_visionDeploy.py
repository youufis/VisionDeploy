# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'visionDeploy.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)
import visionDeploy_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 768)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.linekey = QLineEdit(self.centralwidget)
        self.linekey.setObjectName(u"linekey")

        self.horizontalLayout_5.addWidget(self.linekey)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.detlst = QListView(self.centralwidget)
        self.detlst.setObjectName(u"detlst")
        self.detlst.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout_2.addWidget(self.detlst)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.lbldst = QLabel(self.centralwidget)
        self.lbldst.setObjectName(u"lbldst")

        self.horizontalLayout_2.addWidget(self.lbldst)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFrameShape(QFrame.StyledPanel)

        self.horizontalLayout_7.addWidget(self.label_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.lstfile = QListView(self.centralwidget)
        self.lstfile.setObjectName(u"lstfile")

        self.verticalLayout_3.addWidget(self.lstfile)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.txtmsg = QTextEdit(self.centralwidget)
        self.txtmsg.setObjectName(u"txtmsg")
        self.txtmsg.setMaximumSize(QSize(16777215, 16777215))
        self.txtmsg.setFrameShape(QFrame.Box)
        self.txtmsg.setLineWidth(1)

        self.horizontalLayout_6.addWidget(self.txtmsg)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.rbtimg = QRadioButton(self.centralwidget)
        self.rbtimg.setObjectName(u"rbtimg")
        self.rbtimg.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.rbtimg)

        self.rbtvideo = QRadioButton(self.centralwidget)
        self.rbtvideo.setObjectName(u"rbtvideo")
        self.rbtvideo.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.rbtvideo)

        self.rbtcam = QRadioButton(self.centralwidget)
        self.rbtcam.setObjectName(u"rbtcam")
        self.rbtcam.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.rbtcam)

        self.rbtipcam = QRadioButton(self.centralwidget)
        self.rbtipcam.setObjectName(u"rbtipcam")
        self.rbtipcam.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_3.addWidget(self.rbtipcam)

        self.gboxipcam = QGroupBox(self.centralwidget)
        self.gboxipcam.setObjectName(u"gboxipcam")
        self.gboxipcam.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_4 = QHBoxLayout(self.gboxipcam)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.gboxipcam)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.leip = QLineEdit(self.gboxipcam)
        self.leip.setObjectName(u"leip")
        self.leip.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_4.addWidget(self.leip)

        self.label_4 = QLabel(self.gboxipcam)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.cboxcamid = QComboBox(self.gboxipcam)
        self.cboxcamid.setObjectName(u"cboxcamid")

        self.horizontalLayout_4.addWidget(self.cboxcamid)

        self.label_5 = QLabel(self.gboxipcam)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.leuser = QLineEdit(self.gboxipcam)
        self.leuser.setObjectName(u"leuser")
        self.leuser.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_4.addWidget(self.leuser)

        self.label_6 = QLabel(self.gboxipcam)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.lepwd = QLineEdit(self.gboxipcam)
        self.lepwd.setObjectName(u"lepwd")
        self.lepwd.setMaximumSize(QSize(16777215, 16777215))
        self.lepwd.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_4.addWidget(self.lepwd)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_3.addWidget(self.gboxipcam)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cboxscaled = QCheckBox(self.centralwidget)
        self.cboxscaled.setObjectName(u"cboxscaled")
        self.cboxscaled.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout.addWidget(self.cboxscaled)

        self.chkall = QCheckBox(self.centralwidget)
        self.chkall.setObjectName(u"chkall")
        self.chkall.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout.addWidget(self.chkall)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setMaximumSize(QSize(16777215, 18))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.cboxtask = QComboBox(self.centralwidget)
        self.cboxtask.setObjectName(u"cboxtask")

        self.horizontalLayout.addWidget(self.cboxtask)

        self.cboxmodel = QComboBox(self.centralwidget)
        self.cboxmodel.setObjectName(u"cboxmodel")

        self.horizontalLayout.addWidget(self.cboxmodel)

        self.btnopen = QPushButton(self.centralwidget)
        self.btnopen.setObjectName(u"btnopen")

        self.horizontalLayout.addWidget(self.btnopen)

        self.btnsnap = QPushButton(self.centralwidget)
        self.btnsnap.setObjectName(u"btnsnap")
        self.btnsnap.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btnsnap)

        self.btnrec = QPushButton(self.centralwidget)
        self.btnrec.setObjectName(u"btnrec")
        self.btnrec.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btnrec)

        self.btnclose = QPushButton(self.centralwidget)
        self.btnclose.setObjectName(u"btnclose")

        self.horizontalLayout.addWidget(self.btnclose)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 22))
        self.menuhelp = QMenu(self.menubar)
        self.menuhelp.setObjectName(u"menuhelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuhelp.menuAction())
        self.menuhelp.addAction(self.action)
        self.menuhelp.addSeparator()
        self.menuhelp.addAction(self.action_2)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.linekey.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6216\u8f93\u5165\u68c0\u6d4b\u76ee\u6807\u540d\u79f0\u540e\u56de\u8f66", None))
        self.lbldst.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u68c0\u6d4b\u7ed3\u679c\u6587\u4ef6\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u6e90\uff1a", None))
        self.rbtimg.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u6587\u4ef6", None))
        self.rbtvideo.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6587\u4ef6", None))
        self.rbtcam.setText(QCoreApplication.translate("MainWindow", u"\u6444\u50cf\u5934", None))
        self.rbtipcam.setText(QCoreApplication.translate("MainWindow", u"\u5f55\u50cf\u673a", None))
        self.gboxipcam.setTitle("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"IP:", None))
        self.leip.setInputMask("")
        self.leip.setPlaceholderText(QCoreApplication.translate("MainWindow", u"192.168.1.1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u901a\u9053\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5e10\u53f7\uff1a", None))
        self.leuser.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5e10\u53f7", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\uff1a", None))
        self.lepwd.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.cboxscaled.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u9690\u85cf", None))
        self.chkall.setText(QCoreApplication.translate("MainWindow", u"\u8be6\u7ec6\u8bb0\u5f55", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u6a21\u578b\uff1a", None))
        self.btnopen.setText(QCoreApplication.translate("MainWindow", u"\u9884\u89c8/\u9884\u6d4b", None))
        self.btnsnap.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u7167", None))
        self.btnrec.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5f55\u5236", None))
        self.btnclose.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.menuhelp.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

