#!/usr/bin/env python

__title__       = 'This is the general module, which contains everything which is the least specific to any project: all generic and all purpose code should end up here.'
__version__     = '0.1'
__author__      = 'Olivier Boudeville (olivier.boudeville@online.fr)'
__project__     = 'Ceylan'
__creationDate__= '2004, January 31'
__comments__    = "Curiously enough, making an inherited method private does not override base class' one: Display.display could not be Display.__display if subclasses were to be able to redefine it."
__source__      = 'Mark Pilgrim, http://diveintopython.org/, and al.'
__doc__         = __title__ + '\n' + __comments__



# Import standard python modules:
import os, sys, types, string


class GeneralUtilsException(Exception):
    """Base class for generalUtils exceptions."""


class ApplicationException(Exception):
    """Base class for applicative exceptions."""


def activate_name_completion():
    """Activates python interpreter's command line automatic name
       completion."""
    import rlcompleter
    import readline
    readline.parse_and_bind("tab: complete")
    print("Python's name completion activated.")


def display_dic(dic):
    """Displays the key-value pairs of specified dictionnary."""

    # Find longest key:
    max_len = 0
    for k in dic.keys():
        l = len(k)
        if l > max_len:
            max_len = l
    # First field shoud have the width of the longest key item:
    for (k,v) in dic.items():
        print('  %*s: %s' % (max_len, k, v))


def display_list(list):
    """Displays list elements, one per line."""
    for i in list:
        print(i)


class Display:
    """This class provides abstract display services.
    It is intended to be subclassed."""

    prefix_for_key_messages = "--"
    offset_increment = 4

    normal_prefix  = ''
    info_prefix    = 'Info: '
    debug_prefix   = '--> Debug: '
    warning_prefix = 'Warning: '
    error_prefix   = '#### Error: '

    do_debug = True

    def __init__(self, spacing=10, compression=True, truncate=False, verbosity=2):
        """
        Defines the options for this display to perform its tasks.
            - spacing: minimum size for a field
            - compression: if true, a multi-lined field is displayed only on one line
            - truncate: if set, truncates a field to the maximum length this values provides
            - verbosity: sets the level of detail of the display,
                - 0: totally silent,
                - 1: only the most important messages are displayed, those that start with prefix_for_key_messages
                - 2: all messages are displayed
            """

        self.esp = spacing and (lambda s, space_num=spacing: str.ljust(s, space_num)) or (lambda s: s)
        self.comp = compression and (lambda s: " ".join(s.split())) or (lambda s: s)
        self.trunc = truncate and (lambda s, trunc_num=truncate: s[:trunc_num]) or (lambda s: s)
        self.verb = verbosity
        self.offset = 0


    def display(self, message, add_return=True):
        """Displays unconditionnally specified normal message."""
        if add_return:
            self.inner_display_normal(self.normal_prefix + self.offset * ' ' + message + '\n')
        else:
            self.inner_display_normal(self.normal_prefix + self.offset * ' ' + message)


    def info(self, message, add_return=True):
        """Displays specified information message."""
        if add_return:
            self.inner_display_normal(self.info_prefix + message + '\n')
        else:
            self.inner_display_normal(self.info_prefix + message)


    def debug(self, message, add_return=True):
        """Displays specified debug message if and only if we are in debug mode."""
        if self.do_debug:
            if add_return:
                self.inner_display_normal(self.debug_prefix + message + '\n')
            else:
                self.inner_display_normal(self.debug_prefix + message)


    def warning(self, message, add_return=True):
        """Displays specified warning message."""
        if add_return:
            self.inner_display_error(self.warning_prefix + message + '\n')
        else:
            self.inner_display_error(self.warning_prefix + message)


    def error(self, message, add_return=True):
        """Displays specified error message."""
        if add_return:
            self.inner_display_error(self.error_prefix + message + '\n')
        else:
            self.inner_display_error(self.error_prefix + message)


    def inner_display_normal(self, message):
        """
        Pure virtual function, to be redefined by implementation classes.
        It should have been private, if it could be overridden.
        """
        pass


    def indent(self):
        """Indents one more level for normal messages."""
        self.offset += self.offset_increment


    def desindent(self):
        """Indents one fewer level for normal messages."""
        self.offset -= self.offset_increment
        if self.offset < 0:
            self.offset = 0


    def blank_line(self):
        if self.verb == 2:
            self.inner_display_normal('\n')


    def status(self):
        self.inner_display_normal('Verbosity level is %s.' % (self.verb,))


    def __call__(self, message, add_return=True):
        if type(message) == str:
            if self.verb == 2 or ((self.verb == 1) and (message[:2] == self.prefix_for_key_messages)):
                self.display(self.esp(self.trunc(self.comp(message))), add_return)
        elif type(message) in [list,tuple]:
            for item in message:
                self.__call__(item, add_return)
        else:
            print('Display: unsupported message type, unable to display it.')


    def setVerbosity(self, new_verbosity=2):
        self.verb = new_verbosity



class ScreenDisplay(Display):
    """
    This is the Display implementation that uses screen as display output
    device.
    """

    def __init__(self, spacing=10, compression=True, truncate=False, verbosity=2):
        # Propagates back settings to ancestor class' constructor.
        Display.__init__(self, spacing, compression, truncate, verbosity)


    def inner_display_normal(self, message):
        """Displays a message to standard output file descriptor."""
        sys.stdout.write(message)
        sys.stdout.flush()


    def inner_display_error(self, message):
        """Displays a message to error output file descriptor."""
        sys.stderr.write(message)
        sys.stderr.flush()



class FileDisplay(Display):
    """This is the Display implementation that uses files as display
    output device."""

    default_log_base_name = "Log"
    default_extension = "txt"

    def __init__(self, log_base_name=default_log_base_name, allow_overwrite=True, spacing=10, compression=True, truncate=False, verbosity=2):
        """
        Implements the Display interface so that messages are output to a log file:
            - log_filename: defines the file where messages should be stored
            - allow_overwrite: tells whether a previously existing log file could be overwritten
            - the other parameters have the same semantics as the Display ones
        """

        Display.__init__(self, spacing=10, compression=True, truncate=False, verbosity=2)
        self.log_base_name = log_base_name
        self.allow_overwrite = allow_overwrite
        self.log_filename = self.log_base_name + "." + self.default_extension
        if self.allow_overwrite:
            self.log_file = open(self.log_filename, 'w')
        else:
            self.log_file = open(self.log_filename, 'a')
        self.status()


    def __del__(self):
        """Destructor shall release the resources."""
        if self.log_file:
            self.log_file.close()


    def inner_display_normal(self, message):
        self.log_file.write(message + '\n')
        self.log_file.flush()

    def inner_display_error(self, message):
        self.log_file.write(message + '\n')
        self.log_file.flush()

    def remove(self):
        """Removes any log file written (useful for tests)."""
        if self.log_file:
            self.log_file.close()

        if os.path.exists(self.log_filename):
            os.remove(self.log_filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
    else:
        temp = ScreenDisplay()
        temp(sys.argv[1])
