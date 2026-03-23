import pymol
from pymol import cmd

# Lancement de PyMOL en mode "Fantôme" (sans interface)
pymol.finish_launching(['pymol', '-cq'])

# Dictionnaire de tes mutations : {Position: "Nouvel_Acide_Aminé"}
mutations = {
    "877": "ALA", # T877A
    "874": "TYR", # H874Y
    "715": "MET", # V715M
    "701": "HIS", # L701H
    "876": "LEU", # F876L
    "741": "LEU", # W741L
}

# On ajoute aussi le W741C à part pour ne pas écraser le W741L
mutations_extra = {"741": "CYS"}

def make_mutant(resi, resn, out_name):
    cmd.load("2AM9_clean.pdb", "prot")
    cmd.wizard("mutagenesis")
    cmd.get_wizard().do_select(f"resi {resi}")
    cmd.get_wizard().set_mode(resn)
    # Applique la mutation avec le meilleur rotamère par défaut (sans collision)
    cmd.get_wizard().apply() 
    cmd.save(out_name, "prot")
    cmd.delete("all")
    print(f"✅ Mutant {out_name} généré avec succès !")

print("🚀 Démarrage de l'usine à mutants...")

# Boucle principale
for pos, aa in mutations.items():
    make_mutant(pos, aa, f"2AM9_mut_{pos}{aa}.pdb")

# Le petit extra (W741C)
make_mutant("741", "CYS", "2AM9_mut_741CYS.pdb")

print("End")