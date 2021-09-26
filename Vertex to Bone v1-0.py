import bpy

bl_info = {
    'name': 'Vertex to Bone',
    'author': 'Rufat Mamedov <jasszkey@gmail.com, artstation.com/tafoor>',
    'version': (1, 0),
    'blender': (2, 93, 0),
    'category': 'Animation',
    'location': '3D ViewPort SpaceBar Search -> Vertex to Bones',
    'description': ''
}

class ANIM_OT_vertex_to_bones(bpy.types.Operator):
    """Vertex to Bone"""
    bl_idname = 'view3d.verts_to_bones'
    bl_label = 'Vertex to Bone'
    bl_description = 'Converts properly named mesh (VtoB) vertices to the bones'

    # PUT OBJECT & MESH NAME HERE
    obj_name = 'VtoB'

    @classmethod    
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):   
        obj = bpy.data.objects[self.obj_name]
        mesh = bpy.data.meshes[self.obj_name]  
        bpy.ops.object.armature_add(enter_editmode=True)
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.delete()
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        arm_obj = bpy.data.objects['Armature']

        for vert in mesh.vertices:

            for i in range(len(vert.co)):
                round (vert.co[i], 3)
                if vert.co[i] == -0.0:
                    vert.co[i] = 0
            
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(vert.co[0], vert.co[1], vert.co[2]))
            empty = bpy.data.objects['Empty']
            empty.name = 'Anchor'
            bpy.ops.object.select_all(action='DESELECT')
            empty.select_set(1)
            bpy.ops.view3d.snap_cursor_to_selected()
            obj.select_set(1)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.parent_set(type='VERTEX')
            arm_obj.select_set(1)
            bpy.context.view_layer.objects.active = arm_obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.bone_primitive_add()
            bpy.ops.object.editmode_toggle()
            bpy.data.objects["Armature"].data.bones.active = bpy.data.objects['Armature'].data.bones['Bone']
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.posemode_toggle()
            bpy.ops.pose.constraint_add(type='CHILD_OF')
            bpy.context.object.pose.bones["Bone"].constraints["Child Of"].target = empty
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.ops.object.posemode_toggle()
            bpy.data.objects['Armature'].data.bones['Bone'].name = 'Joint'

        return {'FINISHED'}

    
def register():
    bpy.utils.register_class(ANIM_OT_vertex_to_bones)

def unregister():
    bpy.utils.unregister_class(ANIM_OT_vertex_to_bones)

"""
if __name__== '__main__':
    register()
"""

