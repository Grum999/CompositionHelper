from .compositionhelper import CompositionHelper

# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = CompositionHelper(parent=app)
app.addExtension(extension)
