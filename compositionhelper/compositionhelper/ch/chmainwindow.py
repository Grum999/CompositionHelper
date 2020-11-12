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
# A Krita plugin designed to manage documents
# -----------------------------------------------------------------------------

import os
from krita import Krita

import PyQt5.uic

from PyQt5.Qt import *
from PyQt5.QtWidgets import (
        QDialog,
        QWidget
    )

from .chutils import (
        checkerBoardBrush,
        Debug
    )
from .chwcolorbutton import (
        CHWColorButton
    )

PHI = 1.61803398875

class CHHelpers:
    GOLDEN_RECTANGLE = 'goldrect'
    GOLDEN_SPIRAL = 'goldspi'
    GOLDEN_SPIRAL_SECTION = 'goldspisec'
    GOLDEN_TRIANGLES = 'goldspetr'
    GOLDEN_DIAGONALS = 'goldspidiag'
    GOLDEN_SECTION = 'goldsec'
    RULE_OF_THIRD = 'ro3'
    BASIC_CROSS = 'bascross'
    BASIC_DIAGONALS = 'basdiag'


    OPTION_FLIPV = 'flipV'
    OPTION_FLIPH = 'flipH'
    OPTION_FORCE_GR ='forceGR'

# -----------------------------------------------------------------------------
class CHMainWindow(QDialog):
    """Main Composition Helper window"""
    # A flag to ensure that class is instancied only once
    __OPENED = False

    # helpers key/properties
    __HELPERS = {
            CHHelpers.GOLDEN_RECTANGLE: {
                                        'label': i18n('Golden rectangle'),
                                        'options': {
                                                'available': [],
                                                'default':   [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_SPIRAL: {
                                        'label': i18n('Golden spiral'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FLIPV, CHHelpers.OPTION_FLIPH],
                                                'default':   [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_SPIRAL_SECTION: {
                                        'label': i18n('Golden spiral section'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FLIPV, CHHelpers.OPTION_FLIPH],
                                                'default':   [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_TRIANGLES: {
                                        'label': i18n('Golden triangles'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_FLIPV, CHHelpers.OPTION_FLIPH],
                                                'default':   [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_DIAGONALS: {
                                        'label': i18n('Golden diagonals'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR],
                                                'default':   []
                                            }
                                    },
            CHHelpers.GOLDEN_SECTION: {
                                        'label': i18n('Golden section'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR],
                                                'default':   []
                                            }
                                    },
            CHHelpers.RULE_OF_THIRD: {
                                        'label': i18n('Rule of thirds'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR],
                                                'default':   []
                                            }
                                    },
            CHHelpers.BASIC_CROSS: {
                                        'label': i18n('Basic cross'),
                                        'options': {
                                                'available': [],
                                                'default':   []
                                            }
                                    },
            CHHelpers.BASIC_DIAGONALS: {
                                        'label': i18n('Basic diagonals'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR],
                                                'default':   []
                                            }
                                    }
        }

    # key/names
    __LINE_STYLES = {
            Qt.SolidLine: i18n('Solid'),
            Qt.DashLine: i18n('Dash'),
            Qt.DotLine: i18n('Dot'),
            Qt.DashDotLine: i18n('Dash-Dot'),
            Qt.DashDotDotLine: i18n('Dash-Dot-Dot')
        }

    def __init__(self, chName="Composition Helper", chVersion="testing"):
        super(CHMainWindow, self).__init__(Krita.instance().activeWindow().qwindow())

        # another instance already exist, exit
        self.__opened = False
        if CHMainWindow.__OPENED:
            self.close()
            return

        if Krita.instance().activeDocument() is None:
            # no document opened: cancel plugin
            QMessageBox.warning(
                    QWidget(),
                    f"{chName}",
                    i18n("There's no active document: <i>Composition Helper</i> plugin only works with opened documents")
                )
            self.close()
            return

        uiFileName = os.path.join(os.path.dirname(__file__), 'resources', 'chmainwindow.ui')
        PyQt5.uic.loadUi(uiFileName, self)

        self.setModal(False)
        self.setWindowTitle(i18n(f'{chName} v{chVersion}'))
        self.setWindowFlags(Qt.Dialog|Qt.WindowTitleHint)

        self.__palette = QApplication.palette()
        self.__iconSizeLineStyle = QSize(48,12)
        self.__iconSizeHelper = QSize(128,96)

        # timer is used to update preview content when dialog window is resized
        self.__timerResizeId = 0
        self.__lastResized = QSize(0, 0)

        # document preview: projection from document
        # document resized: projection resized to label dimension andd store as a cache to avoid doing resizing on each
        #                   canvas refresh
        self.__documentPreview = None
        self.__documentResized = None
        # ratio applied between original size and preview size
        self.__documentRatio = 1

        # initialise window
        self.__initialise()

        self.__opened = True
        CHMainWindow.__OPENED = True
        self.show()


    def __initialise(self):
        """Initialise window"""
        def closeWindow(dummy=None):
            # close window
            self.close()

        def updateDsbLineWidth(value):
            # Line width slider value has been modified, update spinbox
            self.dsbLineWidth.setValue(value/100)
            self.__updatePreview()

        def updateHsLineWidth(value):
            # Line width slider value has been modified, update spinbox
            self.hsLineWidth.setValue(int(value*100))
            self.__updatePreview()

        def updateHelper(dummy=None):
            # helper model has been changed, update interface
            currentHelper = self.cbxHelpers.currentData()

            optionsAvailable = CHMainWindow.__HELPERS[currentHelper]['options']['available']
            optionsDefault = CHMainWindow.__HELPERS[currentHelper]['options']['default']

            self.cbForceGR.setEnabled(CHHelpers.OPTION_FORCE_GR in optionsAvailable)
            self.cbForceGR.setChecked(CHHelpers.OPTION_FORCE_GR in optionsDefault)

            self.cbFlipH.setEnabled(CHHelpers.OPTION_FLIPV in optionsAvailable)
            self.cbFlipH.setChecked(CHHelpers.OPTION_FLIPV in optionsDefault)

            self.cbFlipV.setEnabled(CHHelpers.OPTION_FLIPH in optionsAvailable)
            self.cbFlipV.setChecked(CHHelpers.OPTION_FLIPH in optionsDefault)

            self.__updatePreview()

        # build Helper list
        self.cbxHelpers.setIconSize(self.__iconSizeHelper)
        for helper in CHMainWindow.__HELPERS:
            self.cbxHelpers.addItem(self.__buildHelperIcon(helper), f" {CHMainWindow.__HELPERS[helper]['label']}", helper)
        self.cbxHelpers.currentIndexChanged.connect(updateHelper)

        # link line width slider<>spinbox
        self.hsLineWidth.valueChanged.connect(updateDsbLineWidth)
        self.dsbLineWidth.valueChanged.connect(updateHsLineWidth)

        # build line style list
        self.cbxLineStyle.setIconSize(self.__iconSizeLineStyle)
        for lineStyle in CHMainWindow.__LINE_STYLES:
            self.cbxLineStyle.addItem(self.__buildLineIcon(lineStyle), f" {CHMainWindow.__LINE_STYLES[lineStyle]}", lineStyle)
        self.cbxLineStyle.currentIndexChanged.connect(self.__updatePreview)

        # set line color button
        self.pbLineColor.clicked.connect(self.__updatePreview)

        # options
        self.cbForceGR.toggled.connect(self.__updatePreview)
        self.cbFlipH.toggled.connect(self.__updatePreview)
        self.cbFlipV.toggled.connect(self.__updatePreview)

        # button 'add'
        self.pbAdd.clicked.connect(self.addHelper)

        # button 'close'
        self.pbClose.clicked.connect(closeWindow)

        # update preview automatically
        self.lblPreview.paintEvent = self.__lblPreviewPaint
        self.lblPreview.resizeEvent = self.__lblPreviewResize

        self.__updateDocumentPreview()
        updateHelper()


    def __buildLineIcon(self, lineStyle):
        """Build a QIcon with lineStyle"""
        pixmap=QPixmap(self.__iconSizeLineStyle)
        pixmap.fill(Qt.transparent)

        pen = QPen(lineStyle)
        pen.setWidth(2)
        pen.setColor(self.__palette.color(QPalette.ButtonText))

        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(pen)
        painter.drawLine(0, self.__iconSizeLineStyle.height()//2, self.__iconSizeLineStyle.width(), self.__iconSizeLineStyle.height()//2)
        painter.end()

        return QIcon(pixmap)


    def __buildHelperIcon(self, helper):
        """Build a QIcon with lineStyle"""
        pixmap=QPixmap(self.__iconSizeHelper)
        pixmap.fill(Qt.transparent)

        pen = QPen(Qt.SolidLine)
        pen.setWidth(1.5)
        pen.setColor(self.__palette.color(QPalette.ButtonText))

        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(pen)
        self.__paintHelper(helper, painter, self.__iconSizeHelper, CHMainWindow.__HELPERS[helper]['options']['default'])
        painter.end()

        return QIcon(pixmap)


    def __paintHelper(self, helper, painter, size, options=[]):
        """Paint `helper` on `painter`, using given `size`

        Consider that paint surface is initialised as well as the painter pen
        """
        def getGoldenPosition(rect, fromStartSide=True):
            # return coordinates (as QRectF) to use for golden spiral
            if rect.width()>rect.height():
                if fromStartSide:
                    return (
                        QPoint(rect.left() + rect.height(), rect.top()),
                        QPoint(rect.left() + rect.height(), rect.bottom()),
                        QRectF(QPointF(rect.left() + rect.height(), rect.top()), QPointF(rect.right(), rect.bottom()))
                    )
                else:
                    pX=rect.left() + rect.width() - rect.height()
                    return (
                        QPoint(pX, rect.bottom()),
                        QPoint(pX, rect.top()),
                        QRectF(QPointF(rect.left(), rect.top()), QPointF(pX, rect.bottom()))
                    )
            else:
                if fromStartSide:
                    return (
                        QPoint(rect.right(), rect.top() + rect.width()),
                        QPoint(rect.left(), rect.top() + rect.width()),
                        QRectF(QPointF(rect.left(), rect.top() + rect.width()), QPointF(rect.right(), rect.bottom()))
                    )
                else:
                    pY=rect.top() + rect.height() - rect.width()
                    return (
                        QPoint(rect.left(), pY),
                        QPoint(rect.right(), pY),
                        QRectF(QPointF(rect.left(), rect.top()), QPointF(rect.right(), pY))
                    )

        # save current painter transformations state
        painter.save()

        # lines to draw
        lines=[]

        # w, h => easier to read in code
        w = size.width()
        h = size.height()
        nW = w
        nH = h
        oX = 0
        oY = 0
        scaleX = 1
        scaleY = 1

        if h>w:
            # When height is greater than width, just apply a transformation, don't try to define
            # new calculation ( -- lazy mode ^_^' -- )
            h, w = w, h
            nH, nW = nW, nH
            painter.rotate(90)
            painter.translate(0, -nH)

            # due to rotation, need to invert flip V/H
            nOptions=[]
            if CHHelpers.OPTION_FLIPH in options:
                nOptions.append(CHHelpers.OPTION_FLIPV)
            if CHHelpers.OPTION_FLIPV in options:
                nOptions.append(CHHelpers.OPTION_FLIPH)
            if CHHelpers.OPTION_FORCE_GR in options:
                nOptions.append(CHHelpers.OPTION_FORCE_GR)
            options=nOptions

        if CHHelpers.OPTION_FORCE_GR in options:
            # Force to respect golden ratio
            # calculate new width/height + offset for constrained golden ratio
            if (w/h) >= PHI:
                nW = h * PHI
                nH = h
                oX = (w - nW)/2
            else:
                nW = w
                nH = w / PHI
                oY = (h - nH)/2

        if oX != 0 or oY != 0:
            painter.translate(oX, oY)

        if CHHelpers.OPTION_FLIPH in options:
            scaleX = -1
        if CHHelpers.OPTION_FLIPV in options:
            scaleY = -1

        if scaleX != 1 or scaleY != 1:
            painter.scale(scaleX, scaleY)
            tX=0
            if scaleX != 1:
                tX=-nW
            tY=0
            if scaleY != 1:
                tY=-nH
            painter.translate(tX, tY)

        if helper == CHHelpers.RULE_OF_THIRD:
            pX=nW/3
            pY=nH/3
            lines.append(QLineF(pX, 0, pX, nH))
            lines.append(QLineF(nW - pX, 0, nW - pX, nH))

            lines.append(QLineF(0, pY, nW, pY))
            lines.append(QLineF(0, nH - pY, nW, nH - pY))
        elif helper == CHHelpers.GOLDEN_RECTANGLE:
            painter.drawRect(0, 0, nW, nH)
        elif helper == CHHelpers.GOLDEN_SECTION:
            pX=nW/(1+PHI)
            pY=nH/(1+PHI)

            lines.append(QLineF(pX, 0, pX, nH))
            lines.append(QLineF(nW - pX, 0, nW - pX, nH))

            lines.append(QLineF(0, pY, nW, pY))
            lines.append(QLineF(0, nH - pY, nW, nH - pY))
        elif helper == CHHelpers.GOLDEN_SPIRAL:
            # start spiral path
            spiralPath=QPainterPath()
            spiralPath.moveTo(0, 0)

            # fromStart is used to determinate from which side golden section have to be calculated
            fromStart = 1
            startAngle=180
            r = getGoldenPosition(QRectF(0, 0, nW, nH), True)

            # arbitrary define 8 sections...
            for number in range(8):
                # hD = Diameter for spiral arc
                hD = 2 * (abs(r[0].y() - r[1].y()) + abs(r[0].x() - r[1].x()))
                spiralPath.arcTo(QRectF(QPointF(r[0].x() - hD/2, r[0].y() - hD/2), QSizeF(hD, hD)), startAngle, 90 )

                # prepare next arc/golden section
                fromStart+=1
                startAngle+=90
                if fromStart>=4:
                    fromStart=0
                elif fromStart==1:
                    startAngle=180
                r = getGoldenPosition(r[2], (fromStart<=1))
            # draw spiral
            painter.drawPath(spiralPath)
        elif helper == CHHelpers.GOLDEN_SPIRAL_SECTION:
            # fromStart is used to determinate from which side golden section have to be calculated
            fromStart = 1
            r = getGoldenPosition(QRectF(0, 0, nW, nH), True)

            # arbitrary define 8 sections...
            for number in range(8):
                lines.append(QLineF(r[0], r[1]))

                # prepare next arc/golden section
                fromStart+=1
                if fromStart>=4:
                    fromStart=0
                r = getGoldenPosition(r[2], (fromStart<=1))
        elif helper == CHHelpers.GOLDEN_TRIANGLES:
            lines.append(QLineF(0, 0, nW, nH))
            pX=nW/(1+PHI)
            pY=nH/(1+PHI)

            lines.append(QLineF(0, nH, pX, 0))
            lines.append(QLineF(nW, 0, nW - pX, nH))
        elif helper == CHHelpers.GOLDEN_DIAGONALS:
            dX=nW - nH
            lines.append(QLineF(0, 0, nH, nH))
            lines.append(QLineF(0, nH, nH, 0))

            lines.append(QLineF(dX, 0, dX + nH, nH))
            lines.append(QLineF(dX, nH, dX + nH, 0))
        elif helper == CHHelpers.BASIC_CROSS:
            mX=nW/2
            mY=nH/2
            lines.append(QLineF(mX, 0, mX, nH))
            lines.append(QLineF(0, mY, nW, mY))
        elif helper == CHHelpers.BASIC_DIAGONALS:
            lines.append(QLineF(0, 0, nW, nH))
            lines.append(QLineF(0, nH, nW, 0))

        painter.drawLines(lines)

        # restore current painter transformations state
        painter.restore()


    def __lblPreviewPaint(self, event):
        """Update label preview"""
        # Method is paintEvent() for widget lblPreview

        if self.__documentResized is None:
            return

        # ----------------------------------------------------------------------
        # start rendering paper
        painter = QPainter(self.lblPreview)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.lblPreview.rect() , Qt.NoBrush)

        # position for picture
        pX = (self.lblPreview.width() - self.__documentResized.width())/2
        pY = (self.lblPreview.height() - self.__documentResized.height())/2

        painter.translate(pX, pY)

        # draw a checkboard as background, usefull for picture with alpha channel
        painter.fillRect(QRect(0, 0, self.__documentResized.width(), self.__documentResized.height()), checkerBoardBrush())

        # picture from cache
        painter.drawImage(0, 0, self.__documentResized)

        # initialise pen according to UI
        painter.setPen(self.__getPen(self.__documentRatio))

        # -- draw helper
        self.__paintHelper(self.cbxHelpers.currentData(), painter, self.__documentResized.size(), self.__getOptions())


    def __lblPreviewResize(self, event=None):
        """Label has been resized"""
        # can't update self.__documentResized QImage on each event because it's slow down the interface
        # so implement a timer of 250ms
        # if timer reach timeout, then trigger timerEvent() and calculate new dimension and refresh preview
        # otherwise, if event occurs while timeout isn't reached, reinitialise timer
        if self.__timerResizeId!=0:
            self.killTimer(self.__timerResizeId)
            self.__timerResizeId=0

        self.__timerResizeId=self.startTimer(250)


    def __updateDocumentPreview(self):
        """Retrieve current document projection and refresh preview"""
        document=Krita.instance().activeDocument()
        self.__documentPreview = document.projection(0, 0, document.width(), document.height())
        self.__updateDocumentResized()
        self.__updatePreview()
        self.lblPreview.update()


    def __updateDocumentResized(self):
        """Update resized image of document"""
        self.__lastResized = self.lblPreview.size()
        self.__documentResized=self.__documentPreview.scaled(self.lblPreview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.__documentRatio = self.__documentResized.width() / self.__documentPreview.width()


    def __updatePreview(self, dummy=None):
        """Update preview"""
        self.lblPreview.update()


    def __getPen(self, penWidthRatio=1):
        """Return a QPen according to current configuration"""
        pen = QPen(self.pbLineColor.color())
        pen.setStyle(self.cbxLineStyle.currentData())
        pen.setWidth(max(0.75, self.dsbLineWidth.value() * penWidthRatio))
        return pen


    def __getOptions(self):
        """Return option list according to current configuration"""
        returned=[]
        if self.cbForceGR.isChecked():
            returned.append(CHHelpers.OPTION_FORCE_GR)
        if self.cbFlipV.isChecked():
            returned.append(CHHelpers.OPTION_FLIPV)
        if self.cbFlipH.isChecked():
            returned.append(CHHelpers.OPTION_FLIPH)

        return returned


    def showEvent(self, event):
        """Event trigerred when dialog is shown

        At this time, all widgets are initialised and size/visiblity is known
        """
        self.__updateDocumentPreview()


    def timerEvent(self, event):
        """Print resize timeout occured"""
        # timeout initialized during resize has been reached
        self.__timerResizeId=0

        if not self.__documentPreview is None and self.__lastResized != self.lblPreview.size():
            # calculate new dimension + refresh preview only if size has been modified
            self.__updateDocumentResized()
            self.__updatePreview()
            self.lblPreview.update()


    def closeEvent(self, event):
        """Window is closed"""
        if self.__opened:
            CHMainWindow.__OPENED = False


    def addHelper(self):
        """Add Helper do current document"""
        Debug.print("Add helper: not yet implemented")


Debug.setEnabled(True)