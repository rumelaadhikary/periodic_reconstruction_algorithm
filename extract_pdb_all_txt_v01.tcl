source superbox_input_param.tcl
set base_path frame_$frame_id/super_box_pdb

set input_pdb_file $base_path/merged_superbox.pdb

# List of properties relevant for PDB format
#set proplist {name resid x y z segid}
set proplist {segid resid name x y z}

# Process the input molecule
set molid_in [mol new $input_pdb_file]
set numatoms_in [molinfo $molid_in get numatoms]
set sel_all_in [atomselect $molid_in "all"]
#set original_coordinates [$sel_all_in get {x y z}]
set atomdata_in [$sel_all_in get $proplist]

#set id_x [lindex $atomdata_in 0]
#puts [llength $id_x]
set fileID [open "$base_path/merge_superbox.txt" "w"]

puts $fileID [llength $atomdata_in]
puts $fileID "Generated from code : extract_pdb_all_txt_v01.tcl"
foreach i $atomdata_in {
    puts $fileID $i
    #set elem_1 
}

close $fileID

exit
