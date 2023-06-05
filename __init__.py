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
# Define some metadata for the addon
# Define some metadata for the addon

# Define some metadata for the addon
bl_info = {
    "name": "Depthify",
    "author": "Ariel Tavori",
    "description": "Create a 3D surface from a depth map image",
    "blender": (2, 80, 0),
    "version": (0, 0, 2),
    "location": "Properties > Object",
    "warning": "",
    "category": "Object"
}

# Import the necessary modules
import bpy
import logging

# Import translation functions
from bpy.app.translations import pgettext_iface as iface_
from bpy.app.translations import pgettext_tip as tip_

# Define a custom property group for storing and accessing properties
class DepthifyProperties(bpy.types.PropertyGroup):
    # Define an image property for selecting an image file
    image: bpy.props.StringProperty(
        name=iface_("Image"),
        description=tip_("Select an image file"),
        subtype='FILE_PATH'
    )

    # Define a depth map property for storing the depth map values
    depth_map: bpy.props.FloatVectorProperty(
        name=iface_("Depth Map"),
        description=tip_("Store the depth map values"),
        size=1
    )

    # Define a surface property for storing the surface object
    surface: bpy.props.PointerProperty(
        name=iface_("Surface"),
        description=tip_("Store the surface object"),
        type=bpy.types.Object
    )

    # Define a subdivisions property for adjusting the number of subdivisions
    subdivisions: bpy.props.IntProperty(
        name=iface_("Subdivisions"),
        description=tip_("Adjust the number of subdivisions for the surface"),
        default=2,
        min=0,
        max=6
    )

    # Define a displacement strength property for adjusting the strength of the displacement modifier
    displacement_strength: bpy.props.FloatProperty(
        name=iface_("Displacement Strength"),
        description=tip_("Adjust the strength of the displacement modifier for the surface"),
        default=1.0,
        min=0.0,
        max=10.0
    )

    # Define a scale property for adjusting the scale of the surface object
    scale: bpy.props.FloatVectorProperty(
        name=iface_("Scale"),
        description=tip_("Adjust the scale of the surface object"),
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=10.0,
        subtype='XYZ'
    )

    # Define a subdivision type property for choosing the type of subdivision method
    subdivision_type: bpy.props.EnumProperty(
        name=iface_("Subdivision Type"),
        description=tip_("Choose the type of subdivision method for the surface"),
        items=[
            ('SIMPLE', "Simple", "Use simple subdivision algorithm"),
            ('CATMULL_CLARK', "Catmull-Clark", "Use Catmull-Clark subdivision algorithm")
        ],
        default='CATMULL_CLARK'
    )

    # Define a displacement type property for choosing the type of displacement method
    displacement_type: bpy.props.EnumProperty(
        name=iface_("Displacement Type"),
        description=tip_("Choose the type of displacement method for the surface"),
        items=[
            ('BUMP', "Bump", "Use bump mapping to create an illusion of depth"),
            ('TRUE', "True", "Use true displacement to modify the geometry")
        ],
        default='TRUE'
    )

# Import the depthify and operators modules using absolute imports
from Depthify import depthify
from Depthify import operators

# Define a custom panel class for the addon UI
class DepthifyPanel(bpy.types.Panel):
    """A custom panel for creating a 3D surface from a depth map image"""

    # Define some metadata for the panel
    bl_idname = "OBJECT_PT_depthify"
    bl_label = iface_("Depthify")
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # Define a function to draw the panel UI
    def draw(self, context):
        # Get the current object and its properties
        obj = context.object
        props = context.scene.depthify_properties

        # Create a layout for the panel UI
        layout = self.layout

        # Use a file browser template to select an image file
        layout.template_ID(props, "image", open="image.open")

        # Use a row to display a button to create a surface object from the image file
        row = layout.row()
        row.operator("object.depthify_create_surface")

        # Use a column to display properties to adjust the surface object
        col = layout.column()
        
        # Use a slider to adjust the number of subdivisions
        col.prop(props, "subdivisions")

        # Use an enum menu to choose the type of subdivision method
        col.prop(props, "subdivision_type", text="")

        # Use a slider to adjust the strength of the displacement modifier
        col.prop(props, "displacement_strength")

        # Use an enum menu to choose the type of displacement method
        col.prop(props, "displacement_type", text="")

        # Use a vector slider to adjust the scale of the surface object
        col.prop(props, "scale")

# Define a function to register translation dictionaries
def register_translations():
    # Define an English translation dictionary
    en_dict = {
       ("*", "Select an image file"): "Select an image file",
       ("*", "Store the depth map values"): "Store the depth map values",
       ("*", "Store the surface object"): "Store the surface object",
       ("*", "Adjust the number of subdivisions for the surface"): "Adjust the number of subdivisions for the surface",
       ("*", "Adjust the strength of the displacement modifier for the surface"): "Adjust the strength of the displacement modifier for the surface",
       ("*", "Adjust the scale of the surface object"): "Adjust the scale of the surface object",
       ("*", "Choose the type of subdivision method for the surface"): "Choose the type of subdivision method for the surface",
       ("*", "Use simple subdivision algorithm"): "Use simple subdivision algorithm",
       ("*", "Use Catmull-Clark subdivision algorithm"): "Use Catmull-Clark subdivision algorithm",
       ("*", "Choose the type of displacement method for the surface"): "Choose the type of displacement method for the surface",
       ("*", "Use bump mapping to create an illusion of depth"): "Use bump mapping to create an illusion of depth",
       ("*", "Use true displacement to modify the geometry"): "Use true displacement to modify the geometry",
       ("*", "Create a 3D surface from a depth map image"): "Create a 3D surface from a depth map image"
    }

    # Register the English translation dictionary
    bpy.app.translations.register(__name__, en_dict)

    # TODO: Define and register other translation dictionaries for other languages

# Define a function to unregister translation dictionaries
def unregister_translations():
    # Unregister all translation dictionaries
    bpy.app.translations.unregister(__name__)

# Define a function to register the addon
def register():
    # Register the custom property group
    bpy.utils.register_class(DepthifyProperties)
    bpy.types.Scene.depthify_properties = bpy.props.PointerProperty(type=DepthifyProperties)

    # Register the depthify and operators modules
    depthify.register()
    operators.register()

    # Register the custom panel class
    bpy.utils.register_class(DepthifyPanel)

    # Register the translation dictionaries
    register_translations()

    # Log a message to the console
    logging.info("Depthify addon registered")

# Define a function to unregister the addon
def unregister():
    # Unregister the translation dictionaries
    unregister_translations()

    # Unregister the custom panel class
    bpy.utils.unregister_class(DepthifyPanel)

    # Unregister the depthify and operators modules
    operators.unregister()
    depthify.unregister()

    # Unregister the custom property group
    del bpy.types.Scene.depthify_properties
    bpy.utils.unregister_class(DepthifyProperties)

    # Log a message to the console
    logging.info("Depthify addon unregistered")

# Run the register function when the addon is enabled
if __name__ == "__main__":
    register()

       
