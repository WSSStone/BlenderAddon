import bpy
import os, csv

from Core.find_linked import find_linked_objects

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
            # Write the header
            writer.writerow(['Name', 'Location.X', 'Location.Y', 'Location.Z',
            'Quaternion.W', 'Quaternion.X', 'Quaternion.Y', 'Quaternion.Z',
            'Scale.X', 'Scale.Y', 'Scale.Z', 'Mesh'])

            # Write data for each linked object
            for obj in linked_objects:
                # Check if custom property "Mesh" exists
                mesh_property = obj.get("Mesh", "N/A")
                writer.writerow([
                    obj.name,
                    obj.location[0],
                    obj.location[1],
                    obj.location[2],
                    obj.rotation_quaternion[0],
                    obj.rotation_quaternion[1],
                    obj.rotation_quaternion[2],
                    obj.rotation_quaternion[3],
                    obj.scale[0],
                    obj.scale[1],
                    obj.scale[2],
                    mesh_property
                ])

        file.close()

        self.report({'INFO'}, f"Exported {len(linked_objects)} objects to CSV: {self.filepath}")

        return {'FINISHED'}

    def invoke(self, context, event):
        # Show a file selector when the operator is invoked
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}