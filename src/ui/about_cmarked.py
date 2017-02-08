# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_cmarked.ui'
#
# Created: Wed Feb  1 14:23:24 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(753, 708)
        Dialog.setModal(True)
        self.label_version = QtGui.QLabel(Dialog)
        self.label_version.setGeometry(QtCore.QRect(20, 160, 151, 31))
        self.label_version.setOpenExternalLinks(True)
        self.label_version.setObjectName("label_version")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 190, 711, 370))
        self.label_2.setObjectName("label_2")
        self.line = QtGui.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 130, 731, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(250, 10, 201, 111))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/img/img/markdown-208x128-solid.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(174, 165, 161, 20))
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 580, 201, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(220, 584, 121, 21))
        self.label_6.setOpenExternalLinks(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(222, 606, 121, 21))
        self.label_7.setOpenExternalLinks(True)
        self.label_7.setObjectName("label_7")
        self.cancel_Button = QtGui.QPushButton(Dialog)
        self.cancel_Button.setGeometry(QtCore.QRect(570, 640, 99, 27))
        self.cancel_Button.setObjectName("cancel_Button")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_Button, QtCore.SIGNAL("clicked(bool)"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About CMarked", None, QtGui.QApplication.UnicodeUTF8))
        self.label_version.setText(QtGui.QApplication.translate("Dialog", "CMarked: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "MIT License\n"
"\n"
"Copyright (c) 2017 Sergio de la Cruz, Armando Pereda\n"
"\n"
"Permission is hereby granted, free of charge, to any person obtaining a copy\n"
"of this software and associated documentation files (the \"Software\"), to deal\n"
"in the Software without restriction, including without limitation the rights\n"
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
"copies of the Software, and to permit persons to whom the Software is\n"
"furnished to do so, subject to the following conditions:\n"
"\n"
"The above copyright notice and this permission notice shall be included in all\n"
"copies or substantial portions of the Software.\n"
"\n"
"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
"LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
"SOFTWARE.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "<a href=\"https://github.com/sergiodlc/cmarked\">Source Code in Github</a>\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Find the authors on Github:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "<a href=\"https://github.com/sergiodlc\">Sergio de la Cruz</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "<a href=\"https://github.com/aplghl\">Armando Pereda</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_Button.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
