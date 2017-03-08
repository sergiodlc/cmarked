#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example for using the shared library from python
# Will work with either python 2 or python 3
# Requires cmark library to be installed

import sys
import platform
import logging
import os
import logging
import webbrowser
from contextlib import contextmanager
from ctypes import CDLL, c_char_p, c_long
import subprocess
import types

from PySide import QtCore, QtGui

try:
    from ui.main_window import Ui_MainWindow
    from ui.about_cmarked import Ui_Dialog as Ui_Help_About
except ImportError:
    from cmarked.ui.main_window import Ui_MainWindow
    from cmarked.ui.about_cmarked import Ui_Dialog as Ui_Help_About


sysname = platform.system()

if sysname == 'Darwin':
    libname = "libcmark.dylib"
elif sysname == 'Windows':
    libname = "cmark.dll"
else:
    libname = "libcmark.so"
cmark = CDLL(libname)

markdown = cmark.cmark_markdown_to_html
markdown.restype = c_char_p
markdown.argtypes = [c_char_p, c_long, c_long]

opts = 0 # defaults

def md2html(text):
    if sys.version_info >= (3,0):
        textbytes = text.encode('utf-8')
        textlen = len(textbytes)
        return markdown(textbytes, textlen, opts).decode('utf-8')
    else:
        textbytes = text
        textlen = len(text)
        return markdown(textbytes, textlen, opts)


logging.basicConfig(level=logging.DEBUG)

__version__ = "0.4.0"

foghorn = '@import url(http://fonts.googleapis.com/css?family=Vollkorn:400,400italic,700,700italic&subset=latin);ol,ul{padding-left:1.2em}body,code,html{background:#fff}body,h1 a,h1 a:hover{color:#333}a,h1 a,h1 a:hover{text-decoration:none}hr,video{margin:2em 0}h1,h2,p#heart{text-align:center}table tr td,table tr th{border:1px solid #ccc;text-align:left;padding:6px 13px;margin:0}h1,p,table tr td :first-child,table tr th :first-child{margin-top:0}pre code,table,table tr{padding:0}body,html{padding:1em;margin:auto}body{font:1.3em Vollkorn,Palatino,Times;line-height:1;text-align:justify}h1,h2,h3{font-weight:400}h3,nav{font-style:italic}code,nav{font-size:.9em}article,footer,header,nav{margin:0 auto}article{margin-top:4em;margin-bottom:4em;min-height:400px}footer{margin-bottom:50px}video{border:1px solid #ddd}nav{border-bottom:1px solid #ddd;padding:1em 0}nav p{margin:0}p{-webkit-hypens:auto;-moz-hypens:auto;hyphens:auto}ul{list-style:square}blockquote{margin-left:1em;padding-left:1em;border-left:1px solid #ddd}code{font-family:Consolas,Menlo,Monaco,monospace,serif}a{color:#2484c1}a:hover{text-decoration:underline}a img{border:0}hr{color:#ddd;height:1px;border-top:solid 1px #ddd;border-bottom:0;border-left:0;border-right:0}p#heart{font-size:2em;line-height:1;color:#ccc}.red{color:#b50000}body#index li{margin-bottom:1em}@media only screen and (max-device-width:1024px){body{font-size:120%;line-height:1.4}}@media only screen and (max-device-width:480px){body{text-align:left}article,footer{width:auto}article{padding:0 10px}}table tr{border-top:1px solid #ccc;background-color:#fff;margin:0}table tr:nth-child(2n){background-color:#aaa}table tr th{font-weight:700}table tr td:last-child,table tr th :last-child{margin-bottom:0}img{max-width:100%}code,tt{margin:0 2px;padding:0 5px;white-space:nowrap;border:1px solid #eaeaea;background-color:#f8f8f8;border-radius:3px}pre code{margin:0;white-space:pre;border:none;background:0 0}.highlight pre,pre{background-color:#f8f8f8;border:1px solid #ccc;font-size:13px;line-height:19px;overflow:auto;padding:6px 10px;border-radius:3px}'

def fromHTMLtoCommonMark(file):
    try:
        commonMark = subprocess.check_output(["pandoc",
                                           file, "-f", "html", "-t",
                                           "commonmark"])
        return commonMark
    except subprocess.CalledProcessError as error:
        return ""

def canInsertFromMimeData(self, source):
    if source.hasHtml():
        return True
    else:
        return QtGui.QTextEdit.canInsertFromMimeData(self, source)
        
def insertFromMimeData(self, source):
    if source.hasHtml():
        html = source.html()

        temp_file = "temp.html"
        with open(temp_file, 'w') as file:
            file.write(html)

        commonMark = fromHTMLtoCommonMark(temp_file)
        os.remove(temp_file)
        if commonMark:
            cursor = self.textCursor()
            cursor.insertText(commonMark.decode("utf-8"))
    else:
        QtGui.QTextEdit.insertFromMimeData(self, source) 


class CMarkEdMainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(CMarkEdMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.help_about = HelpAbout()
        self.ui.setupUi(self)
        # Restore Window geometry and state:
        settings = QtCore.QSettings("CMarkEd", "CMarkEd")
        geometry = settings.value("geometry")
        editorFont = settings.value("editorFont")
        if editorFont:
            self.ui.sourceText.setFont(editorFont)
        if geometry:
            self.restoreGeometry(geometry)
        windowState = settings.value("windowState")
        if windowState:
            self.restoreState(windowState)

        self.ui.sourceText.canInsertFromMimeData = types.MethodType(canInsertFromMimeData, self.ui.sourceText)
        self.ui.sourceText.insertFromMimeData = types.MethodType(insertFromMimeData, self.ui.sourceText)

        self.ui.action_Save.setDisabled(True)

        self.vSourceScrollBar = self.ui.sourceText.verticalScrollBar()
        self.vPreviewScrollBar = self.ui.previewText.verticalScrollBar()

        # Set up the status bar:
        self.status_template = self.tr('Chars: {0}, Ln: {1}')
        self.statusLabel = QtGui.QLabel(self.status_template.format(0, 0))
        self.ui.statusbar.addPermanentWidget(self.statusLabel)

        self.connectSlots()
        self.appTitle = "CMarked"
        self.setWindowTitle(self.appTitle + " - new_common_mark.md[*]")
        self.workingFile = ""
        self.workingDirectory = ""
        #self.ui.previewText.setDefaultStyleSheet(foghorn)
        self.loadFile()

    def connectSlots(self):
        self.ui.action_Open.triggered.connect(self.onOpenFile)
        self.ui.action_Save.triggered.connect(self.onSaveFile)
        self.ui.action_Save_As.triggered.connect(self.onSaveAs)
        self.ui.action_Export.triggered.connect(self.onExport)
        self.ui.sourceText.document().contentsChanged.connect(self.onDocumentWasModified)
        self.ui.action_Quit.triggered.connect(self.close)
        self.ui.action_Help_About.triggered.connect(self.open_help_about)
        self.ui.action_Live_Preview.changed.connect(self.onLivePreview)
        self.ui.action_Vertical_Layout.changed.connect(self.onVerticalLayout)
        self.ui.action_Swap_Views.changed.connect(self.onSwapViews)
        self.ui.action_Change_Editor_Font.triggered.connect(self.onChangeEditorFont)
        self.ui.action_Export_as_PDF.triggered.connect(self.onExportAsPDF)
        # Experimenting with scrolling:
        if self.vSourceScrollBar:
            self.vSourceScrollBar.actionTriggered.connect(self.onSourceScrollChanged)
        self.ui.previewText.textChanged.connect(self.updateStatusBar)

    def onLivePreview(self):
        if self.ui.action_Live_Preview.isChecked():
            self.ui.previewText.show()
            self.sourceTextChanged()
        else:
            self.ui.previewText.hide()

    def onVerticalLayout(self):
        if self.ui.action_Vertical_Layout.isChecked():
            self.ui.splitter.setOrientation(QtCore.Qt.Vertical)
        else:
            self.ui.splitter.setOrientation(QtCore.Qt.Horizontal)

    def onSwapViews(self):
        if self.ui.action_Live_Preview.isChecked():
            sourceText = self.ui.splitter.widget(0)
            self.ui.splitter.addWidget(sourceText)
        else:
            previewText = self.ui.splitter.widget(0)
            self.ui.splitter.addWidget(previewText)

    def onChangeEditorFont(self):
        font, ok = QtGui.QFontDialog.getFont(self.ui.sourceText.font())
        if ok:
            settings = QtCore.QSettings("CMarkEd", "CMarkEd")
            settings.setValue("editorFont", font)
            self.ui.sourceText.setFont(font)

    def onExportAsPDF(self):
        try:
            import weasyprint
            from weasyprint import HTML
            logger = weasyprint.LOGGER.warning = lambda *a, **kw: None

            fileName, filtr = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Export to PDF"), "", self.tr("PDF files (*.pdf)"))
            if fileName:
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                HTML(string=self.ui.previewText.toHtml()).write_pdf(fileName)
                QtGui.QApplication.restoreOverrideCursor()
        except ImportError:
            message = "You need to install 'weasyprint' in order to use this functionality."
            QtGui.QMessageBox.warning(self, self.tr("Application"),
                                      self.tr(message))

    def onSourceScrollChanged(self):
        if self.vPreviewScrollBar and self.vSourceScrollBar:
            smin, spos, smax = self.vSourceScrollBar.minimum(), self.vSourceScrollBar.value(), self.vSourceScrollBar.maximum()
            tmin, tmax = self.vPreviewScrollBar.minimum(), self.vPreviewScrollBar.maximum()
            try:
                self.vPreviewScrollBar.setValue(((spos - smin) / (smax - smin)) * (tmax - tmin) + tmin)
            except ZeroDivisionError:
                pass

    def sourceTextChanged(self):
        if not self.ui.previewText.isHidden():
            preview_pos = self.vPreviewScrollBar.value() if self.vPreviewScrollBar else None
            rendered = md2html(self.ui.sourceText.toPlainText())
            self.ui.previewText.setHtml(rendered)
            if preview_pos is not None:
                self.vPreviewScrollBar.setValue(preview_pos)

    def onDocumentWasModified(self):
        self.setWindowModified(self.ui.sourceText.document().isModified())
        if self.isWindowModified:
            self.ui.action_Save.setDisabled(False)

    def onSaveFile(self):
        if self.workingFile:
            with self._opened_w_error(self.workingFile, 'w') as (f, err):
                if err:
                    QtGui.QMessageBox.warning(self, self.tr("Application"),
                            self.tr("Cannot open file: {}.").format(fileName))
                else:
                    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                    f.write(self.ui.sourceText.toPlainText())
                    self.setWindowModified(False)
                    self.ui.action_Save.setDisabled(True)
                    QtGui.QApplication.restoreOverrideCursor()
        else:
            fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, self.tr("Save File"),
                "new_common_mark", self.tr("MarkDown files (*.md *.markdown);; All files(*.*)"))
            if fileName:
                with self._opened_w_error(fileName, 'w') as (f, err):
                    if err:
                        QtGui.QMessageBox.warning(self, self.tr("Application"),
                                self.tr("Cannot open file: {}.").format(fileName))
                    else:
                        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                        self.workingFile = fileName
                        workindDirectory = os.path.dirname(fileName)
                        os.chdir(workindDirectory)
                        self.workingDirectory = workindDirectory
                        f.write(self.ui.sourceText.toPlainText())
                        self.setWindowTitle(self.appTitle + " - {}[*]".format(fileName))
                        self.setWindowModified(False);
                        self.ui.action_Save.setDisabled(True)
                        QtGui.QApplication.restoreOverrideCursor()

    def onSaveAs(self):
        if not self.workingFile :
            self.onSaveFile()
        else:
            fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, self.tr("Save as"),
                    "", self.tr("MarkDown files (*.md *.markdown);; All files(*.*)"))
            if fileName:
                with self._opened_w_error(fileName, 'w') as (f, err):
                    if err:
                        QtGui.QMessageBox.warning(self, self.tr("Application"),
                                self.tr("Cannot open file: {}.").format(fileName))
                    else:
                        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                        f.write(self.ui.sourceText.toPlainText())
                        if self.isWindowModified():
                            self.onSaveFile()
                        QtGui.QApplication.restoreOverrideCursor()

    def onOpenFile(self):
        type_of_files = "MarkDown files (*.md *.markdown);; HTML files (*.html);; All files(*.*)"
        fileName, _ = QtGui.QFileDialog.getOpenFileName(self,
                self.tr("Open File"),
                "", self.tr(type_of_files))
        if fileName:
            if fileName.endswith('.html'):
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                workingDirectory = os.path.dirname(fileName)
                os.chdir(workingDirectory)

                html_text = fromHTMLtoCommonMark(fileName)
                
                self.ui.sourceText.setText(html_text.decode('UTF-8'))
                self.workingFile = fileName
                self.workingDirectory = workingDirectory
                self.setWindowTitle(self.appTitle + " - {}[*]".format(fileName))
                self.setWindowModified(False)
                QtGui.QApplication.restoreOverrideCursor()

            else:
                with open(fileName, 'r', encoding='UTF-8') as f:
                    inf = f.read()
                    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                    
                    workingDirectory = os.path.dirname(fileName)
                    os.chdir(workingDirectory)
                    
                    self.ui.sourceText.setPlainText(inf)
                    self.workingFile = fileName
                    self.workingDirectory = workingDirectory
                    self.setWindowTitle(self.appTitle + " - {}[*]".format(fileName))
                    self.setWindowModified(False)
                    QtGui.QApplication.restoreOverrideCursor()

    def loadFile(self):
        """Open a file with commonmark data information when is passed by argument in sys.argv"""
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
            file_name = os.path.realpath(file_name)
            with self._opened_w_error(file_name, 'r') as (f, err):
                if err:
                    pass
                else:
                    inf = f.read()
                    workingDirectory = os.path.dirname(file_name)
                    os.chdir(workingDirectory)
                    self.ui.sourceText.setPlainText(inf)
                    self.workingFile = file_name
                    self.workingDirectory = workingDirectory
                    self.setWindowTitle(self.appTitle + " - {}[*]".format(file_name))
                    self.setWindowModified(False)

    def onExport(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, self.tr("Export to"),
                "", self.tr("HTML files (*.html)"))
        if fileName:
            with self._opened_w_error(fileName, 'w') as (f, err):
                if err:
                    QtGui.QMessageBox.warning(self, self.tr("Application"),
                            self.tr("Cannot open file: {}.").format(fileName))
                else:
                    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                    f.write(self.ui.previewText.toHtml())
                    QtGui.QApplication.restoreOverrideCursor()

    def closeEvent(self, event):
        if self.isWindowModified():
            msgBox = QtGui.QMessageBox(self)
            msgBox.setWindowTitle(self.tr("Confirmation Message"))
            msgBox.setText(self.tr("The document has been modified."))
            msgBox.setInformativeText(self.tr("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Cancel:
                event.ignore()
                msgBox.close()
                return
            if ret == QtGui.QMessageBox.Save:
                self.onSaveFile()
        settings = QtCore.QSettings("CMarkEd", "CMarkEd")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        event.accept()

    def onCopy(self):
        widget = QtGui.QApplication.instance().focusWidget()
        if widget in (self.ui.sourceText, self.ui.previewText):
            widget.copy()

    def onConvertToUppercase(self):
        self._filterSourceTextSelection(lambda text: text.upper())

    def onConvertToLowercase(self):
        self._filterSourceTextSelection(lambda text: text.lower())

    def onUpdatePasteMenuState(self):
        mime_data = QtGui.QApplication.instance().clipboard().mimeData()
        self.ui.actionPaste.setEnabled(mime_data and (mime_data.hasText() or mime_data.hasHtml()))

    @staticmethod
    @contextmanager
    def _opened_w_error(filename, mode, encoding="UTF-8"):
        try:
            f = open(filename, mode, encoding=encoding)
        except (IOError, TypeError, PermissionError) as err:
            yield None, err
        else:
            try:
                yield f, None
            finally:
                f.close()

    def _filterSourceTextSelection(self, func):
        cursor = self.ui.sourceText.textCursor()
        if cursor.hasSelection():
            cursor.insertText(func(cursor.selectedText()))

    def updateStatusBar(self):
        doc = self.ui.previewText.document()
        self.statusLabel.setText(self.status_template.format(doc.characterCount(), doc.lineCount()))

    def open_help_about(self):
        self.help_about.exec_()

    def onOpenCommonMarkTutorial(self):
        webbrowser.open_new_tab("http://commonmark.org/help/tutorial/")

    def onOpenCommonMarkReference(self):
        webbrowser.open_new_tab("http://commonmark.org/help/")


class HelpAbout(QtGui.QDialog):
    """UI to show information about CMarked project version, license, authors, etc."""

    def __init__(self, parent=None):
        super(HelpAbout, self).__init__(parent)
        self.ui = Ui_Help_About()
        self.ui.setupUi(self)
        self.addVersionNumber(__version__)

    def addVersionNumber(self, version_number):
        self.ui.label_version.setText("CMarked: v{}.".format(version_number))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myMainWindow = CMarkEdMainWindow()
    myMainWindow.show()
    sys.exit(app.exec_())

