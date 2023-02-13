# Automatic B-pillar morphing in Blender
## Alex Lee's Master's Project 2022-2023
### Dyson School of Design Engineering, Imperial College London

This code morphs a B-pillar laterally to alter its shape. It takes the B-pillar as an STL file and exports one or multiple STL files.

## Configuration
Modify config.ini to change morphing settings:
- original_b_pillar_file = the STL file which contains the original STL of the B-pillar
- export_directory = folder in which morphed B-pillars will be saved as an STL file
- number_of_samples = the number of morphed B-pillars STL to generate for a single original B-pillar file, default is 10
- number_of_segments_on_part = the number of segments to split the B-pilalr into height-wise, with the top and bottom segments being held constant, meaning they will not be morphed or moved, default is 5
- probability_of_morphing_to_left = the probability of a single morph being to the left direction (negative y-axis), and is also the 1 - the probability of a single morph being to the right direction (positive y-axis), default is 0.5
- distance_to_morph = distance in m which each morph takes, maximum and default is 0.01
- number_of _morphs_per_sample = how many morphs to apply to the original B-pillar before exporting as an STL, default is 1

## How to Use
1. Change configurations to as desired in config.ini
2. Run blender_morph.bat