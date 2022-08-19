#-----------------------------------------------------------------------------
# Composition Helper
# Copyright (C) 2020 - Grum999
# -----------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see https://www.gnu.org/licenses/
# -----------------------------------------------------------------------------
# A Krita plugin designed to add composition helper in documents
# -----------------------------------------------------------------------------

import os
import re
import sys
import time

import PyQt5.uic

from krita import (
        Extension,
        Krita
    )

from PyQt5.Qt import *
from PyQt5 import QtCore
from PyQt5.QtCore import (
        pyqtSlot
    )

if __name__ != '__main__':
     # script is executed from Krita, loaded as a module
    __PLUGIN_EXEC_FROM__ = 'KRITA'

    from .pktk.pktk import (
            EInvalidStatus,
            EInvalidType,
            EInvalidValue,
            PkTk
        )
    from .ch.chutils import checkKritaVersion
    from .ch.chmainwindow import CHMainWindow
else:
    # Execution from 'Scripter' plugin?
    __PLUGIN_EXEC_FROM__ = 'SCRIPTER_PLUGIN'

    from importlib import reload

    print("======================================")
    print(f'Execution from {__PLUGIN_EXEC_FROM__}')

    for module in list(sys.modules.keys()):
        if not re.search(r'^compositionhelper\.', module) is None:
            print('Reload module {0}: {1}', module, sys.modules[module])
            reload(sys.modules[module])

    from compositionhelper.pktk.pktk import (
            EInvalidStatus,
            EInvalidType,
            EInvalidValue,
            PkTk
        )
    from compositionhelper.ch.chutils import checkKritaVersion
    from compositionhelper.ch.chmainwindow import CHMainWindow

    print("======================================")


EXTENSION_ID = 'pykrita_compositionhelper'
PLUGIN_VERSION = '1.1.2'
PLUGIN_MENU_ENTRY = 'Composition Helper'

REQUIRED_KRITA_VERSION = (4, 4, 0)


class CompositionHelper(Extension):

    def __init__(self, parent):
        # Default options

        # Always initialise the superclass.
        # This is necessary to create the underlying C++ object
        super().__init__(parent)
        self.parent = parent
        self.__uiController = None
        self.__isKritaVersionOk = checkKritaVersion(*REQUIRED_KRITA_VERSION)


    def setup(self):
        """Is executed at Krita's startup"""
        pass


    def createActions(self, window):
        action = window.createAction(EXTENSION_ID, PLUGIN_MENU_ENTRY, "tools/scripts")
        action.triggered.connect(self.start)


    def start(self):
        """Execute Composition Helper"""
        # ----------------------------------------------------------------------
        # Create dialog box
        if not self.__isKritaVersionOk:
            QMessageBox.information(QWidget(),
                                      PLUGIN_MENU_ENTRY,
                                      "At least, Krita version {0} is required to use plugin...".format('.'.join([str(v) for v in REQUIRED_KRITA_VERSION]))
                                    )
            return

        CHMainWindow(PLUGIN_MENU_ENTRY, PLUGIN_VERSION)

if __PLUGIN_EXEC_FROM__ == 'SCRIPTER_PLUGIN':
    sys.stdout = sys.__stdout__

    # Disconnect signals if any before assigning new signals

    ch=CompositionHelper(Krita.instance())
    ch.setup()
    ch.start()
