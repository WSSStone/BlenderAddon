import bpy

from Core.find_linked import find_linked_objects

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