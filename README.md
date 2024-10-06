# periodic_reconstruction_algorithm
This algorithm reconstructs the periodically separated states to it's original appearance. For input a pdb is used. As an output user will get a pdb-psf file .
######################################################################################

#During the formation stage of the small clusters, the periodic boundary condition (PBC) gives rise to some really #difficult issues. These issues may cause problem for both quantitative calculation and visualization. To solve these #issues, one can do thorough PBC correction on the clusters. However, this stage is a formation stage. So we have #to consider all the scenarios very carefully and construct a logical algorithm for each and every case. #The major problem arises during case-wise correction of 26 scenarios(8 corners points, 6 faces and 12 edges) #which can be computationally expensive. So the aim is to handle this issue in a less computationally expensive #manner.

#For the automated PBC correction of clusters in specific frame, total twelve codes(7 tcl scripts, 3 python codes #and 1 bash script) are executed altogether serially. superbox input param.tcl is the input tcl file for super #box creation. The main program to run is ”PBC corrected superbox Freud v01.py” and it makes appropriate #calls to other scripts. Below is a list of the sequential procedure that PBC corrected superbox Freud v01.py follows.

##################################################################################

1. First, the super box is created for the particular frame. It requires to run a series of tcl scripts, which are
launched from a shell script :
”script superbox formation frame v01.sh”. The shell script contains seven tcl script as follows.
(a) replicate-my-modified-code v01.tcl : replicates the original box 26 times and thereby creating a
total of 27 box with identical pdb’s and also returns a .txt file containing pdb index vs translation vector
data.
(b) extract segname from pdb v01.tcl : returns two separate lists containing protein segment list and
water segment list respectively.
(c) new sgnames creation for new pdbs v01.tcl : returns 27 unique list of peptide segments,where
list-14 represents the original segment list of the system undergoing production simulation. This is in
accordance with the replicated pdb’s, where pdb-14 represents the central box. This is a pure tcl code,
so can be run with tclsh filename
(d) segname assign for replicated pdb v01.tcl : returns 27 sets of pdb-psf, where the pdb-14 is the
original box and contains actual segment names from original.
(e) super pdb psf creation v01.tcl : takes these 27 pairs of pdb-psf as input and create a superbox with
a total of (27×number of peptides in the original box) unique segment name
(f) make seganme map original replicate v01.tcl : makes a map between the original segnames and
the segnames in the replicated system, where the replica id of the original system is 14. One tcl file
is written with the map for each replicate system. The map data structure consists of list (segnamereplicate
segname-original). This code also returns a JSON file where keys are new segment names and
the values are old segment names.
(g) extract pdb all txt v01.tcl : extracts all atoms from the super-box pdb-psf set to create a merge superbox.txt
file.
Final Output file : merge superbox.txt, it is a txt file very similar to xyz file

#--------------------------------------------------------------------------

2. FREUDcluster frame v01.py : Then FREUD clustering is applied to the super box : merge superbox.txt
with atomic cutoff distance = 3. As we apply Freud clustering on super box, so the number of clusters are 27
times the actual number of clusters. This code is used as a header function for the main program.
3. Among the clusters formed from Freud has maximum matching with the actual clusters, segname of the
central box are considered and stores clusters xyz files in PBC corrected freud of the particular frame.
4. At last merge all the clusters in one xyz file namely ”join all cluster.xyz” and stored in the respective
frame ”PBC corrected freud” directory.
5. readXYZ v01.py and support code v01.py are two supporting codes for the main program.

#-----------------------------------------------------------------------

2.2 Folder Structure

1. All the nine codes and the shell script must be placed in the parent directory. All the frames are
its subdirectory.
2. Inside each frame id, it will create four subfolders namely
(a) super box pdb same seg : Stores all the 27 pdb files have same segment names as that of the original
pdb.
(b) super box pdb : Stores the 27 pdb and psf files with unique segment names.
(c) super box seg : Contains the segname maps between each replica box and central box.
(d) super box xyz : Stores 27 xyz replicas of the super box.
(e) PBC corrected freud : Contains all the PBC corrected clusters in xyz file format.

#######################################################################

2.3 Input Parameters All the input parameters are given in the main code ”PBC corrected superbox Freud v01.py” with respective line number.

1. start frame, end frame : Provide the starting and ending frame numbers on which the PBC correction
applied. Make the change in Line No. 44,45
2. num cluster list : This is the list of number of interaction based clusters each frame has and it gets the
information from ”number of cluster per frame.txt”
3. box length list : List of length of box per frame and takes the input from ”box length.txt”
4. base pdb file : It contains the base name of the original pdb file of a particular frame. Make the change
in Line No. 53
5. central pdb base path : The path of the original pdb file. Make the change in Line No. 61
6. cutoff for clustering : This is the atomic distance cutoff for FREUD clustering on super box. If require
make change in line no. 71.
