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
import shutil
import tempfile
from subprocess import Popen, PIPE

import bpy


bl_info = {
    "name": "Gimel Studio Bridge",
    "author": "Noah Rahm, Correct Syntax",
    "category": "Render",
    'description': 'Allows for editing renders from Blender in Gimel Studio',
    'license': 'Apache 2.0',
    'version': (0, 1),
    'blender': (2, 83, 0),
    'location': 'Compositing > Gimel Studio',
    'warning': 'Still in development!',
}


class GimelStudioOperation(bpy.types.Operator):
    """Edit the current rendered image in the Gimel Studio program"""
    bl_idname = "render.gimel_studio_editing"
    bl_label = "Launch Gimel Studio"
        
        
    def execute(self, context):
        exe = bpy.path.abspath(context.preferences.addons[__name__].preferences.filepath)
        print(exe)
        projpath = bpy.data.filepath
        directory = os.path.dirname(projpath)
        
        
        # Save the temp img
        if bpy.data.is_saved:
            dirname = os.path.join(tempfile.gettempdir(),'blendergimelstudioaddon_temp')
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            else:
                pass
                
            output = os.path.join(dirname,'img.png')
            #bpy.context.scene.render.filepath = output
            #bpy.ops.render.render(write_still = True) 
            
        #import os
        #with open(os.path.splitext() + ".txt", 'w') as fs:
        #fs.write("%s %d x %d\n" % (image.filepath, image.size[0], image.size[1]))          
            
            # write images into a file next to the blend
            #with open(os.path.splitext(bpy.data.filepath)[0] + ".txt", 'w') as fs:
             #   for image in bpy.data.images:
              #      fs.write("%s %d x %d\n" % (image.filepath, image.size[0], image.size[1]))      
            image = bpy.data.images["Render Result"].save_render(output)         
            
            
        
        else:
            self.report({'ERROR'}, 'File not saved!')
            return {'CANCELLED'}
        
        process = Popen([exe], stdin=PIPE, stdout=PIPE)
        

        return {'FINISHED'}


class GimelStudioPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    filepath: bpy.props.StringProperty(
        name="Gimel Studio Executable",
        subtype='FILE_PATH',
    )

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

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Edit the current rendered image in Gimel Studio", icon='IMAGE_DATA')

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

    try:
        pass
        #os.remove(os.path.join(tempfile.gettempdir(), ''))
    except:
        pass


def unregister():
    from bpy.utils import unregister_class

    # remove operator and preferences
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
