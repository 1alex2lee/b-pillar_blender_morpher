import bpy, bmesh, json, configparser
import random
import numpy as np


f = configparser.ConfigParser()
f.read("./config.ini")

original_STL = f['DEFAULT']["original_b_pillar_file"]
export_dir = f['DEFAULT']["export_directory"]
no_of_samples = int(f['DEFAULT']["number_of_samples"])
no_of_segments = int(f['DEFAULT']["number_of_segments_on_part"])
left_prob = float(f['DEFAULT']["probability_of_morphing_to_left"])
morph_dist = float(f['DEFAULT']["distance_to_morph"])
morphs_per_sample = int(f['DEFAULT']["number_of_morphs_per_sample"])


for sample_no in range(no_of_samples):

    context = bpy.context

    if bpy.context.object != None:
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
        bpy.data.objects['Bpillar'].select_set(True)  # select the object
        bpy.ops.object.delete()  # delete all selected objects

    bpy.ops.import_mesh.stl(filepath=original_STL,
        global_scale=1, axis_forward='Y', axis_up='Z')
        
    bpy.data.objects['Bpillar'].select_set(True)  # select the object
    bpy.ops.object.editmode_toggle()  # put the object in edit mode

    context = bpy.context

    bm = bmesh.from_edit_mesh(context.object.data)

    y_coords = []

    for v in bm.verts:
        v.select = False
        y_coords.append(v.co[1])
        
    y_coords = np.array(y_coords)

    y_max = np.max(y_coords)
    y_min = np.min(y_coords)
    y_range = y_max - y_min

    changable_verts = []

    for i in range(no_of_segments):
    #    if i == 4:
        if i != 0 and i != no_of_segments-1:
            
            region = []
            z_coords = []
                
            for v in bm.verts:
                y = v.co[1]
                
                if y_min + 0.2*i*y_range < y and y < y_min + 0.2*(i+1)*y_range:
                    region.append(v)
                    
            for v in region:
                z = v.co[2]
                z_coords.append(z)
            
            z_coords= np.array(z_coords)    
            z_max = np.max(z_coords)
            z_min = np.min(z_coords)
            z_range = z_max - z_min
            z_mean = np.mean(z_coords)
                    
            for v in region:
                z = v.co[2]
                
                if z_mean - 0.1*z_range < z and z < z_mean + 0.1*z_range:
                    changable_verts.append(v)
                        
    for v in region:
        v.select = True
            
    for i in range(morphs_per_sample):
        transform_dist = -morph_dist if random.random() <= left_prob else morph_dist

        transform = (transform_dist, 0, 0)  # left or right
        v = changable_verts[random.randint(0, len(changable_verts) - 1)]
        v.select = True
        bpy.ops.transform.translate(value=transform,    
                                constraint_axis=(False, False, False),
                                mirror=False, 
                                use_proportional_edit=True,
                                use_proportional_connected=True,
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=0.1)
        v.select = False
        
    bpy.ops.object.editmode_toggle()

    bpy.ops.export_mesh.stl(filepath=export_dir + f"morphed_{sample_no}.STL")