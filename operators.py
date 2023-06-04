# Import the necessary modules
import bpy
import os

# Define some helper functions for the addon logic

def create_material(name):
    """Create a new material with a given name.

    Args:
        name (str): The name of the material.

    Returns:
        bpy.types.Material: The material that was created.
    """
    # Create a new material using bpy.data.materials.new()
    material = bpy.data.materials.new(name)

    # Enable nodes for the material using material.use_nodes = True
    material.use_nodes = True

    # Return the material
    return material


def create_image_texture_node(material, image_path, color_space):
    """Create an image texture node for a material with a given image path and color space.

    Args:
        material (bpy.types.Material): The material to create the node for.
        image_path (str): The path of the image file to load.
        color_space (str): The color space of the image ('COLOR' or 'NONE').

    Returns:
        bpy.types.ShaderNodeTexImage: The image texture node that was created.
    """
    # Get the node tree of the material using material.node_tree
    node_tree = material.node_tree

    # Get the nodes and links of the node tree using node_tree.nodes and node_tree.links
    nodes = node_tree.nodes
    links = node_tree.links

    # Create a new image texture node using nodes.new('ShaderNodeTexImage')
    image_node = nodes.new('ShaderNodeTexImage')

    # Load the image from the image path using bpy.data.images.load()
    image = bpy.data.images.load(image_path)

    # Set the color space of the image using image.colorspace_settings.name
    image.colorspace_settings.name = color_space

    # Assign the image to the image texture node using image_node.image = image
    image_node.image = image

    # Return the image texture node
    return image_node


def create_displacement_node(material):
    """Create a displacement node for a material.

    Args:
        material (bpy.types.Material): The material to create the node for.

    Returns:
        bpy.types.ShaderNodeDisplacement: The displacement node that was created.
    """
    # Get the node tree of the material using material.node_tree
    node_tree = material.node_tree

    # Get the nodes and links of the node tree using node_tree.nodes and node_tree.links
    nodes = node_tree.nodes
    links = node_tree.links

    # Create a new displacement node using nodes.new('ShaderNodeDisplacement')
    displacement_node = nodes.new('ShaderNodeDisplacement')

    # Return the displacement node
    return displacement_node


def create_principled_node(material):
    """Create a principled BSDF node for a material.

    Args:
        material (bpy.types.Material): The material to create the node for.

    Returns:
        bpy.types.ShaderNodeBsdfPrincipled: The principled BSDF node that was created.
    """
    
     # Get the node tree of the material using material.node_tree
     node_tree = material.node_tree

     # Get the nodes and links of the node tree using node_tree.nodes and node_tree.links
     nodes = node_tree.nodes
     links = node_tree.links

     # Create a new principled BSDF node using nodes.new('ShaderNodeBsdfPrincipled')
     principled_node = nodes.new('ShaderNodeBsdfPrincipled')

     # Return the principled BSDF node
     return principled_node


def create_output_node(material):
     """Create an output node for a material.

     Args:
         material (bpy.types.Material): The material to create the node for.

     Returns:
         bpy.types.ShaderNodeOutputMaterial: The output node that was created.
     """
     # Get the node tree of the material using material.node_tree
     node_tree = material.node_tree

     # Get the nodes and links of the node tree using node_tree.nodes and node_tree.links
     nodes = node_tree.nodes
     links = node_tree.links

     # Create a new output node using nodes.new('ShaderNodeOutputMaterial')
     output_node = nodes.new('ShaderNodeOutputMaterial')

     # Return the output node
     return output_node


def create_subdivision_modifier(object, levels, render_levels):
    """Create a subdivision modifier for an object with given levels and render levels.

    Args:
        object (bpy.types.Object): The object to create the modifier for.
        levels (int): The number of subdivisions to apply in the viewport.
        render_levels (int): The number of subdivisions to apply in the render.

    Returns:
        bpy.types.SubsurfModifier: The subdivision modifier that was created.
    """
    # Create a new subdivision modifier using object.modifiers.new()
    modifier = object.modifiers.new(name='Subdivision', type='SUBSURF')

    # Set the levels and render levels of the modifier using modifier.levels and modifier.render_levels
    modifier.levels = levels
    modifier.render_levels = render_levels

    # Return the modifier
    return modifier


def create_plane_object(name, location, rotation, scale):
    """Create a plane object with a given name, location, rotation, and scale.

    Args:
        name (str): The name of the object.
        location (tuple): The location of the object as a 3D vector.
        rotation (tuple): The rotation of the object as a 3D vector in radians.
        scale (tuple): The scale of the object as a 3D vector.

    Returns:
        bpy.types.Object: The plane object that was created.
    """
    # Create a new plane mesh using bpy.data.meshes.new()
    mesh = bpy.data.meshes.new(name)

    # Create a new plane object using bpy.data.objects.new()
    object = bpy.data.objects.new(name, mesh)

    # Link the object to the current collection using bpy.context.collection.objects.link()
    bpy.context.collection.objects.link(object)

    # Set the location, rotation, and scale of the object using object.location, object.rotation_euler, and object.scale
    object.location = location
    object.rotation_euler = rotation
    object.scale = scale

    # Return the object
    return object
