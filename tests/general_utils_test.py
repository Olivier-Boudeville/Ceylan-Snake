#!/usr/bin/env python

__title__       = 'This is the test of the general module.'
__version__     = '0.1'
__author__      = 'Olivier Boudeville (olivier.boudeville@online.fr)'
__project__     = 'Ceylan'
__creationDate__= '2004, January 31'
__comments__    = 'Testing module.'
__source__      = 'OSDL (http://osdl.sourceforge.net)'
__doc__         = __title__ + '\n' + __comments__

__testTarget__  = 'general_utils'


from general_utils import *


print('Beginning test of module %s.\n\n' % ( __testTarget__, ))


print('Testing ScreenDisplay...')

my_screen_display = ScreenDisplay()

my_screen_display.blank_line()
print('  + testing channels')

my_screen_display('Hello, screen world!')
my_screen_display('Let the sun shine!')
my_screen_display.error('I made a mistake.')
my_screen_display.debug('I shall debug.')
my_screen_display.warning('I shall warn my users.')

my_screen_display.blank_line()
print('  + testing indentation')

my_screen_display.indent()
my_screen_display('Let the sun shine! (bis)')
my_screen_display('Let the sun shine! (ter)')
my_screen_display.indent()
my_screen_display('Let the sun shine! (quattro?)')
my_screen_display.desindent()
my_screen_display.desindent()
my_screen_display.desindent()
my_screen_display('Let the sun shine! (cinco?)')
my_screen_display.error('I made a mistake.')

my_screen_display.blank_line()
print('  + testing string formatting')

my_screen_display.blank_line()
print('      * testing string truncating')

my_trunc_screen_display = ScreenDisplay(truncate=16)
my_trunc_screen_display('I am afraid I will be in some way truncated, my friend.')

my_screen_display.blank_line()
print('      * testing string spacing')

my_spaced_screen_display = ScreenDisplay(spacing=15, truncate=40)
my_spaced_screen_display('I', add_return=False)
my_spaced_screen_display('am', add_return=False)
my_spaced_screen_display('big', add_return=True)

my_screen_display.blank_line()
print('      * testing string compressing')

my_comp_screen_display = ScreenDisplay(compression=True)
my_comp_screen_display( "I \nsuspect \nI \nwon't \nbe \nmultilined \nfor \nlong."  )

my_screen_display.blank_line()
print('...done\n')

my_screen_display.blank_line()
print('  + testing verbosity management')

my_screen_display('I am a normal message and should be displayed.')
my_screen_display( Display.prefix_for_key_messages + 'I am an important message and should be displayed.')

my_screen_display.setVerbosity(1)
my_screen_display('I am a normal message and should not be displayed.')
my_screen_display( Display.prefix_for_key_messages + 'I am an important message and should be displayed.')

my_screen_display.setVerbosity(0)
my_screen_display('I am a normal message and should not be displayed.')
my_screen_display( Display.prefix_for_key_messages + 'I am an important message but should not be displayed.')
my_screen_display.blank_line()

print('Testing FileDisplay...')

my_file_display = FileDisplay()

my_file_display('Hello, file world!')
my_file_display('This is a silly message indeed.')
my_file_display.error('I made a mistake.')
my_file_display.debug('I shall debug.')
my_file_display.warning('I shall warn my users.')
my_file_display.remove()

print('...done\n')



print('End of test for module %s.\n' % ( __testTarget__, ))
