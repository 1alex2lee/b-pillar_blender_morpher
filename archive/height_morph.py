import bpy
import bmesh
from random import randint, choice
import numpy as np

if bpy.context.object != None:
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
    bpy.data.objects['Bpillar'].select_set(True)  # select the object
    bpy.ops.object.delete()  # delete all selected objects

bpy.ops.import_mesh.stl(filepath="./Bpillar.STL",
    global_scale=1, axis_forward='Y', axis_up='Z')
    
bpy.data.objects['Bpillar'].select_set(True)  # select the object
bpy.ops.object.editmode_toggle()  # put the object in edit mode

context = bpy.context

bm = bmesh.from_edit_mesh(context.object.data)

x_coords = []
y_coords = []
z_coords = []

for v in bm.verts:
    v.select = False          # deselect all
    x_coords.append(v.co[0])  # get y coordinates of every vertex
    y_coords.append(v.co[1])  # get y coordinates of every vertex
    z_coords.append(v.co[2])  # get y coordinates of every vertex

x_coords = np.array(x_coords)    
y_coords = np.array(y_coords)
z_coords = np.array(z_coords)

x_max = np.max(x_coords)
x_min = np.min(x_coords)
x_range = x_max - x_min

y_max = np.max(y_coords)
y_min = np.min(y_coords)
y_range = y_max - y_min

z_max = np.max(z_coords)
z_min = np.min(z_coords)
z_range = z_max - z_min

x_region = [0.4,0.5]
y_region = [0.4,0.5]
z_region = [0.4,0.5]

scale_factor = 0.4

changable_verts = []  # array with all vertices allowed to be changed

for v in bm.verts:
    
    x = v.co[0]
    y = v.co[1]
    z = v.co[2]
    
    if x_min <= x and x <= x_max:
        if y_min + y_region[0]*y_range <= y and y <= y_min + y_region[1]*y_range:
            if z_min + z_region[0]*z_range <= z and z <= z_min + z_region[1]*z_range:
                changable_verts.append(v)  # make all vertices above lower bound changable
                    
for v in changable_verts:
    v.select = True
    transform = (scale_factor*x_range/100, 0, 0)
    bpy.ops.transform.translate(value=transform,    
                            constraint_axis=(False, False, False),
                            mirror=False,
#                            use_proportional_edit=False)
                            use_proportional_edit=True,
                            use_proportional_connected=True,
                            proportional_edit_falloff='SMOOTH',
                            proportional_size=0.1)
                            
#    v.select = False