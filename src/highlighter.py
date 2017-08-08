import re
import sys

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    WORDS = r"(?iu)[^\W\d_]+('[a-zA-Z])?"
    SPELLCHECKSTYLE = QtGui.QTextCharFormat.WaveUnderline if sys.platform != 'darwin' else QtGui.QTextCharFormat.DashDotLine

    def __init__(self, parent=None, speller=None):
        super(SyntaxHighlighter, self).__init__(parent)
        self.speller = speller

    def highlightSpellcheck(self, text):
        for word_object in re.finditer(self.WORDS, str(text)):
            if not word_object.group():  # Don't bother with empty words
                continue
            if self.speller and not self.speller.check(word_object.group()):
                current_format = self.format(word_object.start())
                current_format.setUnderlineColor(Qt.red)
                current_format.setUnderlineStyle(self.SPELLCHECKSTYLE)
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), current_format)

    def highlightBlock(self, text):
        self.highlightSpellcheck(text)

