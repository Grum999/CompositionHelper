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

from .compositionhelper import CompositionHelper

# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = CompositionHelper(parent=app)
app.addExtension(extension)
