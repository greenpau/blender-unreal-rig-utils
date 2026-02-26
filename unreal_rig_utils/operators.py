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

# --- SKELETON DATA ---
# Format: "Bone_Name": {"parent": "Parent_Name", "head": (x, y, z), "tail": (x, y, z)}
# Coordinates are in Meters.

MANNY_DATA = {
    "root": {
        "parent": None,
        "head": (0, 0, 0),
        "tail": (0, 0, 0.1)
    },
    "pelvis": {
        "parent": "root",
        "head": (0, 0, 0.95),
        "tail": (0, 0.05, 1.05)
    },
    "spine_01": {
        "parent": "pelvis",
        "head": (0, 0.05, 1.05),
        "tail": (0, 0.02, 1.15)
    },
    "spine_02": {
        "parent": "spine_01",
        "head": (0, 0.02, 1.15),
        "tail": (0, 0.01, 1.30)
    },
    "neck_01": {
        "parent": "spine_02",
        "head": (0, 0.01, 1.55),
        "tail": (0, 0.02, 1.65)
    },
    "head": {
        "parent": "neck_01",
        "head": (0, 0.02, 1.65),
        "tail": (0, 0.05, 1.85)
    },
    "thigh_l": {
        "parent": "pelvis",
        "head": (0.1, 0, 0.9),
        "tail": (0.12, -0.02, 0.5)
    },
    "calf_l": {
        "parent": "thigh_l",
        "head": (0.12, -0.02, 0.5),
        "tail": (0.12, 0.02, 0.1)
    },
    "foot_l": {
        "parent": "calf_l",
        "head": (0.12, 0.02, 0.1),
        "tail": (0.12, 0.15, 0)
    },
}

QUINN_DATA = {
    "root": {
        "parent": None,
        "head": (0, 0, 0),
        "tail": (0, 0, 0.1)
    },
    "pelvis": {
        "parent": "root",
        "head": (0, 0, 0.88),
        "tail": (0, 0.04, 0.98)
    },
    "spine_01": {
        "parent": "pelvis",
        "head": (0, 0.04, 0.98),
        "tail": (0, 0.02, 1.08)
    },
    "spine_02": {
        "parent": "spine_01",
        "head": (0, 0.02, 1.08),
        "tail": (0, 0.01, 1.25)
    },
    "neck_01": {
        "parent": "spine_02",
        "head": (0, 0.01, 1.48),
        "tail": (0, 0.02, 1.58)
    },
    "head": {
        "parent": "neck_01",
        "head": (0, 0.02, 1.58),
        "tail": (0, 0.05, 1.75)
    },
    "thigh_l": {
        "parent": "pelvis",
        "head": (0.09, 0, 0.85),
        "tail": (0.1, -0.02, 0.45)
    },
    "calf_l": {
        "parent": "thigh_l",
        "head": (0.1, -0.02, 0.45),
        "tail": (0.1, 0.02, 0.08)
    },
    "foot_l": {
        "parent": "calf_l",
        "head": (0.1, 0.02, 0.08),
        "tail": (0.1, 0.12, 0)
    },
}

# --- GENERATION LOGIC ---


def create_unreal_engine_skeleton(context, name, bone_data):
    """Core logic to build the rig from a dictionary"""

    # Create Armature and Object
    arm_data = bpy.data.armatures.new(f"{name}_Data")
    rig_obj = bpy.data.objects.new(name, arm_data)
    context.collection.objects.link(rig_obj)

    # Set as active and enter Edit Mode
    context.view_layer.objects.active = rig_obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Create Bones and set positions
    for b_name, props in bone_data.items():
        bone = arm_data.edit_bones.new(b_name)
        bone.head = props["head"]
        bone.tail = props["tail"]

    # Set Parenting (Must be done after all bones are created)
    for b_name, props in bone_data.items():
        if props["parent"]:
            bone = arm_data.edit_bones[b_name]
            parent = arm_data.edit_bones.get(props["parent"])
            if parent:
                bone.parent = parent

    # Create Bone Collections (Blender 5.0.1 Style)
    # We'll create a 'Deform' collection and add all bones to it
    deform_col = arm_data.collections.new("Deform")
    for bone in arm_data.edit_bones:
        deform_col.assign(bone)

    # Exit Edit Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return rig_obj


# --- OPERATORS ---


class MYRIG_OT_CreateManny(bpy.types.Operator):
    """Create the UE5 Manny skeleton"""
    bl_idname = "myrig.create_ue5_manny"
    bl_label = "UE5 Manny"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_unreal_engine_skeleton(context, "UE5_Manny", MANNY_DATA)
        self.report({'INFO'}, "Manny Skeleton Created")
        return {'FINISHED'}


class MYRIG_OT_CreateQuinn(bpy.types.Operator):
    """Create the UE5 Quinn skeleton"""
    bl_idname = "myrig.create_ue5_quinn"
    bl_label = "UE5 Quinn"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_unreal_engine_skeleton(context, "UE5_Quinn", QUINN_DATA)
        self.report({'INFO'}, "Quinn Skeleton Created")
        return {'FINISHED'}


# --- REGISTRATION ---

classes = (
    MYRIG_OT_CreateManny,
    MYRIG_OT_CreateQuinn,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
