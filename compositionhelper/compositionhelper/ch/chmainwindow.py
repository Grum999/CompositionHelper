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

from .chhelpers import (
        CHHelpers,
        CHHelpersDef
    )
from .chutils import (
        checkerBoardBrush
    )
from .chabout import (
        CHAboutWindow
    )
from .chsettings import (
        CHSettings,
        CHSettingsKey
    )
from .chwcolorbutton import (
        CHWColorButton
    )
from ..pktk.ekrita import (
        EKritaDocument,
        EKritaNode
    )

# Define Golden number value
PHI = 1.61803398875


# -----------------------------------------------------------------------------
class CHMainWindow(QDialog):
    """Main Composition Helper window"""
    # A flag to ensure that class is instancied only once
    __OPENED = False

    # key/names
    __LINE_STYLES = {
            Qt.SolidLine: i18n('Solid'),
            Qt.DashLine: i18n('Dash'),
            Qt.DotLine: i18n('Dot'),
            Qt.DashDotLine: i18n('Dash-Dot'),
            Qt.DashDotDotLine: i18n('Dash-Dot-Dot')
        }

    # default group layers name
    __LAYER_GROUP = 'CH# Composition Helpers'

    def __init__(self, chName="Composition Helper", chVersion="testing"):
        super(CHMainWindow, self).__init__(Krita.instance().activeWindow().qwindow())

        # another instance already exist, exit
        self.__chName = chName
        self.__chVersion = chVersion

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

        self.__documentSelection = None

        self.__settings = CHSettings()
        self.__settings.loadConfig()

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


            # get default value from config
            optionsSettings = self.__settings.option(CHSettingsKey.HELPER_OPTIONS.id(helperId=currentHelper))

            optionsAvailable = CHHelpersDef.HELPERS[currentHelper]['options']['available']
            optionsForced=CHHelpersDef.HELPERS[currentHelper]['options']['forced']

            self.pbLineColor.setColor(self.__settings.option(CHSettingsKey.HELPER_LINE_COLOR.id(helperId=currentHelper)))
            self.cbxLineStyle.setCurrentIndex(list(CHMainWindow.__LINE_STYLES.keys()).index(self.__settings.option(CHSettingsKey.HELPER_LINE_STYLE.id(helperId=currentHelper))))
            self.dsbLineWidth.setValue(self.__settings.option(CHSettingsKey.HELPER_LINE_WIDTH.id(helperId=currentHelper)))

            self.cbForceGR.setEnabled(CHHelpers.OPTION_FORCE_GR in optionsAvailable)
            if self.cbForceGR.isEnabled():
                self.cbForceGR.setChecked(CHHelpers.OPTION_FORCE_GR in optionsSettings)
            else:
                # forced value?
                self.cbForceGR.setChecked(CHHelpers.OPTION_FORCE_GR in optionsForced)

            self.cbFlipH.setEnabled(CHHelpers.OPTION_FLIPV in optionsAvailable)
            if self.cbFlipH.isEnabled():
                self.cbFlipH.setChecked(CHHelpers.OPTION_FLIPV in optionsSettings)
            else:
                # forced value?
                self.cbFlipH.setChecked(CHHelpers.OPTION_FLIPV in optionsForced)

            self.cbFlipV.setEnabled(CHHelpers.OPTION_FLIPH in optionsAvailable)
            if self.cbFlipV.isEnabled():
                self.cbFlipV.setChecked(CHHelpers.OPTION_FLIPH in optionsSettings)
            else:
                # forced value?
                self.cbFlipV.setChecked(CHHelpers.OPTION_FLIPH in optionsForced)

            self.cbUseSelection.setChecked(CHHelpers.OPTION_USE_SELECTION in optionsSettings)

            self.__updatePreview()

        def displayAbout(dummy=None):
            # display about window
            CHAboutWindow(self.__chName, self.__chVersion)

        # build Helper list
        self.cbxHelpers.setIconSize(self.__iconSizeHelper)
        for helper in CHHelpersDef.HELPERS:
            self.cbxHelpers.addItem(self.__buildHelperIcon(helper), f" {CHHelpersDef.HELPERS[helper]['label']}", helper)
        self.cbxHelpers.setCurrentIndex(list(CHHelpersDef.HELPERS.keys()).index(self.__settings.option(CHSettingsKey.HELPER_LAST_USED.id())))
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

        self.cbUseSelection.toggled.connect(self.__updatePreview)
        self.cbUseSelection.setEnabled(False)

        # button 'add'
        self.pbAdd.clicked.connect(self.addHelperLayer)

        # button 'close'
        self.pbClose.clicked.connect(closeWindow)

        self.pbAbout.clicked.connect(displayAbout)

        # update preview automatically
        self.lblPreview.paintEvent = self.__lblPreviewPaint
        self.lblPreview.resizeEvent = self.__lblPreviewResize

        self.__appNotifier = Krita.instance().notifier()
        self.__appNotifier.viewClosed.connect(self.__activeViewChanged)
        self.__window = Krita.instance().activeWindow()
        self.__window.activeViewChanged.connect(self.__activeViewChanged)


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
        self.__paintHelper(helper, painter, QRect(QPoint(0,0), self.__iconSizeHelper), CHHelpersDef.HELPERS[helper]['options']['forced'])
        painter.end()

        return QIcon(pixmap)


    def __paintHelper(self, helper, painter, rectArea, options=[]):
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
        w = rectArea.width()
        h = rectArea.height()
        nW = w
        nH = h
        oX = rectArea.x()
        oY = rectArea.y()
        scaleX = 1
        scaleY = 1

        if h>w:
            # When height is greater than width, just apply a transformation, don't try to define
            # new calculation ( -- lazy mode ^_^' -- )
            h, w = w, h
            nH, nW = nW, nH
            oX, oY = oY, -oX
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
                oX += (w - nW)/2
            else:
                nW = w
                nH = w / PHI
                oY += (h - nH)/2

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
        painter.fillRect(self.lblPreview.rect(), Qt.NoBrush)

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

        # define drawing area
        drawRect = self.__documentResized.rect()
        if not self.__documentSelection is None and self.cbUseSelection.isEnabled() and self.cbUseSelection.isChecked():
            drawRect = QRect(int(self.__documentRatio * self.__documentSelection.x()),
                             int(self.__documentRatio * self.__documentSelection.y()),
                             int(self.__documentRatio * self.__documentSelection.width()),
                             int(self.__documentRatio * self.__documentSelection.height()))

        # -- draw helper
        self.__paintHelper(self.cbxHelpers.currentData(), painter, drawRect, self.__getOptions())


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
        if not document is None:
            self.__documentPreview = document.projection(0, 0, document.width(), document.height())
            self.__updateDocumentSelection()
            self.__updateDocumentResized()
            self.__updatePreview()
        else:
            self.__documentPreview = None
            self.__documentResized = None
        self.lblPreview.update()


    def __updateDocumentResized(self):
        """Update resized image of document"""
        if not self.__documentPreview is None:
            self.__lastResized = self.lblPreview.size()
            self.__documentResized=self.__documentPreview.scaled(self.lblPreview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.__documentRatio = self.__documentResized.width() / self.__documentPreview.width()
        else:
            self.__documentPreview = None
            self.__documentResized = None

    def __updateDocumentSelection(self, selection=None):
        document = Krita.instance().activeDocument()
        if not document is None and not (selection:=document.selection()) is None:
            self.cbUseSelection.setEnabled(True)
            if (self.__documentSelection is None or
               selection.x() != self.__documentSelection.x() or
               selection.y() != self.__documentSelection.y() or
               selection.width() != self.__documentSelection.width() or
               selection.height() != self.__documentSelection.height()):
               self.__documentSelection = QRect(selection.x(), selection.y(), selection.width(), selection.height())
               return True
        elif not self.__documentSelection is None:
            self.cbUseSelection.setEnabled(False)
            self.__documentSelection = None
            return True
        return False


    def __updatePreview(self, dummy=None):
        """Update preview"""
        self.lblPreview.update()


    def __getPen(self, penWidthRatio=1):
        """Return a QPen according to current configuration"""
        pen = QPen(self.pbLineColor.color())
        pen.setStyle(self.cbxLineStyle.currentData())
        pen.setWidthF(max(0.75, self.dsbLineWidth.value() * penWidthRatio))
        return pen


    def __getOptions(self, enabledOnly=False):
        """Return option list according to current configuration"""
        returned=[]
        if self.cbForceGR.isChecked():
            if self.cbForceGR.isEnabled() or not enabledOnly:
                returned.append(CHHelpers.OPTION_FORCE_GR)
        if self.cbFlipV.isChecked():
            if self.cbFlipV.isEnabled() or not enabledOnly:
                returned.append(CHHelpers.OPTION_FLIPV)
        if self.cbFlipH.isChecked():
            if self.cbFlipH.isEnabled() or not enabledOnly:
                returned.append(CHHelpers.OPTION_FLIPH)
        if self.cbUseSelection.isChecked():
            # ignore enabledOnly option here
            returned.append(CHHelpers.OPTION_USE_SELECTION)

        return returned


    def __activeViewChanged(self):
        """Called when view/active document has changed"""
        if len(self.__window.views())<=1:
            # if there's no more view opened, close dialog
            # note: it seems that when notifier 'viewClosed' send signale BEFORE
            #       view is closed... then; need to check if current views is
            #       lower OR EQUAL to 1
            self.close()
            return

        self.__updateDocumentPreview()


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
            try:
                self.__window.activeViewChanged.disconnect(self.__activeViewChanged)
            except:
                pass
            try:
                self.__appNotifier.viewClosed.disconnect(self.__activeViewChanged)
            except:
                pass
            CHMainWindow.__OPENED = False


    def enterEvent(self, event):
        """Trigerred when mouse enter above QDialog"""
        # not sure why focusInEvent is not working so use this one
        # maybe not the more elegant way to do it but as there's no event/signal on Document class
        # allowoing to detect selection has been modified (or if exist, was not found :-/)
        #
        # consider, if mouse leave and the enter on QDialog that maybe, the selection in document
        # has been modified
        # so check selection and update things if needed
        #
        document=Krita.instance().activeDocument()
        if (not document is None and
            (document.width() != self.__documentPreview.width() or
             document.height() != self.__documentPreview.height())):
            # document size have been modified
            self.__updateDocumentPreview()
        elif self.__updateDocumentSelection():
            self.__updatePreview()


    def addHelperLayer(self):
        """Add Helper do current document"""
        # check if a group Node for helper alreay exists
        if self.__documentPreview is None:
            return

        helperId = self.cbxHelpers.currentData()

        document = Krita.instance().activeDocument()

        groupNode = EKritaDocument.findFirstLayerByName(document, CHMainWindow.__LAYER_GROUP)

        if groupNode is None:
            # doesn't exist, create a new one
            groupNode = document.createGroupLayer(CHMainWindow.__LAYER_GROUP)
            document.rootNode().addChildNode(groupNode, None)

        newLayer = document.createNode(CHHelpersDef.HELPERS[helperId]['label'], "paintLayer")

        pixmap = QPixmap(self.__documentPreview.size())
        pixmap.fill(Qt.transparent)

        drawRect = pixmap.rect()
        if self.cbUseSelection.isEnabled() and self.cbUseSelection.isChecked():
            drawRect = self.__documentSelection

        pen = self.__getPen()

        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(pen)
        self.__paintHelper(helperId, painter, drawRect, self.__getOptions())
        painter.end()

        EKritaNode.fromQPixmap(newLayer, pixmap)

        groupNode.addChildNode(newLayer, None)
        document.refreshProjection()
        self.__updateDocumentPreview()

        # also update settings when a layers is added (keep in memory that for current helper, the
        # prefered values are current values)
        self.__settings.setOption(CHSettingsKey.HELPER_LAST_USED.id(), helperId)
        self.__settings.setOption(CHSettingsKey.HELPER_LINE_COLOR.id(helperId=helperId), pen.color().name(QColor.HexArgb))
        self.__settings.setOption(CHSettingsKey.HELPER_LINE_STYLE.id(helperId=helperId), pen.style())
        self.__settings.setOption(CHSettingsKey.HELPER_LINE_WIDTH.id(helperId=helperId), pen.widthF())
        self.__settings.setOption(CHSettingsKey.HELPER_OPTIONS.id(helperId=helperId), self.__getOptions(True))
        self.__settings.saveConfig()

