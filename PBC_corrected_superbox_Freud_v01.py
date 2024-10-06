'''
-------------------------------------
| THIS IS THE MAIN CODE NEED TO RUN  |
-------------------------------------
Execution Instruction:
----------------------
python3 PBC_corrected_superbox_Freud.py

This code do PBC correction of each clusters for every frames.

Workflow :
-----------
1) First the super box is created for the particular frame. It requires to  
    run a series of tcl scripts, which are launched from a shell script :
    
    "script_superbox_formation_frame_v01.sh" .
    -----------------------------------------

    Final Output file : merge_superbox.txt,it is a txt file very similar to xyz file

2) Then FREUD clustering is applied on the superbox : merge_superbox.txt with atomic 
    cutoff distance = 3. As we apply Freud clustering on superbox so the number of 
    clusters are 27 times the actual number of clusters.

3) Among the clusters formed from Freud has maximum matching with the actual clusters 
    segname of the central box are considered and stores clusters xyz files in 
    "PBC_corrected_freud" of the particular frame.

4) And at last merge all the clusters in one xyz file namely "join_all_cluster.xyz" and 
    stored in the respective frame "PBC_corrected_freud" directory.
'''

import numpy as np
import support_code_v01 as sc
import sys,os
import subprocess
import shlex
import json
import FREUDcluster_frame_v01 as frd



# Provide the starting and ending frame numbers on which the PBC correction applied
start_frame=100
end_frame=102

# Some input informations for each frame
num_cluster_list = sc.det_num_cluster("number_of_cluster_per_frame.txt")

box_length_list = sc.box_length_list_function("box_length.txt")

## pdb file base of that frame
base_pdb_file = 'fff-500-mol-175A-box_frame_'

for frame_num in range(start_frame,end_frame):
    num_cluster_per_frame = int(num_cluster_list[frame_num])
    box_len = box_length_list[frame_num]

    # Setup for  superbox 
    # Set the base path for the original pdb file
    central_pdb_base_path = 'frame_'+str(frame_num)+'/xyz_files'
    sc.setup_superbox_create(frame_num,box_len,base_pdb_file,central_pdb_base_path)

    # Superbox formation [step 1]
    subprocess.call(shlex.split('./script_superbox_formation_frame_v01.sh'))

    # Freud clustering on super box
    input_xyz_like_txt_file='frame_'+str(frame_num)+'/super_box_pdb/merge_superbox.txt'

    superbox_length=box_len*3.0
    cutoff_for_clustering=3.0
    freud_cor_save_path = 'frame_'+str(frame_num)+'/PBC_corrected_freud'
    if(os.path.isdir(freud_cor_save_path)==False):
        os.mkdir(freud_cor_save_path)
    frd.main_Freud(frame_num,input_xyz_like_txt_file,superbox_length,cutoff_for_clustering,freud_cor_save_path,num_cluster_per_frame)
    sc.join_xyz_clusters(frame_num,num_cluster_per_frame)







