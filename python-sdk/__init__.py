from .papi import PapiClient
from .solo import SoloAuthClient, SoloOpenAuthClient
#from .witsml import WitsmlClient

__version__ = '0.0.1'

__all__ = [
    'PapiClient',
    #'WitsmlClient',
    'SoloAuthClient',
    'SoloOpenAuthClient'
]
