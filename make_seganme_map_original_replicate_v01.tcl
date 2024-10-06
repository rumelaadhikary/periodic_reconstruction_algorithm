# Make a map bwtween the original segnames and the segnames in the 
# replicated system
# Replica id of the original system is 14
# One tcl file is written with the map for each replicate
# The map data structure consists of list {segname_replicate segname_original}
#
# It also write a JSON file where keys are new segment names and the values are old 
# segment names 

source superbox_input_param.tcl
set rep_id_list {1 2 3 4 5 6 7 8 9 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27}

# Original segname list 
source frame_$frame_id/super_box_seg/segment_list_14.tcl
set segname_list_original $protein_seglist
set num_mols [llength $segname_list_original]

# This list stores the Python dict entries as strings 
set list_py_dic_entries {}
foreach rep_id $rep_id_list {
	set map_list_one_rep {}
	source frame_$frame_id/super_box_seg/segment_list_${rep_id}.tcl
	set segname_list_replicate $protein_seglist
	# Loop over all segments in the current replicate 
	for {set i 0} {$i < $num_mols} {incr i} {
		set one_map {}
		lappend one_map [lindex $segname_list_replicate $i]
		lappend one_map [lindex $segname_list_original $i]
		lappend map_list_one_rep $one_map
		set str_one_pyt_dict_entry "\"[lindex $segname_list_replicate $i]\" : \"[lindex $segname_list_original $i]\""
		lappend list_py_dic_entries $str_one_pyt_dict_entry
	}
	set fp [open "frame_$frame_id/super_box_seg/segname_map_${rep_id}.tcl" w]
	puts $fp "set segname_map \{ $map_list_one_rep \}"
	close $fp
}

# Write the JSON file 
set num_py_dict_entries [llength $list_py_dic_entries]
set num_minus_1 [expr $num_py_dict_entries - 1]
set fpJSON [open "frame_$frame_id/super_box_seg/segname_map_master.json" w]
puts $fpJSON "\{ "
for {set j 0} {$j < $num_py_dict_entries} {incr j} {
	if {$j == $num_minus_1} {
		puts $fpJSON "[lindex $list_py_dic_entries $j]"
	} else {
		puts $fpJSON "[lindex $list_py_dic_entries $j], "
	}
}
puts $fpJSON " \}"
close $fpJSON
exit
