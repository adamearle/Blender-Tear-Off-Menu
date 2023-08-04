bl_info = {
    "name": "AniMix Floating Windows",
    "author": "Adam Earle",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "ui",
    "description": "boilerplate code for creating an empty window blender",
    "category": "Development",
}



'''
Boiler plate starer code that enables the addon developer to put on buttons in a floating windpw
'''



import bpy
import ctypes


# Custom operator to open the AniMix editor in a new window
class AniMixNodeTree(bpy.types.NodeTree):
    bl_idname = 'AniMixNodeTreeType'
    bl_label = 'AniMix Node Tree'
    bl_icon = 'EXPERIMENTAL'


# Custom operator to open the AniMix editor in a new window
class ANIMIX_OT_open_editor(bpy.types.Operator):
    bl_idname = "animix.open_editor"
    bl_label = "Open AniMix Editor"

    # Set window size height widthe and postion on screen
    def set_window_size_and_position(self, window):
        if ctypes.windll:
            hWnd = ctypes.windll.user32.GetForegroundWindow()
            user32 = ctypes.windll.user32
            screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            windowSize = (100, 400)
            x = (screenSize[0] - windowSize[0]) // 2
            y = (screenSize[1] - windowSize[1]) // 2
            ctypes.windll.user32.SetWindowPos(hWnd, 0, x, y, windowSize[0], windowSize[1], 0)
        else:
            print('Window resizing is currently supported only on Windows.')

    def execute(self, context):
        # Duplicate the current 3D Viewport area into a new window       
        result = bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        if result != {'FINISHED'}:
            self.report({'ERROR'}, "Failed to create a new window.")
            return {'CANCELLED'}

        # Get the new window and area
        new_window = bpy.context.window_manager.windows[-1]
        new_area = new_window.screen.areas[0]
        new_area.type = 'NODE_EDITOR'
        
        # Create a new AniMix Node Tree
        node_tree = bpy.data.node_groups.new('AniMix Node Tree', 'AniMixNodeTreeType')
        
        # Set the new node tree as the active node tree in the Node Editor
        space = new_area.spaces.active
        space.tree_type = 'AniMixNodeTreeType'
        space.node_tree = node_tree

        # Set the new window's size and position
        self.set_window_size_and_position(new_window)

        return {'FINISHED'}


# Create button
def draw_animix_button(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator("animix.open_editor", emboss=False, icon='EXPERIMENTAL', text="")




# Register function
def register():
    bpy.utils.register_class(AniMixNodeTree)
    bpy.utils.register_class(ANIMIX_OT_open_editor)
    bpy.types.VIEW3D_HT_header.append(draw_animix_button)
    
# Unregister function
def unregister():
    bpy.types.VIEW3D_HT_header.remove(draw_animix_button)
    bpy.utils.unregister_class(ANIMIX_OT_open_editor)
    bpy.utils.unregister_class(AniMixNodeTree)

# Main execution
if __name__ == "__main__":
    register()
