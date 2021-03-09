#!/usr/bin/env python

__title__       = 'This is the toolbox module, convenient generic functions and classes for python.'
__version__     = '0.1'
__author__      = 'Olivier Boudeville (olivier.boudeville@online.fr)'
__project__     = 'Ceylan'
__creationDate__= '2001, October 12'
__comments__    = 'Set of useful general-purpose python modules.'
__source__      = 'Mark Pilgrim, http://diveintopython.org/, and al.'
__doc__         = __title__ + '\n' + __comments__


# Toolbox's code is being distributed among *_utils.py.


# Home-made ones:
from general_utils import *
from file_utils import *


class ToolboxException(GeneralUtilsException):
    """Base class for toolbox exceptions."""


if __name__ == "__main__":
    print(__doc__)
