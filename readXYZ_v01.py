'''
Functions for reading xyz files
'''

import numpy as np

'''
Reads an XYZ file with single frame and returns a

The input is a list of all lines from the XYZ file

Returns a dictionary of the following format
{"num_particles": Number_of_particles,
 "names": [list of particle names],
 "coordinates": [Nx3 numpy array of particle coordiantes]}
'''
def ReadXYZframe(lines):
    return_dict = {}
    first_line_split = lines[0].split()
    return_dict["num_particles"] = int(first_line_split[0])
    particle_names = []
    particle_coordinates = [[] for i in range(return_dict["num_particles"])]
    for i in range(return_dict["num_particles"]):
        items = lines[i+2].split()
        particle_names.append(items[0])
        particle_coordinates[i].append(float(items[1]))
        particle_coordinates[i].append(float(items[2]))
        particle_coordinates[i].append(float(items[3]))
    return_dict["names"] = particle_names
    return_dict["coordinates"] = np.array(particle_coordinates)
    return return_dict

# Returns the dictionary of data in the above format from an XYZ file with a
# single frame
def ReadXYZfile(xyz_filename):
    lines = [line.strip() for line in open(xyz_filename, "r")]
    return ReadXYZframe(lines)

def Read_XYZ_txt(input_xyz_file):
    data=np.genfromtxt(input_xyz_file,dtype=str,skip_header=2)
    data_float=np.genfromtxt(input_xyz_file,skip_header=2)

    particle_coordinates=data_float[:,3:6]
    segname=data[:,0]
    resid=data[:,1]
    atom=data[:,2]
    len_particle=len(segname)
    particle_name=[]

    for i in range(len_particle):
        seg=segname[i]+"_"+resid[i]+"_"+atom[i]
        particle_name.append(seg)

    return_dict = {}
    return_dict["num_particles"] = int(len_particle)

    return_dict["coordinates"] = np.array(particle_coordinates)
    return_dict["names"] = particle_name
    return return_dict





def main():
    xyz_filename = 'super_box_CA.xyz'
    xyz_data = ReadXYZfile(xyz_filename)
    print(xyz_data["num_particles"])
    print(xyz_data["names"])
    print(xyz_data["coordinates"])

if __name__ == "__main__":
    main()
