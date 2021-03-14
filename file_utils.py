#!/usr/bin/env python

__title__       = 'This module helps managing files and directories.'
__version__     = '0.1'
__author__      = 'Olivier Boudeville (olivier.boudeville@online.fr)'
__project__     = 'Ceylan'
__creationDate__= '2004, February 1'
__comments__    = ""
__source__      = 'Mark Pilgrim, http://diveintopython.org/, and al.'
__doc__         = __title__ + '\n' + __comments__


# Import standard python modules:
import sys, types, string, os, os.path, configparser, hashlib, re

# Import self-made modules:
from general_utils import *


class FileUtilsException(GeneralUtilsException):
    """Base class for file_utils exceptions."""


def update_config_from_file(cfg_dic, cfg_file):
    """
    Updates configuration dictionary 'cfg_dic' with informations found in file
    'cfg_file'.

    Warning: uppercase letters should not be used in configuration files, since
    ConfigParser downcases them.
    """

    try:
        my_parser = configparser.ConfigParser()
        my_parser.read(cfg_file)
        opts_list = my_parser.options('Options')
        #print("Option list is %s." % (opts_list,))
    except:
        print("Cannot open or read configuration file '%s'. Using default settings." % (cfg_file,), file=sys.stderr)
        return cfg_dic

    for opt in opts_list:
        if opt in cfg_dic:
            #print("Setting option %s" % (opt,))
            cfg_dic[opt] = my_parser.get('Options', opt)
        else:
            print("Warning: ignoring option '%s', found in configuration file but not registered." % (opt,))


def to_filename(some_string):
    """
    Transforms specified string into a legit filename.
    """

    # Inspired from
    # https://github.com/django/django/blob/main/django/utils/text.py:

    s = str(some_string).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def find_next_new_dir_name(dest_prefix):
    """
    Returns a unique name: finds next possible new directory name by adding
    increasing numbers to the end of the names of pre-existing ones.
    Example: OSDL-data -> OSDL-data-1, OSDL-data-17 -> OSDL-data-18
    """
    dir_count = 0
    dest_dir = dest_prefix
    while os.path.exists(dest_dir):
        dir_count += 1
        dest_dir = '%s%s%s' % (dest_prefix, '-' , str(dir_count))
    return dest_dir


def check_directory(dir_name):
        """Checks if corresponding directory exists.
        If not, raises FileUtilsException."""

        if not os.path.exists(dir_name):
            raise FileUtilsException("Cannot find directory '%s'." % (dir_name,))
        if not os.path.isdir(dir_name):
            raise FileUtilsException("'%s' is not a directory." % (dir_name,))
        return dir_name


def check_file(filename):
    """Checks if corresponding file exists.
    If not, raises FileUtilsException."""
    if not os.path.exists(filename):
        raise FileUtilsException("Cannot find file '%s'." % (filename,))
        if not os.path.isfile(filename):
            raise FileUtilsException("'%s' is not a file." % (filename,))
        return filename


def convert_into_filename(name):
        """Converts specified name into a valid filename for most
        filesystems."""
        return name.replace('.', '-').replace(' ', '-')


def do_all_files_exist(filenames):
    """Returns true if and only if all files in the list exist."""
    for f in filenames:
        if not os.path.isfile(f):
            #print("File %s does not exist." % (f,))
            return False
    return True


def is_content(filename):
    """Returns true if and only if filename corresponds to a content file."""
    return os.path.isfile(filename) and (is_graphics(filename) or is_sound(filename))


def is_graphics(filename):
    """Returns true if and only if filename is a graphic-related file."""
    graphics_exts = ['.jpg', '.jpeg', '.tiff', '.png', '.gif', '.bmp']
    return os.path.splitext(filename)[1].lower() in graphics_exts


def is_sound(filename):
    """Returns true if and only if filename corresponds to a sound-related
    file."""
    sound_exts = ['.wav', '.mp3', '.ogg', '.raw']
    return os.path.splitext(filename)[1].lower() in sound_exts


def get_parent_dir(dir_name):
    """Returns the name of the parent directory of dir_name."""
    return os.path.dirname(dir_name)


def get_children_dirs(dir_name):
    """
    Returns a list made of the (relative) names of the children directories
    of dir_name.
    """
    return [elem for elem in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, elem))]


def get_files_in_dir(dir_name):
    """Returns a list made of the (relative) names of the files in directory dir_name."""
    #return [ elem for elem in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, elem)) ]
    files = []
    for elem in os.listdir(dir_name):
        if os.path.isfile(os.path.join(dir_name, elem)):
            files.append(elem)
    return files


def get_dir_elements(dir_name):
    """
    Returns a pair, the list of subdirectories of dir_name and the list of
    the files in dir_name, all of them relatively to that directory
    (not absolute paths).
    """
    directories = []
    files = []
    for elem in os.listdir(dir_name):
        if os.path.isdir(os.path.join(dir_name, elem)):
            directories.append(elem)
        elif os.path.isfile(os.path.join(dir_name, elem)):
            files.append(elem)
        else:
            raise FileUtilsException("In directory '%s', '%s' was found being neither directory or file." % (dir_name,elem))
    return directories, files


def add_prefix_to_filenames(prefix, files):
    """All files or directories in files will be prefixed with prefix."""
    return [os.path.join(prefix, f) for f in files]


def scan_dir_for_content(dir_name):
    """Scans specified directory and returns a triplet with graphics files,
    sound files and other files that were spotted."""

    if not os.path.isdir(dir_name):
        raise ValueError("Unable to scan directory '%s', as it does not exist." % (dir_name,))

    graphics = []
    sounds   = []
    unknowns = []
    for f in get_files_in_dir(dir_name):
        if is_graphics(f):
            graphics.append(f)
        elif is_sound(f):
            sounds.append(f)
        else:
            unknowns.append(f)

    return graphics, sounds, unknowns


def get_all_file_paths_from(dir_name):
    """Returns a list of all files relative paths found from specified
    directory."""

    if not os.path.isdir(dir_name):
        raise ValueError("Unable to scan directory '%s', as it does not exist." % (dir_name,))

    subdirs = get_children_dirs(dir_name)
    local_files = [os.path.join(dir_name,d) for d in get_files_in_dir(dir_name)]

    for d in subdirs:
        local_files += get_all_file_paths_from(os.path.join(dir_name,d))

    return local_files


def get_all_relative_file_paths_from(dir_name):
    return get_all_relative_file_paths_helper(".", dir_name)


def get_all_relative_file_paths_helper(dir_suffix_name, base_root):
    """Returns a list of all files relative paths found from specified
    directory."""

    complete_dir = os.path.join(base_root, dir_suffix_name)

    if not os.path.isdir(complete_dir):
        raise ValueError("Unable to scan directory '%s', as it does not exist." % (complete_dir,))

    subdirs = get_children_dirs(complete_dir)
    local_files = [os.path.join(dir_suffix_name, f) for f in get_files_in_dir(complete_dir)]

    for d in subdirs:
        local_files += get_all_relative_file_paths_helper(os.path.join(dir_suffix_name, d), base_root)

    return local_files


def get_md5_for(file_path):
    """"Returns the MD5 code corresponding to the file at specified path."""
    check_file(file_path)
    with open(file_path, 'rb') as scanned_f:
        return hashlib.md5(scanned_f.read()).hexdigest()


def backup(file_to_backup):
    """
    Backups a file. A non-existing file will be ignored. Backup file will
    have the suffix '.bak'.
    """

    back_ext = '.bak'
    backup_file = file_to_backup + back_ext

    if os.path.exists(backup_file):
        try:
            os.remove(backup_file)
        except OSError:
            print("Cannot remove '%s'." % (backup_file,), file=sys.stderr)
        return sys.exc_info()

    if os.path.exists(file_to_backup):
        try:
            os.rename(file_to_backup, backup_file)
        except OSError:
            print("Cannot rename '%s'." % (file_to_backup,), file=sys.stderr)
        return sys.exc_info()



if __name__ == "__main__":
    print(__doc__)
