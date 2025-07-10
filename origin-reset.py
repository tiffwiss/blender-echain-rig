import bpy
import mathutils

# Configuration
Y_OFFSET = -0.03355  # Offset in the -Y direction (half of hinge distance) (Dfault is 0.3355)

# Process all chain link meshes
for obj in bpy.data.objects:
    if obj.name.startswith("EChain_Controller"):
        print(f"Processing: {obj.name}")
        
        # Set geometry origin to center first
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        
        # Create offset vector (no change in X and Z)
        offset = mathutils.Vector((0.0, Y_OFFSET, 0.0))
        
        # Go into Edit Mode and move geometry opposite to the desired origin offset
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(-offset.x, -offset.y, -offset.z))
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Deselect the object
        obj.select_set(False)

print("Origins offset by {:.4f} units in -Y direction.".format(abs(Y_OFFSET)))
