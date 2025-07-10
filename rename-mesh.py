import bpy

# Reset selection
bpy.ops.object.select_all(action='DESELECT')

# Grab all link meshes
link_objs = [obj for obj in bpy.data.objects if obj.name.startswith("Link_Mesh_") or obj.name.startswith("EChain_Controller")]

# Sort based on position along the Y-axis (or change axis as needed)
sorted_objs = sorted(link_objs, key=lambda o: o.location.y)

# Rename each based on sorted order
for i, obj in enumerate(sorted_objs):
    obj.name = f"Link_Mesh_{i:03}"

print("Meshes renamed in spatial order.")
