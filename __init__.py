# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Depthify",
    "author" : "Ariel Tavori",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

# Import the necessary modules
import bpy
import sys
import os

# Import the depthify and operators modules using relative imports
from . import depthify
from . import operators

# Define a custom panel class for the addon UI
class DepthifyPanel(bpy.types.Panel):
    """A custom panel for creating a 3D surface from a depth map image"""
    
    # Define some metadata for the panel
    bl_idname = "OBJECT_PT_depthify"
    bl_label = "Depthify"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # Define a function to draw the panel UI
    def draw(self, context):
        # Get the current object and its properties
        obj = context.object
        props = obj.depthify_props

        # Get the layout of the panel
        layout = self.layout

        # Create a file browser for selecting the depth map image using layout.prop_search()
        layout.prop_search(props, "image_path", bpy.data, "images", text="Depth Map Image")

        # Create a file browser for selecting the output directory using layout.prop()
        layout.prop(props, "output_path", text="Output Directory")

        # Create a checkbox for enabling or disabling depth inversion using layout.prop()
        layout.prop(props, "invert_depth", text="Invert Depth")

        # Create a slider for adjusting the depth scale using layout.prop()
        layout.prop(props, "depth_scale", text="Depth Scale")

        # Create a color picker for selecting the background color using layout.prop()
        layout.prop(props, "background_color", text="Background Color")

        # Create a checkbox for enabling or disabling anti-aliasing using layout.prop()
        layout.prop(props, "anti_aliasing", text="Anti-Aliasing")

        # Create a dropdown menu for selecting the output format using layout.prop()
        layout.prop(props, "output_format", text="Output Format")

        # Create a text input for entering the output name using layout.prop()
        layout.prop(props, "output_name", text="Output Name")

        # Create a button for executing the operator using layout.operator()
        layout.operator("object.depthify", text="Depthify")


# Define a custom property group class for storing the addon properties
class DepthifyProperties(bpy.types.PropertyGroup):
    
    # Define some metadata for each property using bpy.props

    # A string property for storing the path of the depth map image
    image_path: bpy.props.StringProperty(
        name="Image Path",
        description="The path of the depth map image",
        default="",
        subtype="FILE_PATH"
    )

    # A string property for storing the path of the output directory
    output_path: bpy.props.StringProperty(
        name="Output Path",
        description="The path of the output directory",
        default="",
        subtype="DIR_PATH"
    )

    # A boolean property for enabling or disabling depth inversion
    invert_depth: bpy.props.BoolProperty(
        name="Invert Depth",
        description="Invert the depth map values",
        default=False
    )

    # A float property for adjusting the depth scale
    depth_scale: bpy.props.FloatProperty(
        name="Depth Scale",
        description="The scale factor for the depth map values",
        default=0.1,
        min=0.0,
        max=1.0,
        step=0.01,
        precision=2
    )

    # A float vector property for selecting the background color
    background_color: bpy.props.FloatVectorProperty(
        name="Background Color",
        description="The color of the background plane",
        default=(0.0, 0.0, 0.0),
        min=0.0,
        max=1.0,
        subtype="COLOR"
    )

    # A boolean property for enabling or disabling anti-aliasing
    anti_aliasing: bpy.props.BoolProperty(
        name="Anti-Aliasing",
        description="Enable anti-aliasing for the render",
        default=True
    )

    # An enum property for selecting the output format
    output_format: bpy.props.EnumProperty(
        name="Output Format",
        description="The format of the output image file",
        items=[
            ('PNG', "PNG", "Portable Network Graphics"),
            ('JPEG', "JPEG", "Joint Photographic Experts Group"),
            ('BMP', "BMP", "Bitmap"),
            ('TIFF', "TIFF", "Tagged Image File Format")
        ],
        default='PNG'
    )

    # A string property for entering the output name
    output_name: bpy.props.StringProperty(
        name="Output Name",
        description="The name of the output image file",
        default="depthify_output"
    )


# Define a function to register the addon components
def register():
    
    # Register the custom property group class using bpy.utils.register_class()
    bpy.utils.register_class(DepthifyProperties)

    # Register a pointer property to store the addon properties in each object using bpy.types.Object.depthify_props
    bpy.types.Object.depthify_props = bpy.props.PointerProperty(type=DepthifyProperties)

    # Register the custom panel class using bpy.utils.register_class()
    bpy.utils.register_class(DepthifyPanel)

    # Register the custom operator class using depthify.register()
    depthify.register()


# Define a function to unregister the addon components
def unregister():
    
     # Unregister the custom operator class using depthify.unregister()
     depthify.unregister()

     # Unregister the custom panel class using bpy.utils.unregister_class()
     bpy.utils.unregister_class(DepthifyPanel)

     # Unregister the pointer property using del bpy.types.Object.depthify_props
     del bpy.types.Object.depthify_props

     # Unregister the custom property group class using bpy.utils.unregister_class()
     bpy.utils.unregister_class(DepthifyProperties)


# Run the register function if this file is executed as a script
if __name__ == "__main__":
     register()
