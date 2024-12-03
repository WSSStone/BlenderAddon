import bpy

from Core.find_linked import find_linked_objects

class FindLinkedObjectsOperator(bpy.types.Operator):
    bl_label = "Find Linked Objects"
    bl_idname = "object.find_linked_objects"

    def execute(self, context):
        selected_obj = context.object
        
        # Find objects that share the same data block
        linked_objects = find_linked_objects(selected_obj, bpy.data.objects)
        
        # Display the linked objects in the console or as a popup
        self.report({'INFO'}, f"Linked objects: {linked_objects}")

        return {'FINISHED'}