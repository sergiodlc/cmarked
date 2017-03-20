# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/main_window.ui'
#
# Created: Mon Mar  6 21:21:39 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1475, 980)
        MainWindow.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/markdown-32x32-orange.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowFilePath("")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.sourceText = QtGui.QTextEdit(self.splitter)
        self.sourceText.setObjectName("sourceText")
        self.previewText = QtGui.QTextEdit(self.splitter)
        self.previewText.setReadOnly(True)
        self.previewText.setObjectName("previewText")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1475, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Save_As = QtGui.QAction(MainWindow)
        self.action_Save_As.setObjectName("action_Save_As")
        self.action_Export = QtGui.QAction(MainWindow)
        self.action_Export.setObjectName("action_Export")
        self.action_Help_About = QtGui.QAction(MainWindow)
        self.action_Help_About.setObjectName("action_Help_About")
        self.action_Undo = QtGui.QAction(MainWindow)
        self.action_Undo.setEnabled(False)
        self.action_Undo.setObjectName("action_Undo")
        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setEnabled(False)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setEnabled(False)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setEnabled(False)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionConvert_to_Uppercase = QtGui.QAction(MainWindow)
        self.actionConvert_to_Uppercase.setObjectName("actionConvert_to_Uppercase")
        self.actionConvert_to_Lowercase = QtGui.QAction(MainWindow)
        self.actionConvert_to_Lowercase.setObjectName("actionConvert_to_Lowercase")
        self.actionRun = QtGui.QAction(MainWindow)
        self.actionRun.setObjectName("actionRun")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_Save_As)
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_File.addAction(self.actionRun)
        self.menuHelp.addAction(self.action_Help_About)
        self.menu_Edit.addAction(self.action_Undo)
        self.menu_Edit.addAction(self.actionRedo)
        self.menu_Edit.addAction(self.actionCut)
        self.menu_Edit.addAction(self.actionCopy)
        self.menu_Edit.addAction(self.actionPaste)
        self.menu_Edit.addAction(self.actionConvert_to_Uppercase)
        self.menu_Edit.addAction(self.actionConvert_to_Lowercase)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.sourceText, QtCore.SIGNAL("textChanged()"), MainWindow.sourceTextChanged)
        QtCore.QObject.connect(self.action_Undo, QtCore.SIGNAL("triggered()"), self.sourceText.undo)
        QtCore.QObject.connect(self.actionRedo, QtCore.SIGNAL("triggered()"), self.sourceText.redo)
        QtCore.QObject.connect(self.sourceText, QtCore.SIGNAL("undoAvailable(bool)"), self.action_Undo.setEnabled)
        QtCore.QObject.connect(self.sourceText, QtCore.SIGNAL("redoAvailable(bool)"), self.actionRedo.setEnabled)
        QtCore.QObject.connect(self.sourceText, QtCore.SIGNAL("copyAvailable(bool)"), self.actionCopy.setEnabled)
        QtCore.QObject.connect(self.previewText, QtCore.SIGNAL("copyAvailable(bool)"), self.actionCopy.setEnabled)
        QtCore.QObject.connect(self.actionCopy, QtCore.SIGNAL("triggered()"), MainWindow.onCopy)
        QtCore.QObject.connect(self.actionCut, QtCore.SIGNAL("triggered()"), self.sourceText.cut)
        QtCore.QObject.connect(self.sourceText, QtCore.SIGNAL("copyAvailable(bool)"), self.actionCut.setEnabled)
        QtCore.QObject.connect(self.actionPaste, QtCore.SIGNAL("triggered()"), self.sourceText.paste)
        QtCore.QObject.connect(self.actionConvert_to_Uppercase, QtCore.SIGNAL("triggered()"), MainWindow.onConvertToUppercase)
        QtCore.QObject.connect(self.actionConvert_to_Lowercase, QtCore.SIGNAL("triggered()"), MainWindow.onConvertToLowercase)
        QtCore.QObject.connect(self.actionRun, QtCore.SIGNAL("triggered()"), MainWindow.onRun)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_As.setText(QtGui.QApplication.translate("MainWindow", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export.setText(QtGui.QApplication.translate("MainWindow", "Export...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Help_About.setText(QtGui.QApplication.translate("MainWindow", "About CMarked...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Undo.setText(QtGui.QApplication.translate("MainWindow", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Undo.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("MainWindow", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Y", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert_to_Uppercase.setText(QtGui.QApplication.translate("MainWindow", "Convert to Uppercase", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert_to_Lowercase.setText(QtGui.QApplication.translate("MainWindow", "Convert to Lowercase", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
