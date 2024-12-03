import bpy

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