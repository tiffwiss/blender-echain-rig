import bpy
import mathutils
import math
from mathutils import Vector

# ------------------------
# Configuration
# ------------------------
curve_name = "EChain_Loop_Path"   # Replace with your curve object name
curve_obj = bpy.data.objects[curve_name]
curve = curve_obj.data
spline = curve.splines[0]

def get_curve_points(curve_obj, spacing):
    """Get points along straight curve at exact spacing intervals"""
    points = []
    curve = curve_obj.data
    spline = curve.splines[0]
    
    if spline.type != 'NURBS':
        raise ValueError("This script only works with NURBS curves")
    
    # Get start and end points
    start_point = spline.points[0].co.xyz
    end_point = spline.points[-1].co.xyz
    
    # Get total length
    curve_length = (end_point - start_point).length
    num_segments = int(curve_length / spacing)
    
    # Create points at exact intervals along straight line
    matrix = curve_obj.matrix_world
    direction = (end_point - start_point).normalized()
    
    for i in range(num_segments + 1):
        # Calculate position at exact spacing
        distance = min(i * spacing, curve_length)
        point = start_point + (direction * distance)
        pos = matrix @ point
        points.append(pos)
    
    return points

# Calculate points at exact intervals
bone_length = 0.0671  # Exact value from Geometry Nodes (this is the exact hinge distance)
eval_points = get_curve_points(curve_obj, bone_length)
bone_count = len(eval_points)
print(f"Generated {bone_count} points at {bone_length} unit intervals")

armature_name = "EChain_Armature"

# ------------------------
# Create Armature & Object
# ------------------------
# First ensure we're in object mode and nothing is selected
if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')

# Create new armature and set it as active
bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
armature = bpy.context.active_object
armature.name = armature_name
arm = armature.data
arm.name = armature_name + "_Data"

# Now we can safely enter edit mode
bpy.ops.object.mode_set(mode='EDIT')

# Clear default bone
if len(arm.edit_bones) > 0:
    arm.edit_bones.remove(arm.edit_bones[0])

# ------------------------
# Create Bone Chain
# ------------------------
prev_bone = None
for i in range(len(eval_points)):
    bone = arm.edit_bones.new(f"Link_{i:03}")
    bone.head = eval_points[i]
    
    # Calculate tail position
    if i < len(eval_points) - 1:
        # Point bone towards next point
        direction = eval_points[i+1] - eval_points[i]
    elif prev_bone:
        # For last bone, use same direction as previous bone
        direction = prev_bone.tail - prev_bone.head
    else:
        # Fallback direction (shouldn't happen in practice)
        direction = Vector((0.0, bone_length, 0.0))
    
    # Ensure exact bone length
    bone.tail = bone.head + direction.normalized() * bone_length
    
    # Verify bone length
    actual_length = (bone.tail - bone.head).length
    if abs(actual_length - bone_length) > 0.0001:
        print(f"Warning: Bone {i} length {actual_length:.6f} differs from target {bone_length}")
    
    # Parenting
    if prev_bone:
        bone.parent = prev_bone
        bone.use_connect = True
    
    prev_bone = bone

bpy.ops.object.mode_set(mode='POSE')

# Add constraints to each pose bone
for pbone in armature.pose.bones:
    # Limit Rotation constraint
    constraint = pbone.constraints.new('LIMIT_ROTATION')
    constraint.use_limit_x = True
    constraint.min_x = math.radians(-20)
    constraint.max_x = math.radians(20)
    
    constraint.use_limit_y = True
    constraint.min_y = 0
    constraint.max_y = 0

    constraint.use_limit_z = True
    constraint.min_z = 0
    constraint.max_z = 0

    constraint.owner_space = 'LOCAL'

    # Lock Y/Z rotation
    pbone.lock_rotation[1] = True  # Y
    pbone.lock_rotation[2] = True  # Z

# Print final status
print(f"Created armature with {len(armature.pose.bones)} bones")
