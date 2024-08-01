bl_info = {
    "name": "Convert FBX Animations to Maya Coord",
    "blender": (4, 1, 0),
    "category": "Import-Export",
}

import bpy
import os

from Operators.BatchConvertFBXOperator import ConvertFBXOperator
from Operators.BatchConvertFBXOperator import BatchConvertFBXOperator

class BatchConvertFBXPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Convert FBX to Maya Coord"
    bl_idname = "SCENE_PT_convert_fbx"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "input_path")
        layout.prop(scene, "output_path")
        layout.operator("import_export.convert_fbx")
        
        layout.prop(scene, "input_dir")
        layout.prop(scene, "output_dir")
        layout.operator("import_export.batch_convert_fbx")

def register():
    bpy.utils.register_class(ConvertFBXOperator)
    bpy.utils.register_class(BatchConvertFBXOperator)
    bpy.utils.register_class(BatchConvertFBXPanel)
    bpy.types.Scene.input_file = bpy.props.StringProperty(
        name="Input File",
        subtype='FILE_PATH',
        default=""
    )
    bpy.types.Scene.output_file = bpy.props.StringProperty(
        name="Output File",
        subtype='FILE_PATH',
        default=""
    )
    bpy.types.Scene.input_dir = bpy.props.StringProperty(
        name="Input Directory",
        subtype='DIR_PATH',
        default=""
    )
    bpy.types.Scene.output_dir = bpy.props.StringProperty(
        name="Output Directory",
        subtype='DIR_PATH',
        default=""
    )

def unregister():
    bpy.utils.unregister_class(ConvertFBXOperator)
    bpy.utils.unregister_class(BatchConvertFBXOperator)
    bpy.utils.unregister_class(BatchConvertFBXPanel)
    del bpy.types.Scene.input_file
    del bpy.types.Scene.output_file
    del bpy.types.Scene.input_dir
    del bpy.types.Scene.output_dir

if __name__ == "__main__":
    register()