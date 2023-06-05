# Import the necessary modules
import bpy
import logging
import os

# Import the mathutils module for math operations
from mathutils import Vector

# Import the imbuf module for image processing
from imbuf import load as imbuf_load

# Import the translation function
from bpy.app.translations import pgettext_iface as iface_

# Define a custom operator class for creating a surface object from an image file
class DepthifyCreateSurfaceOperator(bpy.types.Operator):
    """Create a 3D surface from a depth map image"""

    # Define some metadata for the operator
    bl_idname = "object.depthify_create_surface"
    bl_label = iface_("Create Surface")
    bl_options = {'REGISTER', 'UNDO'}

    # Define a function to execute the operator
    def execute(self, context):
        # Get the current scene and its properties
        scene = context.scene
        props = scene.depthify_properties

        # Get the image file path from the image property
        image_file = props.image

        # Validate the image file path
        if not image_file:
            # Log an error message to the console and the UI
            logging.error("No image file selected")
            self.report({'ERROR'}, "No image file selected")
            return {'CANCELLED'}

        # Get the absolute path of the image file
        try:
            image_file = bpy.path.abspath(image_file)
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Invalid image file path: {e}")
            self.report({'ERROR'}, f"Invalid image file path: {e}")
            return {'CANCELLED'}

        # Check if the image file exists and is readable
        if not os.path.exists(image_file) or not os.access(image_file, os.R_OK):
            # Log an error message to the console and the UI
            logging.error(f"Image file not found or not readable: {image_file}")
            self.report({'ERROR'}, f"Image file not found or not readable: {image_file}")
            return {'CANCELLED'}

        # Load the image file using imbuf module
        try:
            image = imbuf_load(image_file)
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Failed to load image file: {e}")
            self.report({'ERROR'}, f"Failed to load image file: {e}")
            return {'CANCELLED'}

        # Get the width and height of the image
        width = image.width
        height = image.height

        # Get the depth map values from the image pixels
        depth_map = [pixel[0] for pixel in image.pixels]

        # Store the depth map values in the depth map property
        props.depth_map.clear()
        props.depth_map.extend(depth_map)

        # Create a surface object using depthify module
        try:
            surface = depthify.create_surface(width, height, depth_map)
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Failed to create surface object: {e}")
            self.report({'ERROR'}, f"Failed to create surface object: {e}")
            return {'CANCELLED'}

        # Store the surface object in the surface property
        props.surface = surface

        # Apply adaptive subdivision to the surface object using depthify module
        try:
            depthify.apply_adaptive_subdivision(surface, props.subdivisions, props.subdivision_type)
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Failed to apply adaptive subdivision: {e}")
            self.report({'ERROR'}, f"Failed to apply adaptive subdivision: {e}")
            return {'CANCELLED'}

        # Apply displacement to the surface object using depthify module
        try:
            depthify.apply_displacement(surface, props.displacement_strength, props.displacement_type)
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Failed to apply displacement: {e}")
            self.report({'ERROR'}, f"Failed to apply displacement: {e}")
            return {'CANCELLED'}

        # Scale the surface object using depthify module
        try:
            depthify.scale_surface(surface, props.scale)
        except Exception as e:
            # Log an error message to the console and the UI
            logging.error(f"Failed to scale surface object: {e}")
            self.report({'ERROR'}, f"Failed to scale surface object: {e}")
            return {'CANCELLED'}

        # Link the surface object to the scene
        scene.collection.objects.link(surface)

        # Set the surface object as the active object
        scene.view_layers[0].objects.active = surface

        # Log a success message to the console and the UI
        logging.info(f"Surface object created from image file: {image_file}")
        self.report({'INFO'}, f"Surface object created from image file: {image_file}")

        # Return a success status
        return {'FINISHED'}

# Define a function to register the operator class
def register():
    # Register the operator class
    bpy.utils.register_class(DepthifyCreateSurfaceOperator)

# Define a function to unregister the operator class
def unregister():
    # Unregister the operator class
    bpy.utils.unregister_class(DepthifyCreateSurfaceOperator)
