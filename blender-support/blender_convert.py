# No: !/usr/bin/env python3

# Script to convert thanks to Blender a 3D file format as glTF 2.0 Binary
# (*.glb), i.e. in a single file, with all data packed in binary form.

# Following input file formats are supported:
#  - glTF 2.0 (extensions: '*.gltf')
#  - Collada/DAE (extension: '*.dae')
#  - FBX (extension: '*.fbx')
#  - IFC (extension: '*.ifc')


# This script is not meant to be directly executed / interpreted; it is expected
# to be run as:
#
# $(BLENDER) --python blender_gltf_convert.py -- "$(MY_CONTENT_FILE)", possibly
# (preferably) through Ceylan's Hull blender-convert.sh script.
#
# Refer to http://hull.esperide.org/#blender for further information.
#
# So no need to hack around with PYTHONPATH, pip, etc. to secure bpy, _bpy, etc.

# IFC prerequisite: the BIM add-on must have already been installed in Blender,
# see https://blenderbim.org/.

import bpy

import sys
import os.path


# Needing to find our blender_snake helper module:
# (at least usually returning '', meaning the current directory)
#
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

#print(sys.path)


import blender_snake
from blender_snake import ContentFormat

import logging
import blenderbim.bim.import_ifc

content_file = sys.argv[-1]




# Main program:


# To stop on error, using 'sys.exit(Str)' as 'raise Exception(...' would not
# be sufficient.


if os.path.isfile(content_file):

    blender_snake.setup_blender_blank_state()

    detected_format = blender_snake.get_format(content_file)

    if detected_format == ContentFormat.UNKNOWN:
        sys.exit("    Error, the format of the specified content file '" + content_file + "' is not supported.")

    print("### Requesting Blender to import the content in file '" + content_file + "', detected as being in the %s format..." % (ContentFormat.to_string(detected_format)))

    blender_snake.import_content(content_file, detected_format)

    content_basename = os.path.splitext(content_file)[0]

    target_file = content_basename + ".glb"

    print("### Exporting the content in target file '" + target_file + "' as (binary) gltTF 2.0")

    blender_snake.export_content(target_file, ContentFormat.GLTF)

    print("The file '%s' has been successfully generated from '%s', in '%s'." % (os.path.basename(target_file), os.path.basename(content_file), os.path.dirname(content_file)))

else:
    sys.exit("Error, specified content file '" + content_file + "' to convert could not be found.")
