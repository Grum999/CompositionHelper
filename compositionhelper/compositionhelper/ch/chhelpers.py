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
    OPTION_USE_SELECTION ='useSelection'


class CHHelpersDef:
    # helpers key/properties
    HELPERS = {
            CHHelpers.GOLDEN_RECTANGLE: {
                                        'label': i18n('Golden rectangle'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_SPIRAL: {
                                        'label': i18n('Golden spiral'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FLIPV, CHHelpers.OPTION_FLIPH, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_SPIRAL_SECTION: {
                                        'label': i18n('Golden spiral section'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FLIPV, CHHelpers.OPTION_FLIPH, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    [CHHelpers.OPTION_FORCE_GR]
                                            }
                                    },
            CHHelpers.GOLDEN_TRIANGLES: {
                                        'label': i18n('Golden triangles'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_FLIPV, CHHelpers.OPTION_FLIPH, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [CHHelpers.OPTION_FORCE_GR],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.GOLDEN_DIAGONALS: {
                                        'label': i18n('Golden diagonals'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.GOLDEN_SECTION: {
                                        'label': i18n('Golden section'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.RULE_OF_THIRD: {
                                        'label': i18n('Rule of thirds'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.BASIC_CROSS: {
                                        'label': i18n('Basic cross'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.BASIC_DIAGONALS: {
                                        'label': i18n('Basic diagonals'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    }
        }


