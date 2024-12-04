bl_info = {
    "name": "Export Object's Linked Instance Data to CSV",
    "blender": (4, 1, 0),
    "category": "Intancing",
}

import bpy
import os

from Operators.FindLinkedObjects import FindLinkedObjectsOperator
from Operators.ExportLinkedInstanceData import ExportLinkedInstanceDataOperator
from Operators.SetCustomProperty import SetCustomPropertyOperator

class ReferenceRelationsPanel(bpy.types.Panel):
    """Export Object's Linked Instance Data to CSV"""
    bl_label = "Export Linked Instance Data"
    bl_idname = "OBJECT_PT_export_linked_instance_data"
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