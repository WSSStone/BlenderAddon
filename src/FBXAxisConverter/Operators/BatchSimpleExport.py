import bpy
import os

from Core.core import convert_fbx_to_maya_coord

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