from fileinput import filename
import numpy as np
import freud
import readXYZ_v01 as readXYZ
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import support_code_v01 as sc

'''
CLustering code using Freud's clustering module
Input data is expected to be an XYZ file with one
frame. All the tasks are done from within one Python function

THESE FUNCTIONS ARE MEANT TO BE CALLED FROM ANALYSIS CODES


Infromation about a single particle is stored in a dictionary of
the following form
{"index":0_based_particle_index_in_xyz_file, "name":particle_name_in_xyz_file}
Data for a single cluster is packaged into a dictionary
{"size":cluster_size, "particle_info":list_of_dictionaries_for_particle_info,
 "com":center_of_cluster}

Entire clustering information is stored in a single dictionary, which is returned
by the function. The dictionary looks like following
{"num_points":number_of_data_points,
 "box_length":cubic_box_length,
 "cutoff":cutoff_distance_used_for_clustering,
 "num_clusters":number_of_clusters,
 "clusters":list_of_dictionaries_of_clusters_sorted_in_reverse_by_cluster_size
 }

'''
def clusterXYZframe(input_xyz_file, cubic_box_length, cutoff_for_clustering):
    xyz_data = readXYZ.Read_XYZ_txt(input_xyz_file)

    # Freud box
    box = freud.box.Box.cube(L=cubic_box_length)
    system = freud.AABBQuery(box,xyz_data[ "coordinates"] )
    # Instantiate a Cluster object
    cl = freud.cluster.Cluster()
    # Compute the clusters
    cl.compute(system, neighbors={'r_max':cutoff_for_clustering })
    
    # Get the number of clusters
    num_clusters = cl.num_clusters
    # Array of cluster indices of each particle
    cluster_indices = cl.cluster_idx
    # Instantiate a ClusterProperties object
    cl_prop = freud.cluster.ClusterProperties()
    # Calculate properties of the cluster
    cl_prop.compute(system, cluster_indices)
    cluster_sizes = cl_prop.sizes
    
    # Cluster dictionary
    clusters_dict = {}
    clusters_dict["num_points"] = xyz_data["num_particles"]
    clusters_dict["box_length"] = cubic_box_length
    clusters_dict["cutoff"] = cutoff_for_clustering
    clusters_dict["num_clusters"] = num_clusters
    # Empty dictionaries for storing cluster infroamtion
    clusters_dict["clusters"] = []
   
    for i in range(num_clusters):
        clusters_dict["clusters"].append({})
    for i in range(num_clusters):
        clusters_dict["clusters"][i]["size"] = cluster_sizes[i]
        # Initialize the particle_info filed with an empty list
        clusters_dict["clusters"][i]["particle_info"] = []


    # Loop over all particle indices and put them in the respective clusters
    for j in range(clusters_dict["num_points"]):
        # Create a dictionary for the j'th particle
        temp_dict = {}
        temp_dict["index"] = j
        temp_dict["name"] = xyz_data["names"][j]
        temp_dict["coordinates"] = xyz_data["coordinates"][j]
        # Append the particle dictionary to the proper list of the cluster
        # j'th particle belongs to
        clusters_dict["clusters"][cluster_indices[j]]["particle_info"].append(temp_dict)
    # Sort the list of clusters in descending order of sizes in the master data strucutre
    sorted_list_of_clusters = sorted(clusters_dict["clusters"], key=lambda k: k["size"], reverse=True)
    # Repalce with the sorted list
    clusters_dict["clusters"] = sorted_list_of_clusters
    #print("cluster id :", i , "cluster size :",cluster_sizes[i] )
    #cluster_id.append(i)
    #cluster_population.append(cluster_sizes[i])

    # Return
    return clusters_dict

'''
Write a Tcl file with the segment names of a particular cluster. This Tcl file
can be sourced from a VMD Tcl script
This function should be called with the cluster data generated by the previous function
as an argument
'''
def writeTclFileSegname(clusters_dict, cluster_index, tcl_filename):
    f = open(tcl_filename, "w")
    #print("set segname_list_"+str(cluster_index)+" {", file=f, end='')
    print("set segname_list"+" {", file=f, end='')
    for i in range(clusters_dict["clusters"][cluster_index]["size"]):
        # Loop over all the points in the cluster and access the
        # dictionaries
        segname = clusters_dict["clusters"][cluster_index]["particle_info"][i]["name"][:4]
        if i == 0:
            print(segname, file=f, end='')
        else:
            print("", segname, file=f, end='')

    print("}", file=f, end='')
    f.close()

def writeXYZFile(clusters_dict, cluster_index, xyz_filename):
    f = open(xyz_filename, "w")
    print(clusters_dict["clusters"][cluster_index]["size"],file=f)
    print("Generated from code : FREUDcluster-version_v01",file=f)
    for i in range(clusters_dict["clusters"][cluster_index]["size"]):
        coordinates = clusters_dict["clusters"][cluster_index]["particle_info"][i]["coordinates"]
        segname = clusters_dict["clusters"][cluster_index]["particle_info"][i]["name"]
        print(segname,coordinates[0],coordinates[1],coordinates[2],file=f)
    f.close()

def change_actual_segname(clusters_dict,cluster_index,seg_map):

    keys = seg_map.keys()
    for i in range(clusters_dict["clusters"][cluster_index]["size"]):
        segname = clusters_dict["clusters"][cluster_index]["particle_info"][i]["name"]
        seg = segname[:4]
        if(seg in keys):
            org_seg = seg_map[seg]
            clusters_dict["clusters"][cluster_index]["particle_info"][i]["name"] = clusters_dict["clusters"][cluster_index]["particle_info"][i]["name"].replace(seg,org_seg) 
    return clusters_dict

def main_Freud(frame_id,input_xyz_like_txt_file,box_length,cutoff_for_clustering,save_path,num_non_pbc_cluster):
    input_xyz_file  = input_xyz_like_txt_file
    cubic_box_length = box_length
    #cutoff_for_clustering = 3.0
    cluster_id = []
    cluster_population = []
 
    # Call the function to get all inroamtion about the clustering
    cluster_data = clusterXYZframe(input_xyz_file, cubic_box_length, cutoff_for_clustering)
    # Get infromation from the cluster data structure which is a dictionary
    print("Number of clusters:", cluster_data["num_clusters"])
    #print("Cluster sizes")
    '''
    for i in range(cluster_data["num_clusters"]):
    #    print(cluster_data["clusters"][i]["size"])
        print("cluster id :", i , "cluster size :",cluster_data["clusters"][i]["size"] )
        cluster_id.append(i)
        cluster_population.append(cluster_data["clusters"][i]["size"] )

    plt.plot(cluster_id, cluster_population)
    plt.title('Frequency distribution for 200A beta-sheet system(co 8.5) ', fontsize=18)
    plt.xlabel('Cluster ID', fontsize=16)
    plt.ylabel('points in clusters', fontsize=16)
    plt.grid(color='black', linestyle='-', linewidth=0.1)
    #plt.show()
    '''

    # print("Dictionary for the largest cluster:", cluster_data["clusters"][0])


    #num_non_pbc_cluster=74
    #if(os.path.isfile(cluster_file)==True):

    for c_id in range(num_non_pbc_cluster):
        max_match_id,max_len_match,rem_list,seg_map = sc.pbc_corrected_max_match_v2(frame_id,c_id,cluster_data)
        xyz_filename=save_path+'/cluster_'+str(c_id)+'.xyz'
        if(len(rem_list)!=0):
            cluster_data=change_actual_segname(cluster_data,max_match_id,seg_map)
        writeXYZFile(cluster_data, max_match_id, xyz_filename)
        print(c_id, 'Done')


    '''
    for i in range(81):
        writeTclFileSegname(cluster_data, i , "cluster_files/cluster_"+str(i)+".tcl") '''


