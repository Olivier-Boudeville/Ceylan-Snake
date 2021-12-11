#!/usr/bin/env python3

# Script to import content in Blender.

# Following file formats are supported:
#  - glTF 2.0 (extensions: '*.gltf'/'*.glb')
#  - Collada/DAE (extension: '*.dae')
#  - FBX (extension: '*.fbx')
#  - IFC (extension: '*.ifc')


# This script is not meant to be directly executed / interpreted; it is expected
# to be run as:
#
# $(BLENDER) --python blender_import_dae.py -- "$(MY_DAE_FILE)", possibly
# (preferably) through Ceylan's Hull blender-import.sh script.
#
# Refer to http://hull.esperide.org for further information.
#
# So no need to hack around with PYTHONPATH, pip, etc. to secure bpy, _bpy, etc.

# IFC prerequisite: the BIM add-on must have already been installed in Blender,
# see https://blenderbim.org/.

import bpy

import sys
import os.path

from enum import Enum, auto

import importlib

import logging
import blenderbim.bim.import_ifc

content_file = sys.argv[-1]


class ContentFormat(Enum):
    """Useful to describe the supported content formats"""
    GLTF = auto()
    COLLADA = auto()
    FBX = auto()
    IFC = auto()
    UNKNOWN = auto()

    def to_string(FormatEnum):
        format_dic = { ContentFormat.GLTF: "glTF 2.0",
                       ContentFormat.COLLADA: "Collada",
                       ContentFormat.FBX: "FBX",
                       ContentFormat.IFC: "IFC",
                       ContentFormat.UNKNOWN: "unknown" }
        return format_dic[FormatEnum]





# Main program:


# To stop on error, using 'sys.exit(Str)' as 'raise Exception(...' would not
# be sufficient.


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

    extension = (os.path.splitext(content_file)[1]).lower()
    #print( "extension: %s" % (extension,))

    # Keys are file extensions, values are identifiers of file formats:
    format_dic = {'.gltf': ContentFormat.GLTF,
                  '.glb':  ContentFormat.GLTF,
                  '.dae':  ContentFormat.COLLADA,
                  '.fbx':  ContentFormat.FBX,
                  '.ifc':  ContentFormat.IFC }

    detected_format = format_dic.get(extension, ContentFormat.UNKNOWN)
    #print( "detected_format: %s" % (detected_format,))

    if detected_format == ContentFormat.UNKNOWN:
        sys.exit("    Error, the format of the specified content file '" + content_file + "' is not supported.")

    print("### Requesting Blender to import the content in file '" + content_file + "', detected as being in the %s format..." % (ContentFormat.to_string(detected_format)))

    # Does not allow to import from a given directory (so a better option is to
    # define a bookmark in Blenders' 'File View'):
    #
    #base_dir = os.path.dirname(ifc_file)
    #os.chdir(base_dir)

    # Doc can generally be found here:
    # https://docs.blender.org/api/current/bpy.ops.import_scene.html
    #

    if detected_format == ContentFormat.GLTF:

        bpy.ops.import_scene.gltf( filepath=content_file )

    if detected_format == ContentFormat.COLLADA:

        bpy.ops.wm.collada_import( filepath=content_file )

    elif detected_format == ContentFormat.FBX:

        bpy.ops.import_scene.fbx( filepath=content_file )

    elif detected_format == ContentFormat.IFC:

        # Doc can be found here:
        # https://wiki.osarch.org/index.php?title=BlenderBIM_Add-on_code_examples#Import_an_IFC

        # Check add-on availability first:
        bim_plugin_spec = importlib.util.find_spec("blenderbim")

        if not importlib.util.find_spec("blenderbim"):
            sys.exit("No Blender add-on available for BIM; refer to https://blenderbim.org/download.html")

        ifc_import_settings = blenderbim.bim.import_ifc.IfcImportSettings.factory(bpy.context, content_file, logging.getLogger('ImportIFC'))

        ifc_importer = blenderbim.bim.import_ifc.IfcImporter(ifc_import_settings)

        ifc_importer.execute()


    # Let's focus on all objects, by first selecting them all:
    #for obj in bpy.data.objects:
    #    obj.select_set(True)

    #bpy.context.view_layer.objects.active = obj_to_select
    #bpy.ops.view3d.view_all(use_all_regions=True, center=True)

    # Let's focus As local view needs a VIEW_3D context:
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override["area"] = area
            bpy.ops.view3d.localview(override)

    # To export blend file:
    #bpy.ops.wm.save_mainfile( filepath=yourBlendFilePath )

else:
    sys.exit("Error, specified content file '" + content_file + "' could not be found.")
