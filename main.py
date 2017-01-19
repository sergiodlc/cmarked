#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example for using the shared library from python
# Will work with either python 2 or python 3
# Requires cmark library to be installed

from ctypes import CDLL, c_char_p, c_long
import sys
import platform
import logging

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

# sys.stdout.write(md2html(sys.stdin.read()))


logging.basicConfig(level=logging.DEBUG)

from PySide import QtCore, QtGui
from ui.main_window import Ui_MainWindow

__version__ = "0.1.0"

foghorn = '@import url(http://fonts.googleapis.com/css?family=Vollkorn:400,400italic,700,700italic&subset=latin);ol,ul{padding-left:1.2em}body,code,html{background:#fff}body,h1 a,h1 a:hover{color:#333}a,h1 a,h1 a:hover{text-decoration:none}hr,video{margin:2em 0}h1,h2,p#heart{text-align:center}table tr td,table tr th{border:1px solid #ccc;text-align:left;padding:6px 13px;margin:0}h1,p,table tr td :first-child,table tr th :first-child{margin-top:0}pre code,table,table tr{padding:0}body,html{padding:1em;margin:auto}body{font:1.3em Vollkorn,Palatino,Times;line-height:1;text-align:justify}h1,h2,h3{font-weight:400}h3,nav{font-style:italic}code,nav{font-size:.9em}article,footer,header,nav{margin:0 auto}article{margin-top:4em;margin-bottom:4em;min-height:400px}footer{margin-bottom:50px}video{border:1px solid #ddd}nav{border-bottom:1px solid #ddd;padding:1em 0}nav p{margin:0}p{-webkit-hypens:auto;-moz-hypens:auto;hyphens:auto}ul{list-style:square}blockquote{margin-left:1em;padding-left:1em;border-left:1px solid #ddd}code{font-family:Consolas,Menlo,Monaco,monospace,serif}a{color:#2484c1}a:hover{text-decoration:underline}a img{border:0}hr{color:#ddd;height:1px;border-top:solid 1px #ddd;border-bottom:0;border-left:0;border-right:0}p#heart{font-size:2em;line-height:1;color:#ccc}.red{color:#b50000}body#index li{margin-bottom:1em}@media only screen and (max-device-width:1024px){body{font-size:120%;line-height:1.4}}@media only screen and (max-device-width:480px){body{text-align:left}article,footer{width:auto}article{padding:0 10px}}table tr{border-top:1px solid #ccc;background-color:#fff;margin:0}table tr:nth-child(2n){background-color:#aaa}table tr th{font-weight:700}table tr td:last-child,table tr th :last-child{margin-bottom:0}img{max-width:100%}code,tt{margin:0 2px;padding:0 5px;white-space:nowrap;border:1px solid #eaeaea;background-color:#f8f8f8;border-radius:3px}pre code{margin:0;white-space:pre;border:none;background:0 0}.highlight pre,pre{background-color:#f8f8f8;border:1px solid #ccc;font-size:13px;line-height:19px;overflow:auto;padding:6px 10px;border-radius:3px}'

class CMarkEdMainWindow(QtGui.QMainWindow):
    #Signals:
    connect_stack = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(CMarkEdMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.previewText.setDefaultStyleSheet(foghorn)

    def sourceTextChanged(self):
        rendered = md2html(self.ui.sourceText.toPlainText())
        self.ui.previewText.setHtml(rendered)
        print(rendered)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myMainWindow = CMarkEdMainWindow()
    myMainWindow.show()
    sys.exit(app.exec_())
