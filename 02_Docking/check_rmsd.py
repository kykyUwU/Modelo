from pymol import cmd
import glob
import os

wt_name = "2AM9_clean"
wt_ligand = f"{wt_name}/ligand_H.pdb"

print("\n" + "="*65)
print("🎯 ANALYSE DES POSES DE DOCKING (RMSD vs Wild-Type)")
print("="*65)

# Vérification du WT
if not os.path.exists(wt_ligand):
    print(f"❌ Erreur : Impossible de trouver le ligand du WT ({wt_ligand})")
    cmd.quit()

# On charge le ligand de référence
cmd.load(wt_ligand, "lig_wt")

# On cherche tous les ligands des mutants
ligands_mutants = glob.glob("*/ligand_H.pdb")

for mut_ligand in sorted(ligands_mutants):
    mutant = os.path.dirname(mut_ligand)
    
    # On ignore le WT pour ne pas le comparer à lui-même
    if mutant == wt_name:
        continue
        
    cmd.load(mut_ligand, "lig_mut")
    
    # rms_cur calcule la différence spatiale exacte sans faire bouger les molécules
    rmsd = cmd.rms_cur("lig_mut", "lig_wt")
    
    # Interprétation des résultats
    if rmsd == 0.0:
        status = "🚨 Cross-Docking (Copie exacte)"
    elif rmsd <= 2.0:
        status = "✅ Bien dans la poche (Même pose)"
    elif rmsd <= 4.0:
        status = "⚠️ Légèrement décalé"
    else:
        status = "❌ Hors de la poche (Éjecté !)"
        
    print(f"🔹 {mutant:<25} | RMSD = {rmsd:>5.2f} Å | {status}")
    
    # On nettoie pour le prochain tour
    cmd.delete("lig_mut")

print("="*65 + "\n")
cmd.quit()