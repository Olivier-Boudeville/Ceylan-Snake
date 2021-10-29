#!/usr/bin/env python3

# This script is not meant to be directly executed / interpreted; it is expected
# to be run as:
#
# $(BLENDER) --python blender_import_gltf.py -- "$(MY_GLTF_FILE)", possibly
# through Ceylan's Hull blender-import.sh script.
#
# So no need to hack around with PYTHONPATH, pip, etc. to secure bpy, _bpy, etc.


import bpy
import sys
import os.path

scene_file = sys.argv[-1]

if os.path.isfile(scene_file):

    # Not wanting the default collection (with a default cube, light and
    # camera):
    #
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # No splash screen wanted either:
    if bpy.context.preferences.view.show_splash:
        bpy.context.preferences.view.show_splash = False

    print("### Requesting Blender to import the glTf 2.0 scene in file '" + scene_file + "'...")

    # Does not allow to import from a given directory (so a better option is to
    # define a bookmark in Blenders' 'File View':
    #
    #base_dir = os.path.dirname(ifc_file)
    #os.chdir(base_dir)

    # Doc can be found here:
    # https://docs.blender.org/api/current/bpy.ops.import_scene.html:
    #
    bpy.ops.import_scene.gltf( filepath=scene_file )

else:

    # 'raise Exception(...' would not be sufficient:
    sys.exit("Error, specified glTf file '" + scene_file + "' could not be found.")
