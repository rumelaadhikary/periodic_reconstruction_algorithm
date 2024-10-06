#!/bin/bash

vmd -dispdev text -e replicate-my-modified-code_v01.tcl
vmd -dispdev text -e extract_segname_from_pdb_v01.tcl
tclsh new_sgnames_creation_for_new_pdbs_v01.tcl
vmd -dispdev text -e segname_assign_for_replicated_pdb_v01.tcl
vmd -dispdev text -e super_pdb_psf_creation_v01.tcl
vmd -dispdev text -e make_seganme_map_original_replicate_v01.tcl 
vmd -dispdev text -e extract_pdb_all_txt_v01.tcl
