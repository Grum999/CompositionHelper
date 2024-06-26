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
    DYNAMIC_SYMMETRY = 'dynsym'
    DYNAMIC_SYMMETRY_GS = 'dynsymgs'
    RECIPROCAL_LINES = 'reciproclines'
    RECIPROCAL_LINES_GS = 'reciproclinesgs'
    BASIC_DIAMOND = 'basdiamond'
    BASIC_QUARTERS = 'basquarters'

    OPTION_FLIPV = 'flipV'
    OPTION_FLIPH = 'flipH'
    OPTION_FORCE_GR = 'forceGR'
    OPTION_USE_SELECTION = 'useSelection'


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
            CHHelpers.BASIC_QUARTERS: {
                                        'label': i18n('Quarters'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.BASIC_CROSS: {
                                        'label': i18n('Central cross'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.BASIC_DIAGONALS: {
                                        'label': i18n('Diagonals'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.BASIC_DIAMOND: {
                                        'label': i18n('Diamond'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.DYNAMIC_SYMMETRY_GS: {
                                        'label': i18n('Dynamic Symmetry\n(Golden section)'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.DYNAMIC_SYMMETRY: {
                                        'label': i18n('Dynamic Symmetry\n(Rule of third)'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.RECIPROCAL_LINES_GS: {
                                        'label': i18n('Reciprocal lines\n(Golden section)'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    },
            CHHelpers.RECIPROCAL_LINES: {
                                        'label': i18n('Reciprocal lines\n(Rule of third)'),
                                        'options': {
                                                'available': [CHHelpers.OPTION_FORCE_GR, CHHelpers.OPTION_USE_SELECTION],
                                                'default':   [],
                                                'forced':    []
                                            }
                                    }
        }


