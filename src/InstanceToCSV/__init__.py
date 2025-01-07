import bpy
import os

def find_linked_objects(selected_obj, objs) -> list:
    linked_objects = []
    
    for obj in objs:
        if obj != selected_obj and obj.data == selected_obj.data:
            linked_objects.append(obj.name)

    return linked_objects

class SetCustomPropertyOperator(bpy.types.Operator):
    bl_label = "Propagate All Custom Properties to Linked Objects"
    bl_idname = "object.set_custom_property"

    def execute(self, context):
        selected_obj = context.object
        
        # Find objects that share the same data block
        linked_objects = find_linked_objects(selected_obj, bpy.data.objects)
        
        # Display the linked objects in the console or as a popup
        self.report({'INFO'}, f"Linked objects: {linked_objects}")

        for obj in linked_objects:
            for k, v in selected_obj.items():
                bpy.data.objects[obj][k] = v

        return {'FINISHED'}

class FindLinkedObjectsOperator(bpy.types.Operator):
    bl_label = "Find Linked Objects"
    bl_idname = "object.find_linked_objects"

    def execute(self, context):
        selected_obj = context.object
        
        # Find objects that share the same data block
        linked_objects = find_linked_objects(selected_obj, bpy.data.objects)
        
        # Display the linked objects in the console or as a popup
        self.report({'INFO'}, f"Linked objects: {linked_objects}")

        bpy.ops.object.select_all(action='DESELECT')
        for obj in linked_objects:
            bpy.data.objects[obj].select_set(True)

        return {'FINISHED'}

class ExportLinkedInstanceDataOperator(bpy.types.Operator):
    bl_label = "Export Linked Instance Data"
    bl_idname = "object.export_linked_instance_data"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        selected_obj = context.object
        
        # Find objects that share the same data block
        linked_objects = find_linked_objects(selected_obj, bpy.data.objects)
        
        # Write to CSV file
        with open(self.filepath, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write headers
            writer.writerow(['Name', 'Location.X', 'Location.Y', 'Location.Z',
                'Quaternion.X', 'Quaternion.Y', 'Quaternion.Z', 'Quaternion.W',
                'Scale.X', 'Scale.Y', 'Scale.Z', 'Mesh'])

            # Write data for each linked object
            for name in linked_objects:
                obj = bpy.data.objects[name]
                self.report({'INFO'}, f"{obj} {name}")

                # Check if custom property "Mesh" exists
                mesh_property = obj.get("Mesh", "N/A")

                '''
                A Reminder:
                    if use in Unreal:
                        UnrealWorldLocation = BlenderLocation * 100 * (1.0, -1.0, 1.0)
                        UnrealQuat = BlenderQuat * (-1.0, 1.0, -1.0, 1.0)
                '''
                writer.writerow([
                    obj.name,
                    obj.location[0], 
                    obj.location[1],
                    obj.location[2],
                    obj.rotation_quaternion[1], # X
                    obj.rotation_quaternion[2], # Y
                    obj.rotation_quaternion[3], # Z
                    obj.rotation_quaternion[0], # W
                    obj.scale[0], 
                    obj.scale[1],
                    obj.scale[2],
                    mesh_property])

        file.close()

        self.report({'INFO'}, f"Exported {len(linked_objects)} objects to CSV: {self.filepath}")

        return {'FINISHED'}

    def invoke(self, context, event):
        # Show a file selector when the operator is invoked
        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}

class ReferenceRelationsPanel(bpy.types.Panel):
    """Export Object's Linked Instance Data to CSV"""
    bl_label = "Export Linked Instance Data"
    # bl_idname = "OBJECT_PT_export_linked_instance_data"
    bl_idname = __package__
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        layout.label(text="Target Object:")
        layout.prop(obj, "name")
        layout.operator("object.find_linked_objects", text="Find Linked Objects")
        
        layout.separator
        
        layout.label(text="Custom Properties:")
        layout.operator("object.set_custom_property", text="Propagate All Custom Properties to Linked Objects")

        layout.separator
        layout.label(text="Export Linked Instance Data:")
        layout.operator("object.export_linked_instance_data", text="Export Linked Instance Data")

def register():
    bpy.types.Scene.csv_path = bpy.props.StringProperty(
        name="Output File",
        subtype='FILE_PATH',
        default=""
    )
    
    bpy.utils.register_class(FindLinkedObjectsOperator)
    bpy.utils.register_class(ExportLinkedInstanceDataOperator)
    bpy.utils.register_class(SetCustomPropertyOperator)
    bpy.utils.register_class(ReferenceRelationsPanel)

def unregister():
    bpy.utils.unregister_class(FindLinkedObjectsOperator)
    bpy.utils.unregister_class(ExportLinkedInstanceDataOperator)
    bpy.utils.unregister_class(SetCustomPropertyOperator)
    bpy.utils.unregister_class(ReferenceRelationsPanel)
    
    del bpy.types.Scene.csv_path

if __name__ == "__main__":
    register()