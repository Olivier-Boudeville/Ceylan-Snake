#!/usr/bin/env python

__title__       = "This is the introspection module, made to retrieve easily information about Python elements."
__version__     = "0.2"
__author__      = "Olivier Boudeville (olivier.boudeville@online.fr)"
__project__     = "Ceylan"
__creationDate__= "2001, August 23"
__comments__    = "Use its own introspection capabilities to discover what this module can do!"
__source__      = "Mark Pilgrim, http://diveintopython.org/, and al."
__doc__         = __title__ + '\n' + __comments__


# Original functions translated from Python 2.1 to Python 1.5.2 and, eventually,
# back in 2.1!

import sys, string, inspect, toolbox


def show_dict(my_dict, spacing=10, collapse=1):
    """Displays a dictionnary in a user-friendly fashion, each line showing a key and its related object"""
    tmp_list = []
    for item in my_dict.keys():
        tmp_list.append("%s %s" % (item.ljust(spacing), my_dict[item]))
    print( string.join(tmp_list, '\n') )


def show_methods(object, spacing=15, collapse=1):
    """Prints methods and doc strings of object"""

    method_list = []
    for method in dir(object):
        if callable(getattr(object, method)):
            method_list.append(method)
    tmp_list = []
    for method in method_list:
        tmp_list.append("%s %s" % (method.ljust(spacing),str(getattr(object, method).__doc__)))
    print( string.join(tmp_list, '\n'))


def show_data_members(object, spacing=10, collapse=1):
    """Prints data members of object, with their type"""

    data_list = []
    for member in dir(object):
        if not callable(getattr(object, member)):
            data_list.append(member)
    tmp_list = []
    for member in data_list:
        tmp_list.append("%s %s %s" % (member.ljust(spacing), type(member), str(member)))
    if tmp_list:
        print( string.join(tmp_list, '\n'))
    else:
        print( "No data attributes")


def show_loaded_modules(spacing=10, collapse=1):
    """Prints the loaded modules"""

    tmp_list=[]
    for item in sys.modules.keys():
        tmp_list.append("%s %s" % (item.ljust(spacing), sys.modules[item]))
    print( string.join(tmp_list, '\n'))


def show_object_symbol_table(my_object):
    """Displays the local object symbol table"""
    show_dict( vars(my_object) )


def show_current_local_symbol_table(spacing=10, collapse=1):
    """Shows current local symbol table, with their type"""
    tmp_list=[]
    for item in dir():
        tmp_list.append("%s %s" % (item.ljust(spacing), type(item)))
    print( string.join(tmp_list, '\n'))


def inspect_module(my_module, spacing=10, collapse=1):
    """Displays information regarding a module"""
    print( "Module description: ", my_module.__doc__)
    if my_module.__file__ is not None:
        print( "Defined in file '%s'" % my_module.__file__)
    tmp_list = []
    print("Module members:")
    process_func = collapse and (lambda s: string.join(s.split(), ' ')) or (lambda s: s)
    print( "\n".join(["%s %s" % (item[0].ljust(spacing), process_func(str(item[1]))) for item in inspect.getmembers(my_module)]))


def inspect_class(my_class, spacing=10, collapse=1):
    """Displays information regarding a class"""
    print( "Class description: ", my_class.__doc__)
    print( "Defined in module: ", my_class.__module__)


def inspect_method(my_method, spacing=15, collapse=1):
    """Displays information regarding a method"""
    print( "Name: ", my_method.__name__ )
    print( "Method description: ", my_method.__doc__ )
    print( "Belonging to class: ", my_method.im_class )
    print( "Function-object containing this method: ", my_method.im_func )
    if my_method.im_self is not None:
        print( "Linked to instance: ", im_self )


def inspect_function(my_func, spacing=10, collapse=1):
    """Displays information regarding a function"""
    print( "Name: ", my_func.__name__ )
    print( "Function description: ", my_func.__doc__ )
    print( "Default arguments: ", my_func.func_defaults )
    print( "Global namespace of defintion: ", myfunc.func_globals )



if __name__ == "__main__":
   print( __doc__ )
