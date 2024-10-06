import numpy as np
import json
import os

def get_segname_super_box(segname_tcl_file):
    data=np.genfromtxt(segname_tcl_file,dtype=str,delimiter='{')
    
    super_box=[]
    central_box=[]
    for i in range(2,len(data)):
        if(i==len(data)-1):
            data[i]=data[i].replace('} }','')
        else:
            data[i]=data[i].replace('}','')
        x,y=data[i].split()
        super_box.append(x)
        central_box.append(y)
    #print(len(super_box))
    #print(central_box)
    return super_box,central_box


# Form a dictionary from a list of molecules
# Eg.: list of {AABC_resid1_OT1,AABC_resid1_OT2,...}
#-------------------------------------------------------
def dictionary_atomistic_detail(list_atomistic_segname):
    len_list=len(list_atomistic_segname)
    segname=list_atomistic_segname

    broken_mol_dict={}

    broken_segname=[]
    broken_resid=[]
    broken_atom=[]
    for i in range(len_list):
        seglist=segname[i][:4]
        resid=segname[i][10]
        atom=segname[i][12:]

        broken_segname.append(segname[i][:4])
        broken_resid.append(segname[i][10])
        broken_atom.append(segname[i][12:])
        if seglist in broken_mol_dict:
            if resid in broken_mol_dict[seglist]:
                broken_mol_dict[seglist][resid].append(atom)
            else:
                broken_mol_dict[seglist][resid]=[]
                broken_mol_dict[seglist][resid].append(atom)
        else:
            broken_mol_dict[seglist]={}
            broken_mol_dict[seglist][resid]=[]
            broken_mol_dict[seglist][resid].append(atom)
    #print(broken_mol_dict)
    return broken_mol_dict



#make tcl dictionary for molecules
def tcl_dictionary_molecule_atom_detail(tcl_filename,broken_mol_dict):
    with open(tcl_filename,"w+") as f:
        print("set seglist [dict create ",end="",file=f)
        k=0
        for key in broken_mol_dict:
            if k==0:
                print(key+" {",end="",file=f)
                k=1
            else:
                print(" "+key+" {",end="",file=f)
            i=0
            for resid in broken_mol_dict[key][0]:
                if i==0:
                    print(str(resid)+" {",end="",file=f)
                    i=1
                else:
                    print(" "+str(resid)+" {",end="",file=f)
                j=0
                #print(broken_mol_dict[key][0])
                for atom in broken_mol_dict[key][0][resid]:
                    if j==0:
                        print(atom,end="",file=f)
                        j=1
                    else:
                        print(" "+str(atom),end="",file=f)
                print("}",end="",file=f)
            print("}",end="",file=f)
        print("]",file=f)

def tcl_dictionary_molecule_atom_detail_central_box(tcl_filename,broken_mol_dict):
    with open(tcl_filename,"w+") as f:
        print("set seglist [dict create ",end="",file=f)
        k=0
        for key in broken_mol_dict:
            if k==0:
                print(key+" {",end="",file=f)
                k=1
            else:
                print(" "+key+" {",end="",file=f)
            i=0
            for resid in broken_mol_dict[key]:
                if i==0:
                    print(str(resid)+" {",end="",file=f)
                    i=1
                else:
                    print(" "+str(resid)+" {",end="",file=f)
                j=0
                #print(broken_mol_dict[key][0])
                for atom in broken_mol_dict[key][resid]:
                    if j==0:
                        print(atom,end="",file=f)
                        j=1
                    else:
                        print(" "+str(atom),end="",file=f)
                print("}",end="",file=f)
            print("}",end="",file=f)
        print("]",file=f)



def super_box_dictionary(frame_id,dictionary_central_box,super_box_map,cluster_id,cluster_brk_id):
    len_dict=len(dictionary_central_box)
    dict_rep={}
    super_box=[1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27]
    #super_box=[1]
    for i in super_box:
        dict_rep[i]={}
    for segname in super_box_map:
        for segname_dict in dictionary_central_box:
            if(segname==segname_dict):
                replica_segname=super_box_map[segname]
                list_atomistic=dictionary_central_box[segname_dict]
                for rep in replica_segname:
                    idx_rep=replica_segname.index(rep)
                    super_box_info=super_box[idx_rep]
                    dict_rep[super_box_info][rep]=[]

                    dict_rep[super_box_info][rep].append(list_atomistic)
    cluster_pbc_artifact='frame_'+str(frame_id)+'/super_box_dict/cluster_'+str(cluster_id)
    if(os.path.isdir(cluster_pbc_artifact)==False):
        os.mkdir(cluster_pbc_artifact)
    for i in super_box:
        tcl_filename=cluster_pbc_artifact+"/super_box_clr"+str(cluster_brk_id)+"_"+str(i)+".tcl"
        #print(i)
        dict_print=dict_rep[i]
        #print(dict_print)
        tcl_dictionary_molecule_atom_detail(tcl_filename,dict_print)
    #The central box dictionary:
    tcl_filename=cluster_pbc_artifact+"/super_box_clr"+str(cluster_brk_id)+"_"+str(14)+".tcl"
    dict_print=dictionary_central_box
    tcl_dictionary_molecule_atom_detail_central_box(tcl_filename,dict_print)



# More work to done ........
def tcl_cluster_broken_info(frame_num,cluster_id,num_periodic_artifact):

    #store current frame working
    with open('input_frame_info.tcl','w') as f:
        print("set frame_id ",frame_num,file=f)
    cluster_xyz='frame_'+str(frame_num)+'/super_box_xyz/cluster_'+str(cluster_id)
    if(os.path.isdir(cluster_xyz)==False):
        os.mkdir(cluster_xyz)
    cluster_pbc_artifact='frame_'+str(frame_num)+'/super_box_dict/cluster_'+str(cluster_id)
    #cluster_pbc_artifact='super_box_dict'
    if(os.path.isdir(cluster_pbc_artifact)==False):
        os.mkdir(cluster_pbc_artifact)
    tcl_filename='frame_'+str(frame_num)+"/super_box_dict/periodic_artifact_info.tcl"
    with open(tcl_filename,"w") as f:
        print("set num_broken_cls ",num_periodic_artifact,file=f)
        print("set cluster_id ",cluster_id,file=f)


def center_of_mass(list_coord,list_mass):

    len_list=len(list_mass)
    mass = 0.0
    com = [0.0,0.0,0.0]
    for particle_id in range(len_list):
        m=list_mass[particle_id]
        mass = mass + m
        coord = list_coord[particle_id]
        p = m*coord
        com = com + p 
    
    com = (1.0/mass)*com
    return com

def get_mol_mass(atom):
    molecular_mass={"C":12.01099967956543,"O":15.99899959564209,"H":1.0080000162124634,"N":14.006999969482422}
    #print(atom)
    for atom_id in molecular_mass:
        if atom_id==atom:
            mass=molecular_mass[atom_id]
    return mass


def change_cluster_dict_content(frame_id,cluster_dictionary,idx,changed_item,changed_segname,superbox_replica_id):

    f=open("changed_check.dat",'a+')
    print(idx,"-------",file=f)
    print(len(cluster_dictionary["positions"][idx]))
    print('=====\n',len(changed_item))
    len_list=len(changed_item)

    segname_tcl_file='frame_'+str(frame_id)+'/super_box_seg/segname_map_'+str(superbox_replica_id)+'.tcl'
    super_box,central_box=get_segname_super_box(segname_tcl_file)
    for i in range(len_list):
        s_segname=changed_segname[i][:4]
        s_idx=super_box.index(s_segname)
        c_seg=central_box[s_idx]
        original_segname=changed_segname[i].replace(s_segname,c_seg)
        print("change:",cluster_dictionary["cluster"][idx][i],changed_segname[i],c_seg,original_segname,file=f)
        cluster_dictionary["positions"][idx][i]=changed_item[i]
        cluster_dictionary["cluster"][idx][i]=original_segname
    
    f.close()


def setup_superbox_create(frame_id,box_length,base_pdb_file,pdb_base_path):
    filename='superbox_input_param.tcl'
    #pdb_file='frame_'+str(frame_id)+'/xyz_files/'+base_pdb_file+str(frame_id)+'.pdb'
    pdb_file=pdb_base_path+"/"+base_pdb_file+str(frame_id)+'.pdb'
    save_path_pdb='frame_'+str(frame_id)+'/super_box_pdb_same_seg'
    with open(filename,'w+') as f:
        print("set frame_id ",frame_id,file=f)
        print("set pdb_file ",pdb_file,file=f)
        print("set input_pdb_file ",pdb_file,file=f)
        print("set box_length_x ",box_length,file=f)
        print("set box_length_y ",box_length,file=f)
        print("set box_length_z ",box_length,file=f)
        print("set save_path_pdb ",save_path_pdb,file=f)
    
    dir_sb_formation='frame_'+str(frame_id)+'/super_box_pdb_same_seg'
    dir_sb_pdb='frame_'+str(frame_id)+'/super_box_pdb'
    dir_sb_seg='frame_'+str(frame_id)+'/super_box_seg'
    #dir_sb_dict='frame_'+str(frame_id)+'/super_box_dict'
    dir_sb_xyz='frame_'+str(frame_id)+'/super_box_xyz'

    if(os.path.isdir(dir_sb_formation)==False):
        os.mkdir(dir_sb_formation)
    if(os.path.isdir(dir_sb_pdb)==False):
        os.mkdir(dir_sb_pdb)
    #if(os.path.isdir(dir_sb_dict)==False):
    #    os.mkdir(dir_sb_dict)
    if(os.path.isdir(dir_sb_xyz)==False):
        os.mkdir(dir_sb_xyz)
    if(os.path.isdir(dir_sb_seg)==False):
        os.mkdir(dir_sb_seg)
        


        
def extract_from_tcl(tcl_filename):
    data=np.genfromtxt(tcl_filename,dtype=str)

    segname=data[2:]
    segname[0]=segname[0].replace('{','')
    segname[-1]=segname[-1].replace('}','')
    return segname

def extract_uniq_seg_diction(len_list,seg_list):
    segname = []
    for i in range(len_list):
        seg = seg_list[i]["name"][:4]
        segname.append(seg)
    uniq_segname=np.unique(segname)
    return uniq_segname

def box_length_list_function(filename):
    data=np.genfromtxt(filename)

    return data
    

def det_num_cluster(file_name):
    num_cluster_list = np.loadtxt(file_name)
    return num_cluster_list



def pbc_corrected_max_match_v2(frame_id,cluster_id,clusters_dict):
    non_pbc_cluster='frame_'+str(frame_id)+'/cluster_'+str(cluster_id)+'.tcl'
    segname1=extract_from_tcl(non_pbc_cluster)
    set_A = set(segname1)
    len_A = len(segname1)

    num_freud_cluster = clusters_dict["num_clusters"]
    #j_start=int(27*cluster_id)
    #j_end=int(27*(cluster_id+1))

    f=open("frame_"+str(frame_id)+"/PBC_corrected_freud/selection_info.txt","a+")
    
    for i in range(0,num_freud_cluster):
        pbc_cluster = clusters_dict["clusters"][i]["particle_info"]
        len_pbc_cluster = clusters_dict["clusters"][i]["size"]
        segname2=extract_uniq_seg_diction(len_pbc_cluster,pbc_cluster)
        set_B = set(segname2)
        len_B = len(segname2)
        check_intersection=set_A.intersection(set_B)
        len_AB = len(check_intersection)

        if(i==0):
            max_match_id=i
            max_len_match=len_AB
            rem_list=set_B-check_intersection
        elif(len_AB>max_len_match):
            max_match_id=i
            max_len_match=len_AB
            rem_list=set_B-check_intersection


        print("SB_cluster:",i," len non pbc cluster",len_A," len pbc cluster",len_B," len common cluster",len_AB,file=f)
        #print(i,":::::::::::::::::::::::: Done")

    original_seg_rem_list=[]

    fname_master_map="frame_"+str(frame_id)+"/super_box_seg/segname_map_master.json"
    f_master_map=open(fname_master_map)
    master_map=json.load(f_master_map)
    f_master_map.close()
    original_segname={}
    for item_rem in rem_list:
        #print(item_rem,":",master_map[item_rem])
        original_segname[item_rem]=master_map[item_rem]

    print('Final selection:',max_match_id,max_len_match,rem_list,file=f)

    return max_match_id,max_len_match,rem_list,original_segname




def join_xyz_clusters(frame_id,num_cluster):
    total_len=0
    f=open("frame_"+str(frame_id)+"/PBC_corrected_freud/join_all_cluster.xyz","w")
    print("                 this Generated",file=f)
    for i in range(num_cluster):
        filename='frame_'+str(frame_id)+'/PBC_corrected_freud/cluster_'+str(i)+".xyz"
        data=np.genfromtxt(filename,dtype=str,skip_header=2)
        data_f=np.genfromtxt(filename,skip_header=2)
        len_atom=len(data[:,0])
        total_len=total_len+len_atom

        for idx in range(len_atom):
            print(data[idx,0],data_f[idx,1],data_f[idx,2],data_f[idx,3],file=f)
    f.seek(0)
    print(total_len,file=f)
    f.close()



