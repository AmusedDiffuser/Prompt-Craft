# Import the necessary modules
import bpy
import os

# Import some helper functions from operators module using relative import
from .operators import (
     create_material,
     create_image_texture_node,
     create_displacement_node,
     create_principled_node,
     create_output_node,
     create_subdivision_modifier,
     create_plane_object
)

# Define a custom operator class for the addon logic
class DepthifyOperator(bpy.types.Operator):
     """A custom operator for creating a 3D surface from a depth map image"""

     # Define some metadata for the operator
     bl_idname = "object.depthify"
     bl_label = "Depthify Operator"
     bl_options = {'REGISTER', 'UNDO'}

     # Define a class method to check if there is an active object in the context using @classmethod and cls parameter
     @classmethod
     def poll(cls, context):
          return context.active_object is not None

     # Define a function to execute the operator
     def execute(self, context):
          # Get the current object and its properties
          obj = context.object
          props = obj.depthify_props
          image_path = props.image_path
          output_path = props.output_path
          invert_depth = props.invert_depth
          depth_scale = props.depth_scale
          background_color = props.background_color
          anti_aliasing = props.anti_aliasing
          output_format = props.output_format
          output_name = props.output_name

          # Check if the image path is valid and exists using os.path.isfile()
          if not os.path.isfile(image_path):
               # Report an error message and return cancelled using self.report() and return {'CANCELLED'}
               self.report({'ERROR'}, f"Invalid image path: {image_path}")
               return {'CANCELLED'}

          # Check if the output path is valid and exists using os.path.isdir()
          if not os.path.isdir(output_path):
               # Report an error message and return cancelled using self.report() and return {'CANCELLED'}
               self.report({'ERROR'}, f"Invalid output path: {output_path}")
               return {'CANCELLED'}

          # Check if the output name is valid and not empty using bool()
          if not output_name:
               # Report an error message and return cancelled using self.report() and return {'CANCELLED'}
               self.report({'ERROR'}, f"Invalid output name: {output_name}")
               return {'CANCELLED'}

          try:
               # Import the image as plane using import_image_as_plane()
               depth_plane = self.import_image_as_plane(image_path)

               # Set up adaptive subdivision and displacement for the depth plane using setup_adaptive_subdivision_and_displacement()
               depth_material, depth_modifier = self.setup_adaptive_subdivision_and_displacement(depth_plane, depth_scale)

               # Invert the depth map if the invert depth option is enabled using if statement and invert_depth_map()
               if invert_depth:
                    self.invert_depth_map(depth_material)

               # Set up a background plane with a solid color using setup_background_plane()
               background_plane = self.setup_background_plane(background_color)

               # Join the depth plane and the background plane into one object using join_planes()
               joined_plane = self.join_planes(depth_plane, background_plane)

               # Render the 3D surface to an image file using render_image()
               self.render_image(joined_plane, output_path, anti_aliasing, output_format, output_name)

               # Report a success message and return finished using self.report() and return {'FINISHED'}
               self.report({'INFO'}, "Depthify completed successfully")
               return {'FINISHED'}

          except Exception as e:
               # Report an error message with the exception and return cancelled using self.report() and return {'CANCELLED'}
               self.report({'ERROR'}, f"Depthify failed with exception: {e}")
               return {'CANCELLED'}


     # Define a function to import an image as plane using the addon
     def import_image_as_plane(self, image_path):
          """Import an image as plane using the addon.

          Args:
              image_path (str): The path of the image file to import.

          Returns:
              bpy.types.Object: The plane object that was imported.
          """
          
          # Save the current context mode using bpy.context.mode
          mode = bpy.context.mode

          # Switch to object mode using bpy.ops.object.mode_set()
          bpy.ops.object.mode_set(mode='OBJECT')

          # Enable the import images as planes addon using bpy.ops.preferences.addon_enable()
          bpy.ops.preferences.addon_enable(module='io_import_images_as_planes')

          # Import the image as plane using bpy.ops.import_image.to_plane()
          bpy.ops.import_image.to_plane(files=[{'name': image_path}])

          # Get the imported plane object using bpy.context.active_object
          plane_object = bpy.context.active_object

          # Switch back to the original mode using bpy.ops.object.mode_set()
          bpy.ops.object.mode_set(mode=mode)

          # Return the plane object
          return plane_object


     # Define a function to set up adaptive subdivision and displacement for a plane object
def setup_adaptive_subdivision_and_displacement(self, plane_object, depth_scale):
     """Set up adaptive subdivision and displacement for a plane object.

     Args:
         plane_object (bpy.types.Object): The plane object to set up.
         depth_scale (float): The scale factor for the depth map values.

     Returns:
         tuple: A tuple of (material, modifier) that were set up.
     """
     # Get the material of the plane object using plane_object.active_material
     material = plane_object.active_material

     # Get the image texture node of the material using material.node_tree.nodes['Image Texture']
     image_node = material.node_tree.nodes['Image Texture']

     # Create a displacement node for the material using create_displacement_node()
     displacement_node = create_displacement_node(material)

     # Create an output node for the material using create_output_node()
     output_node = create_output_node(material)

     # Link the image texture node to the displacement node using material.node_tree.links.new()
     material.node_tree.links.new(image_node.outputs['Color'], displacement_node.inputs['Height'])

     # Link the displacement node to the output node using material.node_tree.links.new()
     material.node_tree.links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])

     # Set the scale of the displacement node using displacement_node.inputs['Scale'].default_value
     displacement_node.inputs['Scale'].default_value = depth_scale

     # Set the displacement method of the material to 'DISPLACEMENT' using material.cycles.displacement_method
     material.cycles.displacement_method = 'DISPLACEMENT'

     # Create a subdivision modifier for the plane object using create_subdivision_modifier()
     modifier = create_subdivision_modifier(plane_object, levels=0, render_levels=1)

     # Set the subdivision type of the modifier to 'CATMULL_CLARK' using modifier.subdivision_type
     modifier.subdivision_type = 'CATMULL_CLARK'

     # Enable adaptive subdivision for the modifier using modifier.use_adaptive_subdivision
     modifier.use_adaptive_subdivision = True

     # Set the dicing scale of the modifier to 1.0 using modifier.dicing_rate
     modifier.dicing_rate = 1.0

     # Return a tuple of (material, modifier) that were set up
     return (material, modifier)


# Define a function to invert the depth map in a material
def invert_depth_map(self, material):
    """Invert the depth map values in a material.

    Args:
        material (bpy.types.Material): The material to invert.
    """
    # Get the image texture node of the material using material.node_tree.nodes['Image Texture']
    image_node = material.node_tree.nodes['Image Texture']

    # Get the displacement node of the material using material.node_tree.nodes['Displacement']
    displacement_node = material.node_tree.nodes['Displacement']

    # Invert the color output of the image texture node using image_node.outputs['Color'].default_value
    image_node.outputs['Color'].default_value = 1.0 - image_node.outputs['Color'].default_value

    # Invert the scale input of the displacement node using displacement_node.inputs['Scale'].default_value
    displacement_node.inputs['Scale'].default_value = -displacement_node.inputs['Scale'].default_value


# Define a function to set up a background plane with a solid color
def setup_background_plane(self, background_color):
    """Set up a background plane with a solid color.

    Args:
        background_color (tuple): The color of the background plane as a 3D vector.

    Returns:
        bpy.types.Object: The background plane object that was created.
    """
    # Create a new plane object using create_plane_object()
    background_plane = create_plane_object(name='Background', location=(0.0, 0.0, -1.0), rotation=(0.0, 0.0, 0.0), scale=(10.0, 10.0, 10.0))

    # Create a new material for the background plane using create_material()
    background_material = create_material(name='Background')

    # Assign the material to the background plane using background_plane.active_material
    background_plane.active_material = background_material

    # Create a principled BSDF node for the background material using create_principled_node()
    principled_node = create_principled_node(background_material)

    # Create an output node for the background material using create_output_node()
    output_node = create_output_node(background_material)

    # Link the principled BSDF node to the output node using background_material.node_tree.links.new()
    background_material.node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Set the base color of the principled BSDF node to the background color using principled_node.inputs['Base Color'].default_value
    principled_node.inputs['Base Color'].default_value = background_color

    # Return the background plane object
    return background_plane


# Define a function to join two planes into one object
def join_planes(self, plane1, plane2):
    """Join two planes into one object.

    Args:
        plane1 (bpy.types.Object): The first plane object to join.
        plane2 (bpy.types.Object): The second plane object to join.

    Returns:
        bpy.types.Object: The joined plane object that was created.
    """
    # Save the current context mode using bpy.context.mode
    mode = bpy.context.mode

    # Switch to object mode using bpy.ops.object.mode_set()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Select both planes using plane1.select_set() and plane2.select_set()
    plane1.select_set(True)
    plane2.select_set(True)

    # Set the first plane as the active object using bpy.context.view_layer.objects.active
    bpy.context.view_layer.objects.active = plane1

    # Join the planes using bpy.ops.object.join()
    bpy.ops.object.join()

    # Get the joined plane object using bpy.context.active_object
    joined_plane = bpy.context.active_object

    # Switch back to the original mode using bpy.ops.object.mode_set()
    bpy.ops.object.mode_set(mode=mode)

    # Return the joined plane object
    return joined_plane


# Define a function to render a 3D surface to an image file
def render_image(self, plane_object, output_path, anti_aliasing, output_format, output_name):
     """Render a 3D surface to an image file.

     Args:
         plane_object (bpy.types.Object): The plane object to render.
         output_path (str): The path of the output directory.
         anti_aliasing (bool): Whether to enable anti-aliasing or not.
         output_format (str): The format of the output image file ('PNG', 'JPEG', 'BMP', or 'TIFF').
         output_name (str): The name of the output image file.
     """
     # Save the current context mode using bpy.context.mode
     mode = bpy.context.mode

     # Switch to object mode using bpy.ops.object.mode_set()
     bpy.ops.object.mode_set(mode='OBJECT')

     # Deselect all objects using bpy.ops.object.select_all()
     bpy.ops.object.select_all(action='DESELECT')

     # Select the plane object using plane_object.select_set()
     plane_object.select_set(True)

     # Set the plane object as the active object using bpy.context.view_layer.objects.active
     bpy.context.view_layer.objects.active = plane_object

     # Set the render engine to 'CYCLES' using bpy.context.scene.render.engine
     bpy.context.scene.render.engine = 'CYCLES'

     # Set the render device to 'GPU' if available using if statement and bpy.context.preferences.addons['cycles'].preferences.get_devices()
     devices = bpy.context.preferences.addons['cycles'].preferences.get_devices()
     if devices[0]:
          bpy.context.scene.cycles.device = 'GPU'

     # Set the render resolution to 1024 x 1024 pixels using bpy.context.scene.render.resolution_x and resolution_y
     bpy.context.scene.render.resolution_x = 1024
     bpy.context.scene.render.resolution_y = 1024

     # Set the render percentage to 100% using bpy.context.scene.render.resolution_percentage
     bpy.context.scene.render.resolution_percentage = 100

     # Enable or disable anti-aliasing based on the option using if statement and bpy.context.scene.render.use_antialiasing
     if anti_aliasing:
          bpy.context.scene.render.use_antialiasing = True
     else:
          bpy.context.scene.render.use_antialiasing = False

     # Set the render file format based on the option using if statement and bpy.context.scene.render.image_settings.file_format
     if output_format == 'PNG':
          bpy.context.scene.render.image_settings.file_format = 'PNG'
          extension = '.png'
     elif output_format == 'JPEG':
          bpy.context.scene.render.image_settings.file_format = 'JPEG'
          extension = '.jpg'
     elif output_format == 'BMP':
          bpy.context.scene.render.image_settings.file_format = 'BMP'
          extension = '.bmp'
     elif output_format == 'TIFF':
          bpy.context.scene.render.image_settings.file_format = 'TIFF'
          extension = '.tif'

     # Set the render file path based on the output path and name using os.path.join() and bpy.context.scene.render.filepath
     file_path = os.path.join(output_path, output_name + extension)
     bpy.context.scene.render.filepath = file_path

     # Render the image using bpy.ops.render.render()
     bpy.ops.render.render(write_still=True)


# Define a function to register the addon components
def register():
     # Register the custom operator class using bpy.utils.register_class()
     bpy.utils.register_class(DepthifyOperator)


# Define a function to unregister the addon components
def unregister():
     # Unregister the custom operator class using bpy.utils.unregister_class()
     bpy.utils.unregister_class(DepthifyOperator)

