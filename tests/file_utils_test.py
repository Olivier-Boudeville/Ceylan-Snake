#!/usr/bin/env python

__title__       = 'This is the test of the file module.'
__version__     = '0.1'
__author__      = 'Olivier Boudeville (olivier.boudeville@online.fr)'
__project__     = 'Ceylan'
__creationDate__= '2004, February 2'
__comments__    = 'Testing module.'
__source__      = 'OSDL (http://osdl.sourceforge.net)'
__doc__         = __title__ + '\n' + __comments__

__testTarget__  = 'file_utils'


from general_utils import *


print('Beginning test of module %s.\n\n' % ( __testTarget__, ))

print('Testing basic definitions...')

print('End of test for module %s.\n\n' % ( __testTarget__, ))
