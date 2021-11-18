#!/usr/bin/env python3

# Script to import FBX files in Blender.

# This script is not meant to be directly executed / interpreted; it is expected
# to be run as:
#
# $(BLENDER) --python blender_import_fbx.py -- "$(MY_FBX_FILE)", possibly
# through Ceylan's Hull blender-import.sh script.
#
# So no need to hack around with PYTHONPATH, pip, etc. to secure bpy, _bpy, etc.


import bpy
import sys
import os.path

content_file = sys.argv[-1]

if os.path.isfile(content_file):

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

     # No splash screen wanted either:
    if bpy.context.preferences.view.show_splash:
        bpy.context.preferences.view.show_splash = False

    print("### Requesting Blender to import the FBX content in file '" + content_file + "'...")

    # Does not allow to import from a given directory (so a better option is to
    # define a bookmark in Blenders' 'File View'):
    #
    #base_dir = os.path.dirname(ifc_file)
    #os.chdir(base_dir)

    # Doc can be found here:
    # https://docs.blender.org/api/current/bpy.ops.import_scene.html
    #
    bpy.ops.import_scene.fbx( filepath=content_file )

    # To export blend file:
    #bpy.ops.wm.save_mainfile( filepath = yourBlendFilePath )


else:

    # 'raise Exception(...' would not be sufficient:
    sys.exit("Error, specified fbx file '" + content_file + "' could not be found.")
