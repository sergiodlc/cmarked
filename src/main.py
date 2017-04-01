#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import glob
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

try:
    from ui.main_window import Ui_MainWindow
    from ui.about_cmarked import Ui_Dialog as Ui_Help_About
    from cmark import markdown_to_html, highlightDocument, nearestSourcePos
    from highlighter import SyntaxHighlighter
    from findreplacedialog import FindDialog, FindReplaceDialog
except ImportError:
    from cmarked.ui.main_window import Ui_MainWindow
    from cmarked.ui.about_cmarked import Ui_Dialog as Ui_Help_About
    from cmarked.cmark import markdown_to_html, highlightDocument, nearestSourcePos
    from cmarked.highlighter import SyntaxHighlighter
    from cmarked.findreplacedialog import FindDialog, FindReplaceDialog


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('CMarkEd')
log.setLevel(logging.INFO)

__version__ = "0.4.0"


def fromHTMLtoCommonMark(html_file):
    try:
        commonMark = subprocess.check_output(["pandoc",
                                           html_file, "-f", "html", "-t",
                                           "commonmark"])
        return commonMark
    except subprocess.CalledProcessError as error:
        return ""

def canInsertFromMimeData(self, source):
    if source.hasHtml():
        return True
    else:
        return QtWidgets.QPlainTextEdit.canInsertFromMimeData(self, source)

def insertFromMimeData(self, source):
    if source.hasHtml():
        html = source.html()

        temp_file = "temp.html"
        with open(temp_file, 'w') as file:
            file.write(html)

        commonMark = fromHTMLtoCommonMark(temp_file)
        if commonMark:
            self.insertPlainText(commonMark.decode("utf-8"))
        os.remove(temp_file)
    else:
        QtWidgets.QPlainTextEdit.insertFromMimeData(self, source)


def contextMenuEvent(self, event, parent=None):
    def correctWord(cursor, word):
        # From QTextCursor doc:
        # if there is a selection, the selection is deleted and replaced
        return lambda: cursor.insertText(word)

    popup_menu = self.createStandardContextMenu()
    paste_action = popup_menu.actions()[6]
    paste_formatted_action = QtWidgets.QAction(self.tr("Paste raw HTML"), popup_menu)
    paste_formatted_action.triggered.connect(parent.insertFromRawHtml)
    paste_formatted_action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+V"))
    popup_menu.insertAction(paste_action, paste_formatted_action)

    # Spellcheck the word under the mouse cursor, not self.textCursor
    cursor = self.cursorForPosition(event.pos())
    cursor.select(QtGui.QTextCursor.WordUnderCursor)

    text = cursor.selectedText()
    if parent.speller and text:
        if not parent.speller.check(text):
            lastAction = popup_menu.actions()[0]
            for word in parent.speller.suggest(text)[:10]:
                action = QtWidgets.QAction(word, popup_menu)
                action.triggered.connect(correctWord(cursor, word))
                defaultFamily = QtWidgets.QApplication.font().family()
                action.setFont(QtGui.QFont(defaultFamily, weight=QtGui.QFont.Bold))
                popup_menu.insertAction(lastAction, action)
            popup_menu.insertSeparator(lastAction)

    popup_menu.exec_(event.globalPos())

class CMarkEdMainWindow(QtWidgets.QMainWindow):
    template = '''<html><head><link rel="stylesheet" href="{}"></head><body>{}</body></html>'''
    ast_ready = QtCore.pyqtSignal()
    #request_scroll_adjust = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CMarkEdMainWindow, self).__init__(parent)
        # Define some attributes:
        self.vSourceScrollBar = None
        self.vPreviewScrollBar = None
        self.previewPage = LivePreviewPage(self)
        self.appTitle = "CMarkEd"
        self.setWindowTitle(self.appTitle + " - new_common_mark.md[*]")
        self.workingFile = ""
        self.workingDirectory = ""

        self.ui = UiLayout()
        self.help_about = HelpAbout()
        self.ui.setupUi(self)

        self.ast = None
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

        # Spell checker support
        try:
            import enchant
            enchant.Dict()
            self.speller = enchant.Dict()
        except ImportError:
            log.warning("Spell checking unavailable. Need to install pyenchant.")
            self.speller = None
        except enchant.errors.DictNotFoundError:
            log.warning("Spell checking unavailable. Need to install dictionary (e.g. aspell-en).")
            self.speller = None

        self.syntaxHighlighter = SyntaxHighlighter(self.ui.sourceText.document(), self.speller)

        self.ui.previewText.setPage(self.previewPage)

        self.ui.sourceText.setCenterOnScroll(True)
        self.ui.sourceText.canInsertFromMimeData = types.MethodType(canInsertFromMimeData, self.ui.sourceText)
        self.ui.sourceText.insertFromMimeData = types.MethodType(insertFromMimeData, self.ui.sourceText)
        self.ui.sourceText.contextMenuEvent = types.MethodType(partial(contextMenuEvent, parent=self), self.ui.sourceText)

        self.ui.action_Save.setDisabled(True)

        self.vSourceScrollBar = self.ui.sourceText.verticalScrollBar()
#        self.vPreviewScrollBar = self.ui.previewText.verticalScrollBar()

        # Set up the status bar:
        self.status_template = self.tr('Chars: {0}, Words: {1}, Lines: {2}')
        self.statusLabel = QtWidgets.QLabel(self.status_template.format(0, 0, 0))
        self.ui.statusbar.addPermanentWidget(self.statusLabel)

        self.connectSlots()
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
        # self.previewPage.loadFinished.connect(self.onSourceScrollChanged)
        #self.request_scroll_adjust.connect(self.onSourceScrollChanged)
        self.previewPage.loadFinished.connect(self.updateStatusBar, QtCore.Qt.QueuedConnection)
        self.ast_ready.connect(self.applySyntaxHighlight)
        #self.ui.previewText.renderProcessTerminated.connect(self.previewPage.renderProcessTerminated)
        self.ui.actionFind.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Find))
        self.ui.actionFind.triggered.connect(FindDialog(self.ui.sourceText).show)
        self.ui.actionFind_and_Replace.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Replace))
        self.ui.actionFind_and_Replace.triggered.connect(FindReplaceDialog(self.ui.sourceText).show)

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
        font, ok = QtWidgets.QFontDialog.getFont(self.ui.sourceText.font())
        if ok:
            settings = QtCore.QSettings("CMarkEd", "CMarkEd")
            settings.setValue("editorFont", font)
            self.ui.sourceText.setFont(font)

    def onExportAsPDF(self):
        try:
            import weasyprint
            from weasyprint import HTML
            logger = weasyprint.LOGGER.warning = lambda *a, **kw: None

            fileName, filtr = QtWidgets.QFileDialog.getSaveFileName(self,
                self.tr("Export to PDF"), "", self.tr("PDF files (*.pdf)"))
            if fileName:
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                HTML(md2html(self.ui.sourceText.toPlainText())).write_pdf(fileName)
                QtWidgets.QApplication.restoreOverrideCursor()
        except ImportError:
            message = "You need to install 'weasyprint' in order to use this functionality."
            QtWidgets.QMessageBox.warning(self, self.tr("Application"),
                                      self.tr(message))

    #@QtCore.pyqtSlot(int)
    def onSourceScrollChanged(self):
        if self.vSourceScrollBar and self.ast:
            block = self.ui.sourceText.firstVisibleBlock()
            if block:
                ln = block.blockNumber()
                sp = nearestSourcePos(self.ast, ln)
                if sp:
                    self.previewPage.runJavaScript('''var el = document.querySelector('p[data-sourcepos="%s"]'); el && el.scrollIntoView();''' % sp)

    def onSourceCursorPositionChanged(self):
        pass
        # log.info("Cursor position changed")
        # cl = self.ui.sourceText.textCursor().blockNumber()
        # smin, spos, smax = self.vSourceScrollBar.minimum(), self.vSourceScrollBar.value(), self.vSourceScrollBar.maximum()
        # try:
        #     nlines = self.ui.sourceText.document().blockCount()
        #     ln = int(nlines*((spos - smin) / (smax - smin)))
        #     #log.info("Estimated line: %d", ln)
        #     sp = nearestSourcePos(self.ast, ln)
        #     log.info("Cursor at line %d of %d. Scroll at line %d. Sourcepos = '%s'", cl, nlines, ln, sp)
        #
        # except ZeroDivisionError:
        #     pass


    def sourceTextChanged(self):
        if not self.ui.previewText.isHidden():
            rendered, self.ast = markdown_to_html(self.ui.sourceText.toPlainText())
            #print(rendered)
            # Disable the web preview widget so it doesn't steal focus from the editor
            self.ui.previewText.setEnabled(False)
            self.previewPage.setHtml(self.template.format(self.style, rendered), QtCore.QUrl('file://' + self.workingFile))
            self.ui.previewText.setEnabled(True)
            #self.onSourceScrollChanged()

    def applySyntaxHighlight(self):
        pass
        # doc = self.ui.sourceText.document()
        # highlightDocument(doc, self.ast)
#        block = doc.begin()
#        node_seq = cmark.iterBlockNodes(self.ast)
#        node, node_start, node_end = next(node_seq)
#        while block != doc.end():
#            #print("Block", block.blockNumber(), "Pos:", block.position(), "Cont:", block.text())
#            ln = block.blockNumber() + 1
#            if node and not (node_start <= ln <= node_end):
#                node, node_start, node_end = next(node_seq)
#            if node and node_start <= ln <= node_end:
#                #cmark.highlightBlock(block, node)
#                block.setUserData(ASTUserData(node))
#            block = block.next()
#        self.highlighter.rehighlight()

    def onDocumentWasModified(self):
        self.setWindowModified(self.ui.sourceText.document().isModified())
        if self.isWindowModified:
            self.ui.action_Save.setDisabled(False)

    def onSaveFile(self):
        if self.workingFile:
            with self._opened_w_error(self.workingFile, 'w') as (f, err):
                if err:
                    QtWidgets.QMessageBox.warning(self, self.tr("Application"),
                            self.tr("Cannot open file: {}.").format(fileName))
                else:
                    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                    f.write(self.ui.sourceText.toPlainText())
                    self.setWindowModified(False)
                    self.ui.action_Save.setDisabled(True)
                    QtWidgets.QApplication.restoreOverrideCursor()
        else:
            fileName, filtr = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Save File"),
                "new_common_mark", self.tr("MarkDown files (*.md *.markdown);; All files(*)"))
            if fileName:
                with self._opened_w_error(fileName, 'w') as (f, err):
                    if err:
                        QtWidgets.QMessageBox.warning(self, self.tr("Application"),
                                self.tr("Cannot open file: {}.").format(fileName))
                    else:
                        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                        self.workingFile = fileName
                        workindDirectory = os.path.dirname(fileName)
                        os.chdir(workindDirectory)
                        self.workingDirectory = workindDirectory
                        f.write(self.ui.sourceText.toPlainText())
                        self.setWindowTitle(self.appTitle + " - {}[*]".format(fileName))
                        self.setWindowModified(False);
                        self.ui.action_Save.setDisabled(True)
                        QtWidgets.QApplication.restoreOverrideCursor()

    def onSaveAs(self):
        if not self.workingFile :
            self.onSaveFile()
        else:
            fileName, filtr = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Save as"),
                    "", self.tr("MarkDown files (*.md *.markdown);; All files(*)"))
            if fileName:
                with self._opened_w_error(fileName, 'w') as (f, err):
                    if err:
                        QtWidgets.QMessageBox.warning(self, self.tr("Application"),
                                self.tr("Cannot open file: {}.").format(fileName))
                    else:
                        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                        f.write(self.ui.sourceText.toPlainText())
                        if self.isWindowModified():
                            self.onSaveFile()
                        QtWidgets.QApplication.restoreOverrideCursor()

    def onOpenFile(self):
        type_of_files = "MarkDown files (*.md *.markdown);; HTML files (*.html);; All files(*)"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                self.tr("Open File"),
                "", self.tr(type_of_files))
        if fileName:
            if fileName.endswith('.html'):
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                workingDirectory = os.path.dirname(fileName)
                os.chdir(workingDirectory)

                html_text = fromHTMLtoCommonMark(fileName)

                self.ui.sourceText.setText(html_text.decode('UTF-8'))
                self.workingFile = fileName
                self.workingDirectory = workingDirectory
                self.setWindowTitle(self.appTitle + " - {}[*]".format(fileName))
                self.setWindowModified(False)
                QtWidgets.QApplication.restoreOverrideCursor()

            else:
                with open(fileName, 'r', encoding='UTF-8') as f:
                    inf = f.read()
                    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

                    workingDirectory = os.path.dirname(fileName)
                    os.chdir(workingDirectory)
                    self.ui.sourceText.setPlainText(inf)
                    self.workingFile = fileName
                    self.workingDirectory = workingDirectory
                    self.ui.sourceText.setPlainText(inf)
                    self.setWindowTitle(self.appTitle + " - {}[*]".format(fileName))
                    self.setWindowModified(False)
                    QtWidgets.QApplication.restoreOverrideCursor()

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
        fileName, filtr = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Export to"),
                "", self.tr("HTML files (*.html)"))
        if fileName:
            with self._opened_w_error(fileName, 'w') as (f, err):
                if err:
                    QtWidgets.QMessageBox.warning(self, self.tr("Application"),
                            self.tr("Cannot open file: {}.").format(fileName))
                else:
                    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                    f.write(md2html(self.ui.sourceText.toPlainText()))
                    QtWidgets.QApplication.restoreOverrideCursor()

    def onStyleChanged(self):
        if not self.ui.styles_dir:
            return
        style_action = self.ui.style_actions.checkedAction()
        self.style = os.path.join(self.ui.styles_dir, style_action.objectName() + ".css")
        log.info("Style changed to " + self.style)
        self.ui.sourceText.textChanged.emit()



    def closeEvent(self, event):
        if self.isWindowModified():
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle(self.tr("Confirmation Message"))
            msgBox.setText(self.tr("The document has been modified."))
            msgBox.setInformativeText(self.tr("Do you want to save your changes?"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Cancel:
                event.ignore()
                msgBox.close()
                return
            if ret == QtWidgets.QMessageBox.Save:
                self.onSaveFile()
        settings = QtCore.QSettings("CMarkEd", "CMarkEd")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue("lastStyle", self.ui.style_actions.checkedAction().objectName())
        event.accept()

    def onCopy(self):
        widget = QtWidgets.QApplication.instance().focusWidget()
        if widget in (self.ui.sourceText, self.ui.previewText):
            widget.copy()

    def onConvertToUppercase(self):
        self._filterSourceTextSelection(lambda text: text.upper())

    def onConvertToLowercase(self):
        self._filterSourceTextSelection(lambda text: text.lower())

    def onUpdatePasteMenuState(self):
        mime_data = QtWidgets.QApplication.instance().clipboard().mimeData()
        self.ui.actionPaste.setEnabled(mime_data and (mime_data.hasText() or mime_data.hasHtml()))

    def onRun(self):
        self.ast_ready.emit()
        self.previewPage.runJavaScript('''document.querySelector('p[data-sourcepos="1161:1-1161:43"]').scrollIntoView();''')
#        doc = self.ui.sourceText.document()
#        block = doc.begin()
#        while block != doc.end():
#            print("Block", block.blockNumber(), "Pos:", block.position(), "Cont:", block.text())
#            block = block.next()

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
        def doUpdateStatusBar(text):
            self.statusLabel.setText(self.status_template.format(
                len(text),              # number of characters
                len(text.split()),      # number of words
                text.count('\n') + 1)   # number of lines
            )

        self.previewPage.toPlainText(doUpdateStatusBar)

    def open_help_about(self):
        self.help_about.exec_()

    def insertFromRawHtml(self):
        qclippy = QtWidgets.QApplication.clipboard()
        if qclippy.mimeData().hasHtml():
            self.ui.sourceText.insertFromMimeData(self.mimeFromText(qclippy.mimeData().html()))
        else:
            self.ui.sourceText.insertFromMimeData(qclippy.mimeData())

    def mimeFromText(self, text):
        mime = QtCore.QMimeData()
        mime.setText(text)
        return mime


    def onOpenCommonMarkTutorial(self):
        webbrowser.open_new_tab("http://commonmark.org/help/tutorial/")

    def onOpenCommonMarkReference(self):
        webbrowser.open_new_tab("http://commonmark.org/help/")




class HelpAbout(QtWidgets.QDialog):
    """UI to show information about CMarked project version, license, authors, etc."""

    def __init__(self, parent=None):
        super(HelpAbout, self).__init__(parent)
        self.ui = Ui_Help_About()
        self.ui.setupUi(self)
        self.addVersionNumber(__version__)

    def addVersionNumber(self, version_number):
        self.ui.label_version.setText("CMarked: v{}.".format(version_number))




class LivePreviewPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent):
        super(LivePreviewPage, self).__init__()
        self.parent = parent
        self.loadFinished.connect(self.pageLoaded)
        #self.renderProcessTerminated.connect(self.pageRendered)

    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        if nav_type == QtWebEngineWidgets.QWebEnginePage.NavigationTypeLinkClicked:
            webbrowser.open_new_tab(url.toString())
            return False
        return True

    @QtCore.pyqtSlot('QWebEnginePage::RenderProcessTerminationStatus', int)
    def pageRendered(self, terminationStatus, exitCode):
        if terminationStatus == QtWebEngineWidgets.QWebEnginePage.NormalTerminationStatus:
            self.parent.onSourceScrollChanged()

    @QtCore.pyqtSlot(bool)
    def pageLoaded(self, ok):
        self.parent.onSourceScrollChanged()



class UiLayout(Ui_MainWindow):
    def __init__(self):
        self.style_actions = None

    def setupUi(self, MainWindow):
        super(UiLayout, self).setupUi(MainWindow)
        # Dynamically load the stylesheets:
        system_styles_dir = os.path.join(sys.prefix, 'share', 'cmarked', 'styles')
        local_styles_dir = os.path.realpath(os.path.join(__file__, os.pardir, os.pardir, 'styles'))
        print("system_styles_dir =", system_styles_dir)
        print("local_styles_dir =", local_styles_dir)

        self.styles_dir = system_styles_dir if os.path.isdir(system_styles_dir) else local_styles_dir if os.path.isdir(local_styles_dir) else None

        self.style_actions = QtWidgets.QActionGroup(MainWindow)
        self.style_actions.triggered.connect(MainWindow.onStyleChanged)

        if self.styles_dir:
            for style_file in sorted(glob.glob(os.path.join(self.styles_dir, '*.css'))):
                style_name = os.path.basename(style_file)
                menu_name = style_name[0:-4].replace("_", " ").title()
                action = QtWidgets.QAction(MainWindow)
                action.setObjectName(style_name[0:-4])
                action.setCheckable(True)
                self.menu_Styles.addAction(action)
                self.style_actions.addAction(action)

        # Restore the last style:
        settings = QtCore.QSettings("CMarkEd", "CMarkEd")
        lastStyle = settings.value("lastStyle")
        if lastStyle and os.path.isfile(os.path.join(self.styles_dir, lastStyle + '.css')):
            last_action = MainWindow.findChild(QtWidgets.QAction, lastStyle)
        else:
            last_action = MainWindow.findChild(QtWidgets.QAction, "github")
        if last_action:
            last_action.setChecked(True)
            self.style_actions.triggered.emit(last_action)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        super(UiLayout, self).retranslateUi(MainWindow)
        if self.style_actions:
            for action in self.style_actions.actions():
                action.setText(MainWindow.tr(action.objectName().replace("_", " ").title()))




class ASTUserData(QtGui.QTextBlockUserData):
    def __init__(self, node):
        self.node = node
        super(ASTUserData, self).__init__()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myMainWindow = CMarkEdMainWindow()
    myMainWindow.setWindowTitle(myMainWindow.appTitle + " - new_common_mark.md[*]")
    myMainWindow.show()
    sys.exit(app.exec_())

