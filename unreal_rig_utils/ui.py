#
# Copyright (C) 2026 Paul Greenberg greenpau@outlook.com
#
# Licensed under the GPLv3 License.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import bpy


class MYRIG_MT_SkeletonSubMenu(bpy.types.Menu):
    """The 'Skeletons' sub-menu that appears in the Shift+A menu"""
    bl_label = "Skeletons"
    bl_idname = "MYRIG_MT_skeleton_submenu"

    def draw(self, context):
        layout = self.layout

        # Link to the operators from operators.py
        layout.operator("myrig.create_ue5_manny", text="UE5 Manny", icon='USER')
        layout.operator("myrig.create_ue5_quinn", text="UE5 Quinn", icon='USER')


# --- SIDEBAR PANEL (N-PANEL) ---


class MYRIG_PT_MainPanel(bpy.types.Panel):
    """Creates a custom tab in the Sidebar for extra rigging tools"""
    bl_label = "UE5 Rigging Tools"
    bl_idname = "MYRIG_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MyRig'    # The name of the tab

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Quick Spawn", icon='ARMATURE_DATA')
        col = box.column(align=True)
        col.operator("myrig.create_ue5_manny", icon='ADD')
        col.operator("myrig.create_ue5_quinn", icon='ADD')


# --- MENU INJECTION ---


def draw_menu_append(self, context):
    """Adds our 'Skeletons' sub-menu to the standard Add > Armature menu"""
    layout = self.layout
    layout.separator()
    # This refers to the bl_idname of the Menu class above
    layout.menu("MYRIG_MT_skeleton_submenu", icon='GROUP_BONE')


# --- REGISTRATION ---

classes = (
    MYRIG_MT_SkeletonSubMenu,
    MYRIG_PT_MainPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # This appends our menu to the standard Blender 'Add Armature' menu
    bpy.types.VIEW3D_MT_armature_add.append(draw_menu_append)


def unregister():
    # Remove the menu injection
    bpy.types.VIEW3D_MT_armature_add.remove(draw_menu_append)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
