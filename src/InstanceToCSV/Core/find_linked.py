import bpy

def find_linked_objects(selected_obj, objs) -> list:
    linked_objects = []
    
    for obj in objs:
        if obj != selected_obj and obj.data == selected_obj.data:
            linked_objects.append(obj.name)

    return linked_objects