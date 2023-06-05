# Import the necessary modules
import bpy
import math

# Import the mathutils module for math operations
from mathutils import Vector

# Import the translation function
from bpy.app.translations import pgettext_iface as iface_

# Import the bpy.app.timers module for creating progress bar and status message
import bpy.app.timers

# Define a global variable to store the timer object
timer = None

# Define a function to create a surface object from the width, height, and depth map values
def create_surface(width, height, depth_map):
    """Create a surface object from the width, height, and depth map values.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        depth_map (list): The list of depth map values.

    Returns:
        bpy.types.Object: The surface object that was created.
    """

    # Create a list of vertices for the surface object
    vertices = []

    # Create a list of faces for the surface object
    faces = []

    # Loop through the rows and columns of the image
    for row in range(height):
        for col in range(width):
            # Get the depth value from the depth map
            depth = depth_map[row * width + col]

            # Calculate the x, y, and z coordinates of the vertex
            x = col - width / 2
            y = row - height / 2
            z = depth * 10

            # Append the vertex to the vertices list
            vertices.append(Vector((x, y, z)))

            # Check if we can create a face with the current and previous vertices
            if row > 0 and col > 0:
                # Calculate the indices of the vertices that form the face
                i1 = (row - 1) * width + (col - 1)
                i2 = (row - 1) * width + col
                i3 = row * width + col
                i4 = row * width + (col - 1)

                # Append the face to the faces list
                faces.append([i1, i2, i3, i4])

    # Create a new mesh data block with the vertices and faces
    mesh = bpy.data.meshes.new("Surface")

    # Assign the vertices and faces to the mesh
    mesh.from_pydata(vertices, [], faces)

    # Update the mesh with the new data
    mesh.update()

    # Create a new object with the mesh data block
    obj = bpy.data.objects.new("Surface", mesh)

    # Return the object
    return obj

# Define a function to apply adaptive subdivision to a surface object
def apply_adaptive_subdivision(obj, subdivisions, subdivision_type):
    """Apply adaptive subdivision to a surface object.

    Args:
        obj (bpy.types.Object): The surface object.
        subdivisions (int): The number of subdivisions.
        subdivision_type (str): The type of subdivision method.

    Returns:
        None.
    """

    # Get the context and scene
    context = bpy.context
    scene = context.scene

    # Set the cycles render engine as active
    scene.render.engine = 'CYCLES'

    # Set the experimental feature set as active
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # Create a new subdivision surface modifier for the object
    modifier = obj.modifiers.new("Subdivision", 'SUBSURF')

    # Set the modifier properties
    modifier.subdivision_type = subdivision_type
    modifier.levels = subdivisions
    modifier.render_levels = subdivisions

    # Enable adaptive subdivision for the modifier
    modifier.use_adaptive_subdivision = True

# Define a function to apply displacement to a surface object
def apply_displacement(obj, displacement_strength, displacement_type):
    """Apply displacement to a surface object.

    Args:
        obj (bpy.types.Object): The surface object.
        displacement_strength (float): The strength of the displacement modifier.
        displacement_type (str): The type of displacement method.

    Returns:
        None.
    """

     # Get the context and scene
    context = bpy.context
    scene = context.scene

    # Set the cycles render engine as active
    scene.render.engine = 'CYCLES'

    # Set the experimental feature set as active
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # Create a new material for the object using operators module
    from .operators import create_materials

    material = create_materials("Surface")

    # Assign the material to the object's active material slot
    obj.active_material = material

    # Get the material nodes and links
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Get the output node and the principled BSDF node
    output_node = nodes.get("Material Output")
    principled_node = nodes.get("Principled BSDF")

    # Create a new image texture node for the depth map image
    image_node = nodes.new("ShaderNodeTexImage")

    # Set the image node properties
    image_node.image = bpy.data.images.load(bpy.path.abspath(scene.depthify_properties.image))
    image_node.interpolation = 'Closest'

    # Create a new displacement node for the displacement output
    displacement_node = nodes.new("ShaderNodeDisplacement")

    # Set the displacement node properties
    displacement_node.inputs['Scale'].default_value = displacement_strength

    # Link the image node to the principled node and the displacement node
    links.new(image_node.outputs['Color'], principled_node.inputs['Base Color'])
    links.new(image_node.outputs['Color'], displacement_node.inputs['Height'])

    # Link the displacement node to the output node
    links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])

    # Set the displacement method for the material
    material.cycles.displacement_method = displacement_type

# Define a function to scale a surface object
def scale_surface(obj, scale):
    """Scale a surface object.

    Args:
        obj (bpy.types.Object): The surface object.
        scale (tuple): The scale factors for x, y, and z axes.

    Returns:
        None.
    """

    # Set the scale property of the object
    obj.scale = Vector(scale)

# Define a function to update the progress bar and status message
def update_progress():
    """Update the progress bar and status message.

    Returns:
        float: The time interval for the next update.
    """

    # Get the context and scene
    context = bpy.context
    scene = context.scene

    # Get the current progress value from the scene property
    progress = scene.depthify_properties.progress

    # Check if the progress is complete
    if progress >= 1.0:
        # Log a success message to the console and the UI
        logging.info("Depthify process completed")
        bpy.ops.wm.progress_end()
        bpy.ops.wm.report({'INFO'}, "Depthify process completed")

        # Return None to stop the timer
        return None

    # Update the progress bar and status message using operators module
    bpy.ops.wm.progress_update(value=int(progress * 100))
    bpy.ops.wm.report({'INFO'}, f"Depthify process in progress: {progress * 100:.2f}%")

    # Increment the progress value by 0.1
    progress += 0.1

    # Store the progress value in the scene property
    scene.depthify_properties.progress = progress

    # Return 0.5 as the time interval for the next update
    return 0.5

# Define a function to register a timer for updating the progress bar and status message
def register_timer():
    """Register a timer for updating the progress bar and status message.

    Returns:
        None.
    """

    # Get the context and scene
    context = bpy.context
    scene = context.scene

    # Initialize the progress value to zero and store it in the scene property
    scene.depthify_properties.progress = 0.0

    # Start a progress bar using operators module
    bpy.ops.wm.progress_begin(min=0, max=100)

    # Create a global variable to store the timer object
    global timer

    # Register a timer with an initial time interval of 0.5 seconds and a callback function of update_progress
    timer = bpy.app.timers.register(update_progress, first_interval=0.5)

# Define a function to unregister the timer for updating the progress bar and status message
def unregister_timer():
    """Unregister the timer for updating the progress bar and status message.

    Returns:
        None.
    """

    # Get the context and scene
    context = bpy.context
    scene = context.scene

    # Create a global variable to store the timer object
    global timer

    # Check if the timer is registered
    if timer:
        # Unregister the timer using timers module
        bpy.app.timers.unregister(timer)

        # Set the timer object to None
        timer = None

# Define a function to register Depthify module with Blender handlers module 
def register():
   """Register depthify module with Blender handlers module.

   Returns:
       None.
   """

   # Register a callback function with load_post handler to update image and depth map properties when loading a file 
   bpy.app.handlers.load_post.append(update_image_and_depth_map)

   # Register a callback function with save_pre handler to unregister timer when saving a file
   bpy.app.handlers.save_pre.append(unregister_timer)

# Define a function to unregister Depthify module from Blender handlers module
def unregister():
   """Unregister depthify module from Blender handlers module.

   Returns:
       None.
   """

   # Unregister the callback function from save_pre handler
   bpy.app.handlers.save_pre.remove(unregister_timer)

   # Unregister the callback function from load_post handler
   bpy.app.handlers.load_post.remove(update_image_and_depth_map)

# Define a function to update image and depth map properties when loading a file
def update_image_and_depth_map(dummy):
    """Update image and depth map properties when loading a file.

    Args:
        dummy: A dummy argument to match the handler signature.

    Returns:
        None.
    """

    # Get the context and scene
    context = bpy.context
    scene = context.scene

    # Get the image and depth map properties
    image = scene.depthify_properties.image
    depth_map = scene.depthify_properties.depth_map

    # Check if the image property is not empty
    if image:
        # Try to load the image file using imbuf module
        try:
            image = imbuf_load(bpy.path.abspath(image))
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Failed to load image file: {e}")
            bpy.ops.wm.report({'ERROR'}, f"Failed to load image file: {e}")
            return

        # Get the width and height of the image
        width = image.width
        height = image.height

        # Get the depth map values from the image pixels
        depth_map = [pixel[0] for pixel in image.pixels]

        # Store the depth map values in the depth map property
        scene.depthify_properties.depth_map.clear()
        scene.depthify_properties.depth_map.extend(depth_map)

# Define a function to register Depthify module with Blender handlers module 
def register():
   """Register depthify module with Blender handlers module.

   Returns:
       None.
   """

   # Register a callback function with load_post handler to update image and depth map properties when loading a file 
   bpy.app.handlers.load_post.append(update_image_and_depth_map)

   # Register a callback function with save_pre handler to unregister timer when saving a file
   bpy.app.handlers.save_pre.append(unregister_timer)

# Define a function to unregister Depthify module from Blender handlers module
def unregister():
   """Unregister depthify module from Blender handlers module.

   Returns:
       None.
   """

   # Unregister the callback function from save_pre handler
   bpy.app.handlers.save_pre.remove(unregister_timer)

   # Unregister the callback function from load_post handler
   bpy.app.handlers.load_post.remove(update_image_and_depth_map)

