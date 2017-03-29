# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1475, 980)
        MainWindow.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/markdown-32x32-orange.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowFilePath("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.sourceText = QtWidgets.QTextEdit(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sourceText.sizePolicy().hasHeightForWidth())
        self.sourceText.setSizePolicy(sizePolicy)
        self.sourceText.setObjectName("sourceText")
        self.previewText = QtWebEngineWidgets.QWebEngineView(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.previewText.sizePolicy().hasHeightForWidth())
        self.previewText.setSizePolicy(sizePolicy)
        self.previewText.setObjectName("previewText")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1475, 25))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menu_Styles = QtWidgets.QMenu(self.menubar)
        self.menu_Styles.setObjectName("menu_Styles")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Save_As = QtWidgets.QAction(MainWindow)
        self.action_Save_As.setObjectName("action_Save_As")
        self.action_Export = QtWidgets.QAction(MainWindow)
        self.action_Export.setObjectName("action_Export")
        self.action_Help_About = QtWidgets.QAction(MainWindow)
        self.action_Help_About.setObjectName("action_Help_About")
        self.action_Undo = QtWidgets.QAction(MainWindow)
        self.action_Undo.setEnabled(False)
        self.action_Undo.setObjectName("action_Undo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setEnabled(False)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setEnabled(False)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setEnabled(False)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionConvert_to_Uppercase = QtWidgets.QAction(MainWindow)
        self.actionConvert_to_Uppercase.setObjectName("actionConvert_to_Uppercase")
        self.actionConvert_to_Lowercase = QtWidgets.QAction(MainWindow)
        self.actionConvert_to_Lowercase.setObjectName("actionConvert_to_Lowercase")
        self.action_Vertical_Layout = QtWidgets.QAction(MainWindow)
        self.action_Vertical_Layout.setCheckable(True)
        self.action_Vertical_Layout.setObjectName("action_Vertical_Layout")
        self.action_Swap_Views = QtWidgets.QAction(MainWindow)
        self.action_Swap_Views.setCheckable(True)
        self.action_Swap_Views.setObjectName("action_Swap_Views")
        self.action_Live_Preview = QtWidgets.QAction(MainWindow)
        self.action_Live_Preview.setCheckable(True)
        self.action_Live_Preview.setChecked(True)
        self.action_Live_Preview.setObjectName("action_Live_Preview")
        self.action_Change_Editor_Font = QtWidgets.QAction(MainWindow)
        self.action_Change_Editor_Font.setObjectName("action_Change_Editor_Font")
        self.action_Export_as_PDF = QtWidgets.QAction(MainWindow)
        self.action_Export_as_PDF.setObjectName("action_Export_as_PDF")
        self.actionCommonMark_Tutorial = QtWidgets.QAction(MainWindow)
        self.actionCommonMark_Tutorial.setObjectName("actionCommonMark_Tutorial")
        self.actionCommonMark_Reference = QtWidgets.QAction(MainWindow)
        self.actionCommonMark_Reference.setObjectName("actionCommonMark_Reference")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_Save_As)
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addAction(self.action_Export_as_PDF)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menuHelp.addAction(self.actionCommonMark_Tutorial)
        self.menuHelp.addAction(self.actionCommonMark_Reference)
        self.menuHelp.addAction(self.action_Help_About)
        self.menu_Edit.addAction(self.action_Undo)
        self.menu_Edit.addAction(self.actionRedo)
        self.menu_Edit.addAction(self.actionCut)
        self.menu_Edit.addAction(self.actionCopy)
        self.menu_Edit.addAction(self.actionPaste)
        self.menu_Edit.addAction(self.actionConvert_to_Uppercase)
        self.menu_Edit.addAction(self.actionConvert_to_Lowercase)
        self.menuView.addAction(self.action_Live_Preview)
        self.menuView.addAction(self.action_Vertical_Layout)
        self.menuView.addAction(self.action_Swap_Views)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Change_Editor_Font)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menu_Styles.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.sourceText.textChanged.connect(MainWindow.sourceTextChanged)
        self.action_Undo.triggered.connect(self.sourceText.undo)
        self.actionRedo.triggered.connect(self.sourceText.redo)
        self.sourceText.undoAvailable['bool'].connect(self.action_Undo.setEnabled)
        self.sourceText.redoAvailable['bool'].connect(self.actionRedo.setEnabled)
        self.sourceText.copyAvailable['bool'].connect(self.actionCopy.setEnabled)
        self.actionCopy.triggered.connect(MainWindow.onCopy)
        self.actionCut.triggered.connect(self.sourceText.cut)
        self.sourceText.copyAvailable['bool'].connect(self.actionCut.setEnabled)
        self.actionPaste.triggered.connect(self.sourceText.paste)
        self.actionConvert_to_Uppercase.triggered.connect(MainWindow.onConvertToUppercase)
        self.actionConvert_to_Lowercase.triggered.connect(MainWindow.onConvertToLowercase)
        self.menu_Edit.aboutToShow.connect(MainWindow.onUpdatePasteMenuState)
        self.actionCommonMark_Tutorial.triggered.connect(MainWindow.onOpenCommonMarkTutorial)
        self.actionCommonMark_Reference.triggered.connect(MainWindow.onOpenCommonMarkReference)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menu_Styles.setTitle(_translate("MainWindow", "&Styles"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))
        self.action_Quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_Save.setText(_translate("MainWindow", "Save"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_Open.setText(_translate("MainWindow", "Open"))
        self.action_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Save_As.setText(_translate("MainWindow", "Save As..."))
        self.action_Export.setText(_translate("MainWindow", "Export..."))
        self.action_Help_About.setText(_translate("MainWindow", "About CMarked..."))
        self.action_Undo.setText(_translate("MainWindow", "Undo"))
        self.action_Undo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionConvert_to_Uppercase.setText(_translate("MainWindow", "Convert to Uppercase"))
        self.actionConvert_to_Lowercase.setText(_translate("MainWindow", "Convert to Lowercase"))
        self.action_Vertical_Layout.setText(_translate("MainWindow", "Vertical Layout"))
        self.action_Swap_Views.setText(_translate("MainWindow", "Swap Views"))
        self.action_Live_Preview.setText(_translate("MainWindow", "Live Preview"))
        self.action_Change_Editor_Font.setText(_translate("MainWindow", "Change Editor Font"))
        self.action_Export_as_PDF.setText(_translate("MainWindow", "Export as PDF"))
        self.actionCommonMark_Tutorial.setText(_translate("MainWindow", "CommonMark &Tutorial"))
        self.actionCommonMark_Reference.setText(_translate("MainWindow", "CommonMark &Reference"))

from PyQt5 import QtWebEngineWidgets
from . import resources_rc
