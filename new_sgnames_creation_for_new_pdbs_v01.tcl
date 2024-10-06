##################################################################################
#####   THIS CODE RETURNS 27 UNIQUE LISTS OF PEPTIDE SEGMENTS, WHERE LIST_14  ####
#####   REPRESENTS THE ORIGINAL SEGMENT LIST OF THE SYSTEM UNDERGOING         ####
#####   PRODUCTION SIMULATION. THIS IS IN ACCORADANCE WITH THE REPLICATED     ####
#####   PDB'S, WHERE PDB_14 REPRESENTS THE CENTRAL BOX                        ####
##################################################################################


############### UNIQUE LIST GENERATION ################################## 
set list_of_charecters {"A" "B" "C" "D" "E" "F" "G"
                        "H" "I" "J" "K" "L" "M" "N"
                        "O" "P" "Q" "R" "S" "T" "U"
                        "V" "W" "X" "Y" "Z"}

# generate random integer number in the range [min,max]
proc RandomInteger4 {min max} {
    return [expr {int(rand()*($max-$min+1)+$min)}]
}

# Generate a random string by picking charectors from a list
proc generate_one_string { list_of_charecters width } {
    set length_of_list [llength $list_of_charecters]
    set min 0
    set max [expr $length_of_list - 1]
    set output ""
    for {set i 0} {$i < $width} {incr i} {
        set index [RandomInteger4 $min $max]
        set output $output[lindex $list_of_charecters $index]
    }
    return $output
}

# Generate a list of random strings with unique entires. Each string
# has a specified width and the list consists of unique entries
proc generate_unique_list_of_strings { list_of_strings list_of_charecters width num_strings } {
    #set list_of_strings ""
    while { [llength $list_of_strings] < $num_strings } {
        set one_string [generate_one_string $list_of_charecters $width]
        lappend list_of_strings $one_string
        set list_of_strings [lsort -unique $list_of_strings]
    }
    return $list_of_strings
}

############## FIND COMMON ELEMENTS IN TWO LISTS ##############################

proc common_between_two_list { list1 list2 } {
	set list_xy ""
	foreach x $list1 {
		#lappend list_x $x
		set cache($x) 1
	}
	foreach y $list2 {
		#lappend list_y $y
    	if {[info exists cache($y)]} {
        	lappend list_xy $y
    	}
	}
	return $list_xy

}

source superbox_input_param.tcl
source frame_$frame_id/super_box_pdb_same_seg/protein_segments.tcl
set num_mol [llength $protein_seglist]
set num_replica 27
set total_segname [expr $num_replica * $num_mol]

set list_of_segments [generate_unique_list_of_strings $protein_seglist $list_of_charecters 4 $total_segname]
set common_elem [common_between_two_list $protein_seglist $list_of_segments]
puts "[llength $common_elem]"
puts "[llength $list_of_segments]"

###################### REMOVES THE ORIGINAL SEGLIST FROM THE 27 x $num_mol SEGLIST #############
foreach i $protein_seglist {
	set idx [lsearch $list_of_segments "$i"]
	set list_of_segments [lreplace $list_of_segments $idx $idx]
}

#puts "asdfg [llength $list_of_segments]"
set list_of_segments [lsort -unique $list_of_segments]
#puts "pokijh $list_of_segments"
##################### FILE OUTPUT #####################################

#set fp [open "segment_list_14.tcl" w]
#puts $fp "set protein_seglist \{ $protein_seglist \}"
#close $fp

for { set j 1} { $j <= 27 } {incr j } {
	if { $j < 14} {
		set i $j
		set k [expr $j - 1]		
	} elseif { $j > 14 } {
		set i $j 
		set k [expr $j - 2]
	} else {
		set fp [open "frame_$frame_id/super_box_seg/segment_list_14.tcl" w]
		puts $fp "set protein_seglist \{ $protein_seglist \}"
		close $fp
		#puts "its box 14"
	}
	set first_range [expr  $num_mol * $k  + 0]
	set last_range [expr  $num_mol * $k  + ($num_mol - 1)]
	puts "$first_range $last_range"
	set list_new ""
	set list_new [lrange $list_of_segments $first_range $last_range]
	#puts "box $j"
	#puts "$list_new"

	set fp [open "frame_$frame_id/super_box_seg/segment_list_$i.tcl" w]
	puts $fp "set protein_seglist \{ $list_new \} "
	close $fp

}



exit
