from config import LANGUAGE

if LANGUAGE == 'en':
    from .en import *

elif LANGUAGE == 'fr':
    from .fr import *
