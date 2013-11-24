import warnings
from .sessions import Session


def Imbox(hostname, username=None, password=None, ssl=True):
    warnings.warn('Imbox is deprecated. Please use imbox.login instead',
                  DeprecationWarning)
    return login(hostname, username=username, password=password, ssl=ssl)


def login(hostname, username=None, password=None, ssl=True):
    session = Session(hostname, ssl=ssl)
    session.login(username, password)
    return session
