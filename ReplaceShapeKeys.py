import bpy
from mathutils import Vector

# Parse the file to extract frame data
def parse_coordinates(file_path):
    frame_data = {}
    with open(file_path, "r") as file:
        current_frame = None
        for line in file:
            line = line.strip()
            if line.startswith("Frame:"):
                current_frame = int(line.split(":")[1].strip())
                frame_data[current_frame] = []
            elif line.startswith("Vertex:") and current_frame is not None:
                parts = line.split(", ")
                try:
                    x = float(parts[1].split(":")[1].strip())
                    y = float(parts[2].split(":")[1].strip())
                    z = float(parts[3].split(":")[1].strip())
                    frame_data[current_frame].append((x, y, z))
                except ValueError:
                    print(f"Invalid data format in line: {line}")
    return frame_data

# Remove all shape keys from the object
def remove_all_shape_keys(obj):
    if obj and obj.data.shape_keys:
        keys = obj.data.shape_keys
        for _ in range(len(keys.key_blocks)):
            obj.shape_key_remove(keys.key_blocks[0])  # Remove each shape key
        print(f"Removed all shape keys from {obj.name}.")
    else:
        print(f"No shape keys to remove for {obj.name if obj else 'None'}.")

# Add shape keys for animation
def add_shape_keys(obj, frame_data):
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")
    
    # Ensure the number of vertices in the object matches the frame data
    num_vertices = len(obj.data.vertices)
    
    for frame, vertices in frame_data.items():
        if len(vertices) != num_vertices:
            print(f"Warning: Number of vertices in frame {frame} does not match the object.")
            continue
        
        shape_key = obj.shape_key_add(name=f"Frame_{frame}")
        
        # Ensure the shape key has the same number of vertices as the object
        for i, vertex in enumerate(vertices):
            if i < len(shape_key.data):  # Ensure index is valid
                shape_key.data[i].co = Vector(vertex)
            else:
                print(f"Warning: Vertex index {i} out of bounds for shape key {shape_key.name}.")
        
        # Animate the shape key influence
        for other_frame in frame_data.keys():
            shape_key.value = 1.0 if other_frame == frame else 0.0
            shape_key.keyframe_insert(data_path="value", frame=other_frame)

# Main Execution
file_path = "Your Filepath!" # Update to your file path
frame_data = parse_coordinates(file_path)

# Ensure the object exists
obj_name = "DynamicMesh"  # Update with your object's name
obj = bpy.data.objects.get(obj_name)

if obj:
    remove_all_shape_keys(obj)  # Remove existing shape keys
    add_shape_keys(obj, frame_data)  # Add new shape keys
    print(f"Shape keys recreated for {obj_name}.")
else:
    print(f"Object '{obj_name}' not found.")
