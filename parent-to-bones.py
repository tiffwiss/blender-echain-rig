import bpy

armature_name = "EChain_Armature"
mesh_prefix = "Link_Mesh_"
bone_prefix = "Link_"

# Find how many mesh objects exist
mesh_objs = [obj for obj in bpy.data.objects if obj.name.startswith(mesh_prefix)]
mesh_count = len(mesh_objs)

armature = bpy.data.objects[armature_name]

for i in range(mesh_count):
    mesh_name = f"{mesh_prefix}{i:03}"
    bone_name = f"{bone_prefix}{i:03}"

    mesh = bpy.data.objects.get(mesh_name)
    if not mesh:
        print(f"❌ Mesh '{mesh_name}' not found.")
        continue

    # 1. Save the current world transform
    original_matrix = mesh.matrix_world.copy()

    # 2. Parent to bone
    mesh.parent = armature
    mesh.parent_type = 'BONE'
    mesh.parent_bone = bone_name

    # 3. Restore original world transform
    mesh.matrix_world = original_matrix

print("All meshes parented to bones without shifting.")
