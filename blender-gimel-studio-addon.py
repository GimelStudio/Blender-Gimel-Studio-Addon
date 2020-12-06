## ----------------------------------------------------------------------------
## Gimel Studio Blender Bridge Addon Copyright 2020 Noah Rahm
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## ----------------------------------------------------------------------------


import os
import tempfile
from subprocess import Popen, PIPE

import bpy


bl_info = {
    "name": "Gimel Studio Bridge",
    "author": "Noah Rahm, Correct Syntax",
    "category": "Render",
    'description': 'Allows for editing renders from Blender in Gimel Studio',
    'license': 'Apache 2.0',
    'version': (0, 2),
    'blender': (2, 83, 0),
    'location': 'Compositing > Gimel Studio',
    'warning': 'Still in development! WIP!',
}


class GimelStudioOperation(bpy.types.Operator):
    """Edit the current rendered image in the Gimel Studio program"""
    bl_idname = "render.gimel_studio_editing"
    bl_label = "Launch Gimel Studio"


    def execute(self, context):
        pref_fp = context.preferences.addons[__name__].preferences.filepath
        exe_path = bpy.path.abspath(pref_fp)
        project_path = bpy.data.filepath
        directory = os.path.dirname(project_path)

        # Save the temp image
        if bpy.data.is_saved:
            dirname = os.path.join(tempfile.gettempdir(),
                                   'BlenderGimelStudioAddonTemp')
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            else:
                pass

            output_path = os.path.join(dirname,'temp.png')
            image = bpy.data.images["Render Result"].save_render(output_path)

        else:
            self.report({'ERROR'}, 'File not saved!')
            return {'CANCELLED'}

        # Pass the path to the temp image as an arg to the
        # Gimel Studio executable on launch in another process.
        process = Popen([exe_path, '--blender', output_path],
                        stdin=PIPE, stdout=PIPE)

        return {'FINISHED'}


class GimelStudioPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    filepath: bpy.props.StringProperty(name="Gimel Studio Executable",
                                       subtype='FILE_PATH')

    def draw(self, context):
        layout = self.layout
        layout.label(text="Please specify the path to the Gimel Studio executable (e.g: 'GimelStudio.exe')")
        layout.prop(self, "filepath")


class GimelStudioPanel(bpy.types.Panel):
    """Creates a Panel in the Node Compositing window"""
    bl_label = "Gimel Studio"
    bl_idname = "OBJECT_PT_gimel_studio_pnl"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "View"
    bl_category = "Gimel Studio"

    @classmethod
    def poll(cls, context):
        snode = context.space_data
        return snode.tree_type == 'CompositorNodeTree'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Edit the current rendered image in Gimel Studio",
                  icon='IMAGE_DATA')

        row = layout.row()
        row.operator(GimelStudioOperation.bl_idname)


classes = (
    GimelStudioPanel,
    GimelStudioPrefs,
    GimelStudioOperation
)


def register():
    # add operator
    from bpy.utils import register_class
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    from bpy.utils import unregister_class

    # remove operator and preferences
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
