import bpy
import os
from Core.core import convert_fbx_to_maya_coord

class ConvertFBXOperator(bpy.types.Operator):
    """Batch Convert FBX Animations to Maya Coordinates"""
    bl_idname = "import_export.convert_fbx"
    bl_label = "Convert FBX"
    
    input_path: bpy.props.StringProperty(
        name="Input File",
        subtype='FILE_PATH'
    )
    output_path: bpy.props.StringProperty(
        name="Output File",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        input_path = context.scene.input_path
        output_path = context.scene.output_path

        print({'INFO'}, f"Input File: {input_path}")
        print({'INFO'}, f"Output File: {output_path}")
        
        convert_fbx_to_maya_coord(input_path, output_path)
        return {'FINISHED'}
    
    def cleanup(self):
        # Clear the scene for the next file
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_all(action='SELECT')
        # bpy.ops.object.delete()
        bpy.ops.outliner.orphans_purge(do_recursive=True)  # Purge all orphan data
        print(f"Cleared the scene for the next file")