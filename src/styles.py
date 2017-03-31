from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

# Default format definitions:

# Bold
default_bold = QtGui.QTextCharFormat()
default_bold.setFontWeight(QtGui.QFont.Bold)
default_bold.setForeground(Qt.black)

# Italic
default_italic = QtGui.QTextCharFormat()
default_italic.setFontItalic(True)
default_italic.setForeground(Qt.black)

# Title 1
default_title1 = QtGui.QTextCharFormat()
default_title1.setFontWeight(QtGui.QFont.Bold)
default_title1.setForeground(Qt.blue)

editorStyles = {
    "default" : {
        b"strong" : default_bold,
        b"emph" : default_italic,
        b"heading" : default_title1,
    }
}
