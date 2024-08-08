import bpy
import os

from Core.core import convert_fbx_to_maya_coord

class BatchConvertFBXOperator(bpy.types.Operator):
    """Batch Convert FBX Animations to Maya Coordinates"""
    bl_idname = "import_export.batch_convert_fbx"
    bl_label = "Batch Convert FBX"
    
    cvt_fbx_input_dir: bpy.props.StringProperty(
        name="Input Directory",
        subtype='DIR_PATH'
    )
    cvt_fbx_output_dir: bpy.props.StringProperty(
        name="Output Directory",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        input_dir = context.scene.cvt_fbx_input_dir
        output_dir = context.scene.cvt_fbx_output_dir

        if not input_dir or not output_dir:
            self.report({'ERROR'}, "Input and Output directories must be set.")
            return {'CANCELLED'}

        print({'INFO'}, f"Input Directory: {input_dir}")
        print({'INFO'}, f"Output Directory: {output_dir}")
        
        self.recur_dir(input_dir, output_dir)
        return {'FINISHED'}
    
    def cleanup(self):
        # Clear the scene for the next file
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.ops.outliner.orphans_purge(do_recursive=True)  # Purge all orphan data
        print(f"Cleared the scene for the next file")

    def recur_dir(self, input_dir, output_dir):
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            print(f"Created output directory: {output_dir}")
        
        for f in os.listdir(input_dir):
            if os.path.isdir(os.path.join(input_dir, f)):        
                new_input_dir = os.path.join(input_dir, f)
                new_output_dir = os.path.join(output_dir, f)
                self.recur_dir(new_input_dir, new_output_dir)
                continue
                
            if f.lower().endswith('.fbx'):
                print(f"Found {len(f)} FBX files in {input_dir}")
                convert_fbx_to_maya_coord(os.path.join(input_dir, f), os.path.join(output_dir, f))
                continue