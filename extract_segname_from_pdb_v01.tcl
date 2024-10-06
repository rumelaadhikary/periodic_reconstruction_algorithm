# Get the segment names of all peptide from pdb
source superbox_input_param.tcl

#set pdb_file fff-600-mol-250A-box_frame_$frame_id.pdb
#set psf_file fff-600-mol-250A-box.psf

set f_protein [open "frame_$frame_id/super_box_pdb_same_seg/protein_segments.tcl" w+]
set f_water [open "frame_$frame_id/super_box_pdb_same_seg/water_segments.tcl" w+]

#set molid [mol load psf $psf_file pdb $pdb_file]
set molid [mol load pdb $pdb_file]

set sel_protein [atomselect $molid "protein" frame 0]
set sel_water [atomselect $molid "water" frame 0]

set segnames_protein [lsort -unique [${sel_protein} get segname]]
set num_peptide_segments [llength $segnames_protein]
set segnames_water [lsort -unique [${sel_water} get segname]]
set num_water_segments [llength $segnames_water]

puts $f_protein "set protein_seglist \{ $segnames_protein \} "
puts $f_water "set water_seglist \{ $segnames_water \} "
puts "No. of protein segments: $num_peptide_segments"
puts "No. of water segments: $num_water_segments"
puts "No. of water atoms: [$sel_water num]"

close $f_protein
close $f_water
exit
