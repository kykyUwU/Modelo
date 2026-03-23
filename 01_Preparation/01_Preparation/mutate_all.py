import pymol
from pymol import cmd
import os

INPUT_PDB = "2AM9_clean.pdb"
MUTATIONS = [
    "T877A", "T877S",
    "Q711A", "Q711V",
    "R752A",
    "W741L", "W741A",
    "M745A",
    "F764A"
]

AA_MAP = {
    'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE',
    'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU',
    'M': 'MET', 'N': 'ASN', 'P': 'PRO', 'Q': 'GLN', 'R': 'ARG',
    'S': 'SER', 'T': 'THR', 'V': 'VAL', 'W': 'TRP', 'Y': 'TYR'
}

pymol.finish_launching(['pymol', '-cq'])

def make_mutant(mutation_str):
    # Décryptage
    pos = mutation_str[1:-1]
    new_aa = mutation_str[-1].upper()
    resn_3l = AA_MAP.get(new_aa)
    
    # Nom du fichier de sortie basé sur l'input
    base_name = INPUT_PDB.replace('.pdb', '')
    out_name = f"{base_name}_{mutation_str}.pdb"
    
    # Commandes PyMOL
    cmd.load(INPUT_PDB, "prot")
    cmd.wizard("mutagenesis")
    cmd.get_wizard().do_select(f"resi {pos}")
    cmd.get_wizard().set_mode(resn_3l)
    cmd.get_wizard().apply()
    cmd.save(out_name, "prot")
    cmd.delete("all")
    print(f"{out_name} Done")

print(f"{INPUT_PDB}")

for mut in MUTATIONS:
    make_mutant(mut)

print("End")