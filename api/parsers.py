from django.utils.translation import ugettext as _
from django.utils import translation

class ParserDefault():
    def parse(self, message):
        translation.activate("en")
        if "hi" in message.lower():
            return _("Hi bro!")
        return None
