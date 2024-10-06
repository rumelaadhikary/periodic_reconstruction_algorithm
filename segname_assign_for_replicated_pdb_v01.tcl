source superbox_input_param.tcl

set num_atoms_one_seg 63
#set replica 28
for {set l 1 } { $l < 28 } {incr l } {
	source frame_$frame_id/super_box_seg/segment_list_$l.tcl
	set filename_input_pdb frame_$frame_id/super_box_pdb_same_seg/output_water1_pdb_file$l.pdb
	set filename_output_pdb frame_$frame_id/super_box_pdb/output_new_segids_pdbfile_$l.pdb
	set filename_output_psf frame_$frame_id/super_box_pdb/output_new_segids_pdbfile_$l.psf

	mol load pdb $filename_input_pdb
	#mol new {$filename_input_pdb} type {pdb} first 0 last -1 step 1 waitfor 1
	set all_atoms [atomselect top all]
	set num_atoms [$all_atoms num]


	set num_seg [expr $num_atoms / $num_atoms_one_seg]

	# serial numbers are the 1-based atom numbers in the PDB file
	set all_serial_numbers [$all_atoms get serial]
	#puts $all_serial_numbers

	for { set i 0 } { $i < $num_seg } { incr i } {
		set new_segid [lindex $protein_seglist $i]
		#puts $new_segid
		set first_lim [expr  $num_atoms_one_seg * $i  + 1]
		set k [expr $i + 1]
		set last_lim [expr $num_atoms_one_seg * $k]
		for { set j [expr $first_lim - 1] } { $j < $last_lim } { incr j} {
			set one_atom [atomselect top "serial [lindex $all_serial_numbers $j]"]
	    	$one_atom set segname $new_segid
	    	#puts "$first_lim $last_lim $j $new_segid"
	    	$one_atom delete
		}
	    
	}
	#$all_atoms delete
	
	$all_atoms writepdb $filename_output_pdb
	$all_atoms writepsf $filename_output_psf

	#delete $mol
	#mol delete [expr $l - 1]
	puts "box_$l complete"
}

#source segment_list_2.tcl

#set filename_input_pdb output_water1_pdb_file2.pdb
#set filename_output_pdb output_pdbfile2_new_segids.pdb

#mol load pdb $filename_input_pdb
#set all_atoms [atomselect top all]
#set num_atoms [$all_atoms num]

#set num_seg [expr $num_atoms / $num_atoms_one_seg]

#puts "num_seg: $num_seg"

# serial numbers are the 1-based atom numbers in the PDB file
#set all_serial_numbers [$all_atoms get serial]

#puts "$num_atoms"

#set new_segid [lindex $protein_seglist_2 0]

#for { set i 0 } { $i < $num_seg } { incr i } {
#	set new_segid [lindex $protein_seglist_2 $i]
#	puts $new_segid
#	set first_lim [expr  $num_atoms_one_seg * $i  + 1]
#	set k [expr $i + 1]
#	set last_lim [expr $num_atoms_one_seg * $k]
#	for { set j [expr $first_lim - 1] } { $j < $last_lim } { incr j} {
#		set one_atom [atomselect top "serial [lindex $all_serial_numbers $j]"]
 #   	$one_atom set segname $new_segid
  #  	puts "$first_lim $last_lim $j $new_segid"
	#}
    
#}

#$all_atoms writepdb $filename_output_pdb


#mol new $pdbfile
#set sel [atomselect top all]
#set segnames_protein [lsort -unique [${sel} get segname]]
#puts $segnames_protein
#$sel delete
#foreach segid $protein_seglist_1 {
#	$
#}
#coordpdb $pdbfile 
#for { set i 0 } { $i < [llength $segnames_protein] } {incr i } {
#	pdbalias segname [lindex $segnames_protein $i] [lindex $protein_seglist_1 $i]
#}
#coordpdb $pdbfile 
#writepdb test.pdb	
#set fp [open $pdbfile "r"]
#set file_data [read $fp]
#close $fp

#  Process data file
#set data [split $file_data "\n"]
#foreach line $data {
     # do some line processing here
     #puts $line
     #set item [split $line]
#     set item ""
#     set item [regexp -all -inline {\S+} $line]
#     set last_val [llength $item]
#     puts $last_val
#     puts [lindex $item $last_val]
#}

exit
