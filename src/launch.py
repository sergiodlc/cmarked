#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('CMarkEd')
log.setLevel(logging.INFO)

from PySide import QtGui

try:
    from main import CMarkEdMainWindow, __version__
except ImportError:
    from cmarked.main import CMarkEdMainWindow, __version__

def main():

    # Display version and exit (if requested)
    if "--version" in sys.argv:
        print("CMarkEd version %s" % __version__)
        exit()

    log.info("------------------------------------------------")
    log.info("   CMarkEd (version %s)" % __version__ )
    log.info("------------------------------------------------")

    app = QtGui.QApplication(sys.argv)
    myMainWindow = CMarkEdMainWindow()
    myMainWindow.setWindowTitle(myMainWindow.appTitle + " - new_common_mark.md[*]")
    myMainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
