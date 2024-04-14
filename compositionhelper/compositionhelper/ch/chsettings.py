# -----------------------------------------------------------------------------
# Composition Helper
# Copyright (C) 2020-2024 - Grum999
# -----------------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
#
# https://spdx.org/licenses/GPL-3.0-or-later.html
# -----------------------------------------------------------------------------
# A Krita plugin designed to add composition helper in documents
# -----------------------------------------------------------------------------

from enum import Enum


from PyQt5.Qt import *
from PyQt5.QtCore import (
        pyqtSignal,
        QSettings,
        QStandardPaths
    )

import os

from compositionhelper.pktk.widgets.wcolorselector import (
        WColorPicker,
        WColorComplementary
    )
from compositionhelper.pktk.modules.settings import (
        Settings,
        SettingsFmt,
        SettingsKey,
        SettingsRule
    )

from .chhelpers import (
        CHHelpers,
        CHHelpersDef
    )


# -----------------------------------------------------------------------------

class CHSettingsValues(object):
    VIEWMODE_LIST = 0
    VIEWMODE_ICON = 1
    VALID_LINE_STYLES = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine]


class CHSettingsKey(SettingsKey):
    HELPER_LAST_USED =                                      'helper.global.lastUsed'
    HELPER_ADD_AS_VL =                                      'helper.global.addAsVectorLayer'
    HELPER_LINE_COLOR =                                     'helper.style.{helperId}.line.color'
    HELPER_LINE_WIDTH =                                     'helper.style.{helperId}.line.width'
    HELPER_LINE_STYLE =                                     'helper.style.{helperId}.line.style'
    HELPER_OPTIONS =                                        'helper.style.{helperId}.options'

    CONFIG_WINDOW_GEOMETRY_SIZE_WIDTH =                     'config.window.geometry.size.width'
    CONFIG_WINDOW_GEOMETRY_SIZE_HEIGHT =                    'config.window.geometry.size.height'
    CONFIG_WINDOW_GEOMETRY_POSITION_X =                     'config.window.geometry.position.x'
    CONFIG_WINDOW_GEOMETRY_POSITION_Y =                     'config.window.geometry.position.y'

    CONFIG_HELPER_COLORPICKER_COMPACT =                     'config.helper.colorPicker.compact'
    CONFIG_HELPER_COLORPICKER_ORIENTATION =                 'config.helper.colorPicker.orientation'
    CONFIG_HELPER_COLORPICKER_PALETTE_VISIBLE =             'config.helper.colorPicker.palette.visible'
    CONFIG_HELPER_COLORPICKER_PALETTE_DEFAULT =             'config.helper.colorPicker.palette.default'
    CONFIG_HELPER_COLORPICKER_CWHEEL_VISIBLE =              'config.helper.colorPicker.colorWheel.visible'
    CONFIG_HELPER_COLORPICKER_CWHEEL_CPREVIEW =             'config.helper.colorPicker.colorWheel.colorPreview'
    CONFIG_HELPER_COLORPICKER_CCOMBINATION =                'config.helper.colorPicker.colorCombination'
    CONFIG_HELPER_COLORPICKER_CCSS =                        'config.helper.colorPicker.colorCss.visible'
    CONFIG_HELPER_COLORPICKER_CCSS_ALPHA =                  'config.helper.colorPicker.colorCssAlpha.checked'
    CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_VISIBLE =         'config.helper.colorPicker.colorSlider.rgb.visible'
    CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_ASPCT =           'config.helper.colorPicker.colorSlider.rgb.asPct'
    CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_VISIBLE =        'config.helper.colorPicker.colorSlider.cmyk.visible'
    CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_ASPCT =          'config.helper.colorPicker.colorSlider.cmyk.asPct'
    CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_VISIBLE =         'config.helper.colorPicker.colorSlider.hsl.visible'
    CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_ASPCT =           'config.helper.colorPicker.colorSlider.hsl.asPct'
    CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_VISIBLE =         'config.helper.colorPicker.colorSlider.hsv.visible'
    CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_ASPCT =           'config.helper.colorPicker.colorSlider.hsv.asPct'
    CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_VISIBLE =       'config.helper.colorPicker.colorSlider.alpha.visible'
    CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_ASPCT =         'config.helper.colorPicker.colorSlider.alpha.asPct'

    CONFIG_SETUPMANAGER_ZOOMLEVEL =                         'config.setupManager.zoomLevel'
    CONFIG_SETUPMANAGER_COLUMNWIDTH =                       'config.setupManager.columnWidth'
    CONFIG_SETUPMANAGER_PROPERTIES_DLGBOX_ICON_VIEWMODE =   'config.setupManager.properties.dlgBox.icon.viewMode'
    CONFIG_SETUPMANAGER_PROPERTIES_DLGBOX_ICON_ZOOMLEVEL =  'config.setupManager.properties.dlgBox.icon.zoomLevel'
    CONFIG_SETUPMANAGER_PROPERTIES_DLGBOX_COLORPICKER =     'config.setupManager.properties.dlgBox.colorPicker'
    CONFIG_SETUPMANAGER_LASTFILE =                          'config.setupManager.lastFile'
    CONFIG_SETUPMANAGER_COLORPICKER_COMPACT =               'config.setupManager.colorPicker.compact'
    CONFIG_SETUPMANAGER_COLORPICKER_ORIENTATION =           'config.setupManager.colorPicker.orientation'
    CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_VISIBLE =       'config.setupManager.colorPicker.palette.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_DEFAULT =       'config.setupManager.colorPicker.palette.default'
    CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_VISIBLE =        'config.setupManager.colorPicker.colorWheel.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_CPREVIEW =       'config.setupManager.colorPicker.colorWheel.colorPreview'
    CONFIG_SETUPMANAGER_COLORPICKER_CCOMBINATION =          'config.setupManager.colorPicker.colorCombination'
    CONFIG_SETUPMANAGER_COLORPICKER_CCSS =                  'config.setupManager.colorPicker.colorCss.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_VISIBLE =   'config.setupManager.colorPicker.colorSlider.rgb.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_ASPCT =     'config.setupManager.colorPicker.colorSlider.rgb.asPct'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_VISIBLE =  'config.setupManager.colorPicker.colorSlider.cmyk.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_ASPCT =    'config.setupManager.colorPicker.colorSlider.cmyk.asPct'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_VISIBLE =   'config.setupManager.colorPicker.colorSlider.hsl.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_ASPCT =     'config.setupManager.colorPicker.colorSlider.hsl.asPct'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_VISIBLE =   'config.setupManager.colorPicker.colorSlider.hsv.visible'
    CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_ASPCT =     'config.setupManager.colorPicker.colorSlider.hsv.asPct'


class CHSettings(Settings):
    """Manage all Composition Helper settings

    Configuration is saved as JSON file
    """

    def __init__(self, pluginId=None):
        """Initialise settings"""
        if pluginId is None or pluginId == '':
            pluginId = 'compositionhelper'

        helperIds = list(CHHelpersDef.HELPERS.keys())

        # define current rules for options
        rules = [
            SettingsRule(CHSettingsKey.HELPER_LAST_USED,                                    CHHelpers.GOLDEN_RECTANGLE,           SettingsFmt(str, helperIds)),
            SettingsRule(CHSettingsKey.HELPER_ADD_AS_VL,                                    True,                                 SettingsFmt(bool)),

            SettingsRule(CHSettingsKey.CONFIG_WINDOW_GEOMETRY_SIZE_WIDTH,                   0,  SettingsFmt(int)),
            SettingsRule(CHSettingsKey.CONFIG_WINDOW_GEOMETRY_SIZE_HEIGHT,                  0,  SettingsFmt(int)),
            SettingsRule(CHSettingsKey.CONFIG_WINDOW_GEOMETRY_POSITION_X,                   0,  SettingsFmt(int)),
            SettingsRule(CHSettingsKey.CONFIG_WINDOW_GEOMETRY_POSITION_Y,                   0,  SettingsFmt(int)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_COMPACT,                   True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_ORIENTATION,               WColorPicker.OPTION_ORIENTATION_VERTICAL,
                                                                                            SettingsFmt(int, [WColorPicker.OPTION_ORIENTATION_VERTICAL,
                                                                                                              WColorPicker.OPTION_ORIENTATION_HORIZONTAL
                                                                                                              ]
                                                                                            )),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_PALETTE_VISIBLE,           True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_PALETTE_DEFAULT,           "Default", SettingsFmt(str)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CWHEEL_VISIBLE,            False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CWHEEL_CPREVIEW,           True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCOMBINATION,              WColorComplementary.COLOR_COMBINATION_NONE,
                                                                                            SettingsFmt(int, [WColorComplementary.COLOR_COMBINATION_NONE,
                                                                                                              WColorComplementary.COLOR_COMBINATION_MONOCHROMATIC,
                                                                                                              WColorComplementary.COLOR_COMBINATION_COMPLEMENTARY,
                                                                                                              WColorComplementary.COLOR_COMBINATION_ANALOGOUS,
                                                                                                              WColorComplementary.COLOR_COMBINATION_TRIADIC,
                                                                                                              WColorComplementary.COLOR_COMBINATION_TETRADIC
                                                                                                              ]
                                                                                            )),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCSS,                      True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCSS_ALPHA,                True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_VISIBLE,       True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_ASPCT,         False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_VISIBLE,      False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_ASPCT,        False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_VISIBLE,       False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_ASPCT,         False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_VISIBLE,       False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_ASPCT,         False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_VISIBLE,     False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_ASPCT,       False,     SettingsFmt(bool)),

            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_LASTFILE,                         '', SettingsFmt(str)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_ZOOMLEVEL,                        3,  SettingsFmt(int, [0, 1, 2, 3, 4])),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLUMNWIDTH,                     -1, SettingsFmt(int)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_PROPERTIES_DLGBOX_ICON_ZOOMLEVEL, 3, SettingsFmt(int, [0, 1, 2, 3, 4, 5, 6])),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_PROPERTIES_DLGBOX_ICON_VIEWMODE,  CHSettingsValues.VIEWMODE_LIST,
                                                                                             SettingsFmt(int,
                                                                                                         [CHSettingsValues.VIEWMODE_LIST,
                                                                                                          CHSettingsValues.VIEWMODE_ICON
                                                                                                          ]
                                                                                                         ),
                         ),

            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_COMPACT,              True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_ORIENTATION,          WColorPicker.OPTION_ORIENTATION_VERTICAL,
                                                                                             SettingsFmt(int, [WColorPicker.OPTION_ORIENTATION_VERTICAL,
                                                                                                               WColorPicker.OPTION_ORIENTATION_HORIZONTAL
                                                                                                               ]
                                                                                             )),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_VISIBLE,      True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_DEFAULT,      "Default", SettingsFmt(str)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_VISIBLE,       False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_CPREVIEW,      True,      SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CCOMBINATION,         WColorComplementary.COLOR_COMBINATION_NONE,
                                                                                             SettingsFmt(int, [WColorComplementary.COLOR_COMBINATION_NONE,
                                                                                                               WColorComplementary.COLOR_COMBINATION_MONOCHROMATIC ,
                                                                                                               WColorComplementary.COLOR_COMBINATION_COMPLEMENTARY,
                                                                                                               WColorComplementary.COLOR_COMBINATION_ANALOGOUS,
                                                                                                               WColorComplementary.COLOR_COMBINATION_TRIADIC,
                                                                                                               WColorComplementary.COLOR_COMBINATION_TETRADIC
                                                                                                               ]
                                                                                             )),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CCSS,                 False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_VISIBLE,  False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_ASPCT,    False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_VISIBLE, False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_ASPCT,   False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_VISIBLE,  False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_ASPCT,    False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_VISIBLE,  False,     SettingsFmt(bool)),
            SettingsRule(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_ASPCT,    False,     SettingsFmt(bool)),
            ]

        for helperId in helperIds:
            rules += [
                SettingsRule(CHSettingsKey.HELPER_LINE_COLOR.id(helperId=helperId),          '#ff00aa00',   SettingsFmt(str)),
                SettingsRule(CHSettingsKey.HELPER_LINE_WIDTH.id(helperId=helperId),          2.0,           SettingsFmt(float)),
                SettingsRule(CHSettingsKey.HELPER_LINE_STYLE.id(helperId=helperId),          Qt.SolidLine,  SettingsFmt(int, CHSettingsValues.VALID_LINE_STYLES)),
                SettingsRule(CHSettingsKey.HELPER_OPTIONS.id(helperId=helperId),             CHHelpersDef.HELPERS[helperId]['options']['default'],  SettingsFmt(list))
                ]

        super(CHSettings, self).__init__(pluginId, rules)

    @staticmethod
    def getTxtColorPickerLayout():
        """Convert picker layout from settings to layout"""
        # build a dummy color picker
        tmpColorPicker = WColorPicker()
        tmpColorPicker.setConstraintSize(True)
        tmpColorPicker.setOptionCompactUi(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_COMPACT))
        tmpColorPicker.setOptionOrientation(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_ORIENTATION))
        tmpColorPicker.setOptionShowColorPalette(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_VISIBLE))
        tmpColorPicker.setOptionColorPalette(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_DEFAULT))
        tmpColorPicker.setOptionShowColorWheel(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_VISIBLE))
        tmpColorPicker.setOptionShowPreviewColor(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_CPREVIEW))
        tmpColorPicker.setOptionShowColorCombination(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CCOMBINATION))
        tmpColorPicker.setOptionShowCssRgb(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CCSS))
        tmpColorPicker.setOptionShowColorRGB(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorRGB(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_ASPCT))
        tmpColorPicker.setOptionShowColorCMYK(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorCMYK(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_ASPCT))
        tmpColorPicker.setOptionShowColorHSV(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorHSV(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_ASPCT))
        tmpColorPicker.setOptionShowColorHSL(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorHSL(CHSettings.get(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_ASPCT))
        tmpColorPicker.setOptionShowColorAlpha(False)
        return tmpColorPicker.optionLayout()

    @staticmethod
    def setTxtColorPickerLayout(layout):
        """Convert color picker layout from settings to layout"""
        # build a dummy color picker
        tmpColorPicker = WColorPicker()
        tmpColorPicker.setOptionLayout(layout)

        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_COMPACT, tmpColorPicker.optionCompactUi())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_ORIENTATION, tmpColorPicker.optionOrientation())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_VISIBLE, tmpColorPicker.optionShowColorPalette())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_PALETTE_DEFAULT, tmpColorPicker.optionColorPalette())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_VISIBLE, tmpColorPicker.optionShowColorWheel())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CWHEEL_CPREVIEW, tmpColorPicker.optionShowPreviewColor())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CCOMBINATION, tmpColorPicker.optionShowColorCombination())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CCSS, tmpColorPicker.optionShowColorCssRGB())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_VISIBLE, tmpColorPicker.optionShowColorRGB())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_RGB_ASPCT, tmpColorPicker.optionDisplayAsPctColorRGB())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_VISIBLE, tmpColorPicker.optionShowColorCMYK())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_CMYK_ASPCT, tmpColorPicker.optionDisplayAsPctColorCMYK())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_VISIBLE, tmpColorPicker.optionShowColorHSL())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSL_ASPCT, tmpColorPicker.optionDisplayAsPctColorHSL())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_VISIBLE, tmpColorPicker.optionShowColorHSV())
        CHSettings.set(CHSettingsKey.CONFIG_SETUPMANAGER_COLORPICKER_CSLIDER_HSV_ASPCT, tmpColorPicker.optionDisplayAsPctColorHSV())

    @staticmethod
    def getHelperColorPickerLayout():
        """Convert picker layout from settings to layout"""
        # build a dummy color picker
        tmpColorPicker = WColorPicker()
        tmpColorPicker.setConstraintSize(True)
        tmpColorPicker.setOptionCompactUi(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_COMPACT))
        tmpColorPicker.setOptionOrientation(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_ORIENTATION))
        tmpColorPicker.setOptionShowColorPalette(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_PALETTE_VISIBLE))
        tmpColorPicker.setOptionColorPalette(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_PALETTE_DEFAULT))
        tmpColorPicker.setOptionShowColorWheel(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CWHEEL_VISIBLE))
        tmpColorPicker.setOptionShowPreviewColor(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CWHEEL_CPREVIEW))
        tmpColorPicker.setOptionShowColorCombination(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCOMBINATION))
        tmpColorPicker.setOptionShowColorRGB(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorRGB(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_ASPCT))
        tmpColorPicker.setOptionShowColorCMYK(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorCMYK(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_ASPCT))
        tmpColorPicker.setOptionShowColorHSV(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorHSV(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_ASPCT))
        tmpColorPicker.setOptionShowColorHSL(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorHSL(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_ASPCT))
        tmpColorPicker.setOptionShowColorAlpha(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_VISIBLE))
        tmpColorPicker.setOptionDisplayAsPctColorAlpha(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_ASPCT))
        tmpColorPicker.setOptionShowCssRgb(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCSS))
        tmpColorPicker.setOptionShowCssRgbAlphaChecked(CHSettings.get(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCSS_ALPHA))
        return tmpColorPicker.optionLayout()

    @staticmethod
    def setHelperColorPickerLayout(layout):
        """Convert color picker layout from settings to layout"""
        # build a dummy color picker
        tmpColorPicker = WColorPicker()
        tmpColorPicker.setOptionLayout(layout)
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_COMPACT, tmpColorPicker.optionCompactUi())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_ORIENTATION, tmpColorPicker.optionOrientation())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_PALETTE_VISIBLE, tmpColorPicker.optionShowColorPalette())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_PALETTE_DEFAULT, tmpColorPicker.optionColorPalette())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CWHEEL_VISIBLE, tmpColorPicker.optionShowColorWheel())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CWHEEL_CPREVIEW, tmpColorPicker.optionShowPreviewColor())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCOMBINATION, tmpColorPicker.optionShowColorCombination())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_VISIBLE, tmpColorPicker.optionShowColorRGB())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_RGB_ASPCT, tmpColorPicker.optionDisplayAsPctColorRGB())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_VISIBLE, tmpColorPicker.optionShowColorCMYK())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_CMYK_ASPCT, tmpColorPicker.optionDisplayAsPctColorCMYK())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_VISIBLE, tmpColorPicker.optionShowColorHSL())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSL_ASPCT, tmpColorPicker.optionDisplayAsPctColorHSL())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_VISIBLE, tmpColorPicker.optionShowColorHSV())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_HSV_ASPCT, tmpColorPicker.optionDisplayAsPctColorHSV())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_VISIBLE, tmpColorPicker.optionShowColorAlpha())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CSLIDER_ALPHA_ASPCT, tmpColorPicker.optionDisplayAsPctColorAlpha())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCSS, tmpColorPicker.optionShowColorCssRGB())
        CHSettings.set(CHSettingsKey.CONFIG_HELPER_COLORPICKER_CCSS_ALPHA, tmpColorPicker.optionShowCssRgbAlphaChecked())
