import bpy
import os

def convert_fbx_to_maya_coord(fbx_path, output_fbx_path):
    print(f"Processing file: {fbx_path} to {output_fbx_path}")
        
    # Import the FBX file
    bpy.ops.import_scene.fbx(
        filepath=fbx_path,
        use_anim=True,
        use_subsurf=False,
        use_custom_props=True,
        use_custom_normals=True,
        use_custom_props_enum_as_string=True,
        axis_forward='-Z',
        axis_up='Y')
    print(f"Imported FBX file: {fbx_path}")
    
    # Apply the transformation to convert Blender coordinates to Maya coordinates
    for obj in bpy.context.selected_objects:
        obj.rotation_euler[0] += 3.14159 / 2  # Rotate 90 degrees around X-axis
        print(f"Transformed object: {obj.name}, New rotation: {obj.rotation_euler}")
        
    # Construct the output file path
    print(f"Output file path: {output_fbx_path}")
    
    # Export the FBX file
    bpy.ops.export_scene.fbx(
        filepath=output_fbx_path,
        axis_forward='-Z',
        axis_up='Y',
        object_types={'ARMATURE'},
        use_mesh_modifiers=False,
        add_leaf_bones=False,
        bake_anim_use_all_bones=False,
        bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=False,
        bake_anim_force_startend_keying=False)
    print(f"Exported FBX file to: {output_fbx_path}")
    
    self.cleanup()

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

class BatchSimpleExportOperator(bpy.types.Operator):
    """Batch Convert FBX Animations to Maya Coordinates"""
    bl_idname = "import_export.batch_export_fbx"
    bl_label = "Batch Export FBX"
    
    fbx_output_dir: bpy.props.StringProperty(
        name="Export Directory",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        output_dir = context.scene.fbx_output_dir

        if not output_dir:
            self.report({'ERROR'}, "Output directories cannot be empty.")
            return {'CANCELLED'}

        print({'INFO'}, f"Output Directory: {output_dir}")
        
        view_layer = bpy.context.view_layer
        
        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in selection:
            obj.select_set(True)
            
            name = bpy.path.clean_name(obj.name)
            name += ".fbx"
            fn = os.path.join(output_dir, name)
        
            # Export the FBX file
            bpy.ops.export_scene.fbx(
                filepath=fn,
                use_selection=True,
                axis_forward='-Z',
                axis_up='Y',
                object_types={'MESH'},
                mesh_smooth_type='OFF',
                use_tspace=True,
                use_mesh_modifiers=False,
                add_leaf_bones=False,
                bake_anim_use_all_bones=False,
                bake_anim_use_nla_strips=False,
                bake_anim_use_all_actions=False,
                bake_anim_force_startend_keying=False)
            
            obj.select_set(False)
            
            print(f"Exported FBX file to: {fn}")
        
        # Reset status
        view_layer.objects.active = obj_active
        for obj in selection:
            obj.select_set(True)
        
        return {'FINISHED'}

class ConvertFBXOperator(bpy.types.Operator):
    """Convert FBX Animations to Maya Coordinates"""
    bl_idname = "import_export.convert_fbx"
    bl_label = "Convert FBX"
    
    cvt_fbx_input_path: bpy.props.StringProperty(
        name="Input File",
        subtype='FILE_PATH'
    )
    cvt_fbx_output_path: bpy.props.StringProperty(
        name="Output File",
        subtype='FILE_PATH'
    )

    def execute(self, context):        
        input_path = context.scene.cvt_fbx_input_path
        output_path = context.scene.cvt_fbx_output_path

        if not input_path or not output_path:
            self.report({'ERROR'}, "Input and Output pathes must be set.")
            return {'CANCELLED'}

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

class BatchConvertFBXPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Convert FBX to Maya Coord"
    # bl_idname = "FBXAxisConverter"
    bl_idname = __package__
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "cvt_fbx_input_path")
        layout.prop(scene, "cvt_fbx_output_path")
        layout.operator("import_export.convert_fbx")
        
        layout.separator

        layout.prop(scene, "cvt_fbx_input_dir")
        layout.prop(scene, "cvt_fbx_output_dir")
        layout.operator("import_export.batch_convert_fbx")
        
        layout.separator
        
        layout.prop(scene, "fbx_output_dir")
        layout.operator("import_export.batch_export_fbx")

def register():
    bpy.types.Scene.cvt_fbx_input_path = bpy.props.StringProperty(
        name="Input File",
        subtype='FILE_PATH',
        default=""
    )
    bpy.types.Scene.cvt_fbx_output_path = bpy.props.StringProperty(
        name="Output File",
        subtype='FILE_PATH',
        default=""
    )
    bpy.types.Scene.cvt_fbx_input_dir = bpy.props.StringProperty(
        name="Input Directory",
        subtype='DIR_PATH',
        default=""
    )
    bpy.types.Scene.cvt_fbx_output_dir = bpy.props.StringProperty(
        name="Output Directory",
        subtype='DIR_PATH',
        default=""
    )
    bpy.types.Scene.fbx_output_dir = bpy.props.StringProperty(
        name="Export Directory",
        subtype='DIR_PATH',
        default=""
    )
    bpy.utils.register_class(ConvertFBXOperator)
    bpy.utils.register_class(BatchConvertFBXOperator)
    bpy.utils.register_class(BatchSimpleExportOperator)
    bpy.utils.register_class(BatchConvertFBXPanel)

def unregister():
    bpy.utils.unregister_class(ConvertFBXOperator)
    bpy.utils.unregister_class(BatchConvertFBXOperator)
    bpy.utils.unregister_class(BatchSimpleExportOperator)
    bpy.utils.unregister_class(BatchConvertFBXPanel)
    
    del bpy.types.Scene.cvt_fbx_input_path
    del bpy.types.Scene.cvt_fbx_output_path
    del bpy.types.Scene.cvt_fbx_input_dir
    del bpy.types.Scene.cvt_fbx_output_dir
    del bpy.types.Scene.fbx_output_dir

if __name__ == "__main__":
    register()