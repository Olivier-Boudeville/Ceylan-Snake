#!/usr/bin/env python3

# Script to import DAE (Collada) files in Blender.

# This script is not meant to be directly executed / interpreted; it is expected
# to be run as:
#
# $(BLENDER) --python blender_import_dae.py -- "$(MY_DAE_FILE)", possibly
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

    print("### Requesting Blender to import the DAE content in file '" + content_file + "'...")

    # Does not allow to import from a given directory (so a better option is to
    # define a bookmark in Blenders' 'File View'):
    #
    #base_dir = os.path.dirname(ifc_file)
    #os.chdir(base_dir)

    # Doc can be found here:
    # https://docs.blender.org/api/current/bpy.ops.import_scene.html
    #
    # (currently does not work at least in some cases, whereas via the Blender
    # version 2.93.6 GUI these DAE can be loaded; message: 'RuntimeError:
    # Operator bpy.ops.object.mode_set.poll() failed, context is incorrect')
    #
    bpy.ops.wm.collada_import( filepath=content_file )

    # Select the first object found:
    obj_to_select = bpy.data.objects[0]
    obj_to_select.select_set(True)

    bpy.context.view_layer.objects.active = obj_to_select
    #bpy.ops.view3d.view_all(use_all_regions=True, center=True)
    #original_type = bpy.context.area.type
    #bpy.context.area.type = "VIEW_3D"
    #bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    #bpy.context.area.type = original_type

    # As local view needs a VIEW_3D context:
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override["area"] = area
            bpy.ops.view3d.localview(override)

    # To export blend file:
    #bpy.ops.wm.save_mainfile( filepath = yourBlendFilePath )


else:

    # 'raise Exception(...' would not be sufficient:
    sys.exit("Error, specified DAE file '" + content_file + "' could not be found.")
