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

bl_info = {
    "name": "Unreal Engine Skeleton Rigging Utilities",
    "author": "Paul Greenberg @greenpau",
    "version": (1, 0, 5),
    "blender": (5, 0, 1),
    "location": "View3D > Add > Armature > Skeletons",
    "description": "Adds Unreal Engine skeletons to the Add menu.",
    "warning": "",
    "doc_url": "https://github.com/greenpau/blender-unreal-rig-utils",
    "category": "Rigging",
}

import bpy
from . import operators
from . import ui

modules = [operators, ui]


def register():
    """Register classes and menu appends from sub-modules"""
    for module in modules:
        module.register()


def unregister():
    """Unregister classes and menu appends in reverse order to prevent dependencies"""
    for module in reversed(modules):
        module.unregister()


if __name__ == "__main__":
    register()
