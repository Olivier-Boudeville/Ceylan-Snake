#!/usr/bin/env python3

# A Ceylan-Snake module centralising common facilities for various other
# import/conversion scripts.

import bpy

import sys
import os.path

from enum import Enum, auto


class ContentFormat(Enum):
    """Useful to describe the supported content formats."""
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



def setup_blender_blank_state():
    """Sets an appropriate initial Blender initial state."""

    # Not wanting the default collection (with a default cube, light and
    # camera), yet 'bpy.ops.wm.read_factory_settings(use_empty=True)' induces
    # too much side-effects; so doing it manually then:
    #
    #objs = bpy.data.objects
    #[objs.remove(objs[obj], do_unlink=True)
    #    obj in ["Cube", "Light", "Camera"]

    default_collection = bpy.data.collections.get('Collection')

    for obj in default_collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(default_collection)

    # No splash screen wanted either:
    if bpy.context.preferences.view.show_splash:
        bpy.context.preferences.view.show_splash = False



def get_format(content_file):
    """Returns the detected file format for the specified file."""

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

    return detected_format



def import_content(content_file, content_format):
    """Imports the specified content of specified format in Blender."""

    # Does not allow to import from a given directory (so a better option is to
    # define a bookmark in Blenders' 'File View'):
    #
    #base_dir = os.path.dirname(ifc_file)
    #os.chdir(base_dir)

    # Doc can generally be found here:
    # https://docs.blender.org/api/current/bpy.ops.import_scene.html
    #

    if content_format == ContentFormat.GLTF:

        bpy.ops.import_scene.gltf( filepath=content_file )

    elif content_format == ContentFormat.COLLADA:

        bpy.ops.wm.collada_import( filepath=content_file )

    elif content_format == ContentFormat.FBX:

        bpy.ops.import_scene.fbx( filepath=content_file )

    elif content_format == ContentFormat.IFC:

        # Doc can be found here:
        # https://wiki.osarch.org/index.php?title=BlenderBIM_Add-on_code_examples#Import_an_IFC

        # Check add-on availability first:
        if not importlib.util.find_spec("blenderbim"):
            sys.exit("No Blender add-on available for BIM; refer to https://blenderbim.org/download.html")

        ifc_import_settings = blenderbim.bim.import_ifc.IfcImportSettings.factory(bpy.context, content_file, logging.getLogger('ImportIFC'))

        ifc_importer = blenderbim.bim.import_ifc.IfcImporter(ifc_import_settings)

        ifc_importer.execute()

    else:
        sys.exit("Error, the format ('" + ContentFormat.to_string(content_format) + "') for the specified content to import is not supported.")



def export_content(target_file, target_format):
    """Exports the current 3D content in the target file, using the target
format.Focuses on the objects (as a whole) of the scene."""

    # See https://docs.blender.org/api/current/bpy.ops.export_scene.html:
    if target_format == ContentFormat.GLTF:

        bpy.ops.export_scene.gltf(filepath=target_file, export_format='GLB')

    else:
        sys.exit("Error, the target format ('" + ContentFormat.to_string(target_format) + "') for the content to export is not supported.")



def focus_on_objects():
    """Focuses on the objects (as a whole) of the scene."""

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
