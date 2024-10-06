package require psfgen

source superbox_input_param.tcl
set base_path frame_$frame_id/super_box_pdb

for { set i 1 } { $i < 28 } {incr i} {
        set psffile_$i $base_path/output_new_segids_pdbfile_$i.psf
        set pdbfile_$i $base_path/output_new_segids_pdbfile_$i.pdb
}

readpsf $psffile_1 pdb $pdbfile_1
readpsf $psffile_2 pdb $pdbfile_2
readpsf $psffile_3 pdb $pdbfile_3
readpsf $psffile_4 pdb $pdbfile_4
readpsf $psffile_5 pdb $pdbfile_5
readpsf $psffile_6 pdb $pdbfile_6
readpsf $psffile_7 pdb $pdbfile_7
readpsf $psffile_8 pdb $pdbfile_8
readpsf $psffile_9 pdb $pdbfile_9
readpsf $psffile_10 pdb $pdbfile_10
readpsf $psffile_11 pdb $pdbfile_11
readpsf $psffile_12 pdb $pdbfile_12
readpsf $psffile_13 pdb $pdbfile_13
readpsf $psffile_14 pdb $pdbfile_14
readpsf $psffile_15 pdb $pdbfile_15
readpsf $psffile_16 pdb $pdbfile_16
readpsf $psffile_17 pdb $pdbfile_17
readpsf $psffile_18 pdb $pdbfile_18
readpsf $psffile_19 pdb $pdbfile_19
readpsf $psffile_20 pdb $pdbfile_20
readpsf $psffile_21 pdb $pdbfile_21
readpsf $psffile_22 pdb $pdbfile_22
readpsf $psffile_23 pdb $pdbfile_23
readpsf $psffile_24 pdb $pdbfile_24
readpsf $psffile_25 pdb $pdbfile_25
readpsf $psffile_26 pdb $pdbfile_26
readpsf $psffile_27 pdb $pdbfile_27

writepsf $base_path/merged_superbox.psf
writepdb $base_path/merged_superbox.pdb

exit
