#!/usr/bin/env python3

# Script to import IFC files in Blender.

# This script is not meant to be directly executed / interpreted; it is expected
# to be run as:

# $(BLENDER) --python blender_import_ifc.py -- "$(MY_IFC_FILE)", possibly
# through Ceylan's Hull blender-import.sh script.
#
# So no need to hack around with PYTHONPATH, pip, etc. to secure bpy, _bpy, etc.

# Prerequisite: the BIM add-on must have already been installed in Blender, see
# https://blenderbim.org/.


import bpy
import logging
import blenderbim.bim.import_ifc


import sys
import os.path

ifc_file = os.path.abspath(sys.argv[-1])

if os.path.isfile(ifc_file):

    # Not wanting the default collection (with a default cube, light and
    # camera), yet 'bpy.ops.wm.read_factory_settings(use_empty=True)' induces
    # too much side-effects; so doing it manually then:
    #
    #objs = bpy.data.objects
    #[objs.remove(objs[obj], do_unlink=True) for obj in ["Cube", "Light", "Camera"]

    default_collection = bpy.data.collections.get('Collection')

    for obj in default_collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(default_collection)

    # Not relevant here either:
    # No splash screen wanted either:
    #if bpy.context.preferences.view.show_splash:
    #    bpy.context.preferences.view.show_splash = False

    print("### Requesting Blender to import the IFC content in file '" + ifc_file + "'...")

    # Does not allow to import from a given directory (so a better option is to
    # define a bookmark in Blenders' 'File View':
    #
    #base_dir = os.path.dirname(ifc_file)
    #os.chdir(base_dir)

    # Doc can be found here:
    # https://wiki.osarch.org/index.php?title=BlenderBIM_Add-on_code_examples#Import_an_IFC
    #
    ifc_import_settings = blenderbim.bim.import_ifc.IfcImportSettings.factory(bpy.context, ifc_file, logging.getLogger('ImportIFC'))

    ifc_importer = blenderbim.bim.import_ifc.IfcImporter(ifc_import_settings)

    ifc_importer.execute()

else:

    # 'raise Exception(...' would not be sufficient:
    sys.exit("Error, specified IFC file '" + ifc_file + "' could not be found.")
