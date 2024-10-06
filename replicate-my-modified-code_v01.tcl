
#set input_pdb_file fff-600-mol-250-angst-box-npt_last_20ns_final_only_protein.pdb

source superbox_input_param.tcl
#set input_pdb_file fff-600-mol-250A-box_frame_50.pdb 

# List of properties relevant for PDB format
set proplist {name chain resid resname x y z segid}

# Process the input molecule
set molid_in [mol new $input_pdb_file]
set numatoms_in [molinfo $molid_in get numatoms]
set sel_all_in [atomselect $molid_in "all"]
set original_coordinates [$sel_all_in get {x y z}]
set atomdata_in [$sel_all_in get $proplist]

#set list_of_atom_data ""
set fp [open "$save_path_pdb/translation_vector_index_track_list.txt" w+]

#set box_length_x 246.719879
#set box_length_y 246.719879
#set box_length_z 246.719879
set num_replica 1
set numatoms_new 0
set n 1

set translation_vector_index_track_list ""
for {set i [expr -1*$num_replica]} {$i <=  $num_replica} {incr i} {
    for {set j [expr -1*$num_replica]} {$j <=  $num_replica} {incr j} {
        for {set k [expr -1*$num_replica]} {$k <=  $num_replica} {incr k} {
			set trans_vec_x [expr ($i)*$box_length_x]
	        set trans_vec_y [expr ($j)*$box_length_y]
	        set trans_vec_z [expr ($k)*$box_length_z]
	        set translation_vec [list $trans_vec_x $trans_vec_y $trans_vec_z]
	        puts "$translation_vec"
	        puts "[llength $translation_vec]"
	        for {set l 0} {$l < 3} {incr l} {
	        	set i_rel [expr int([lindex $translation_vec 0] / $box_length_x)]
	        	set j_rel [expr int([lindex $translation_vec 1] / $box_length_x)]
	        	set k_rel [expr int([lindex $translation_vec 2] / $box_length_x)]
	        }
	        #puts "$i_rel$j_rel$k_rel"
	        set strng " "
	        lappend strng "$i_rel $j_rel $k_rel"
			set molid_out [mol new atoms $numatoms_in]
			animate dup $molid_out
			set list_of_atom_data ""
			$sel_all_in moveby $translation_vec
			set atomdata [$sel_all_in get $proplist]
			set list_of_atom_data [concat $list_of_atom_data $atomdata]
			set sel_all_new [atomselect $molid_out "all"]
	        $sel_all_new set $proplist $list_of_atom_data
			animate write pdb $save_path_pdb/output_water1_pdb_file$n.pdb

			#set one_elem_trans_vec_index ""
			#append one_elem_trans_vec_index $n
			#append one_elem_trans_vec_index $strng	
			#puts "$one_elem_trans_vec_index"		
			#animate write pdb output_water1_pdb_file$strng.pdb
			puts $fp "$n  $strng "
			#lappend translation_vector_index_track_list $one_elem_trans_vec_index
			set numatoms_new [expr $numatoms_new + $numatoms_in]
			$sel_all_in set {x y z} $original_coordinates
			set n [expr $n + 1]
		}
    }	
}
close $fp
#puts "$translation_vector_index_track_list"
exit
