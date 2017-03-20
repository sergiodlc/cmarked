#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('CMarkEd')
log.setLevel(logging.INFO)

from PySide import QtGui

from . import main

#try:
#    from main import CMarkEdMainWindow, __version__
#except ImportError:
#    from cmarked.main import CMarkEdMainWindow, __version__

def _main():

    # Display version and exit (if requested)
    if "--version" in sys.argv:
        print("CMarkEd version %s" % main.__version__)
        exit()

    log.info("------------------------------------------------")
    log.info("   CMarkEd (version %s)" % main.__version__ )
    log.info("------------------------------------------------")

    app = QtGui.QApplication(sys.argv)
    myMainWindow = main.CMarkEdMainWindow()
    myMainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    _main()
