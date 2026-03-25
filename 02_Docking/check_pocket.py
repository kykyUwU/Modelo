import glob
import os
from pymol import cmd
import numpy as np

wt_name = "2AM9_clean"
wt_pdbqt = f"{wt_name}/{wt_name}_resultat.pdbqt"

print("\n" + "="*65)
print("🔍 VÉRIFICATION DES POSES (Par distance du Centre de Masse)")
print("="*65)

if not os.path.exists(wt_pdbqt):
    print(f"❌ Erreur : Impossible de trouver le résultat du WT ({wt_pdbqt})")
    cmd.quit()

# On charge le WT et on calcule son centre
cmd.load(wt_pdbqt, "wt_lig", state=1)
coords_wt = cmd.get_coords("wt_lig", 1)
centre_wt = coords_wt.mean(axis=0)

dossiers = sorted(glob.glob("2AM9_clean_*/"))

for dossier in dossiers:
    mutant = dossier.replace("/", "")
    if mutant == wt_name: 
        continue
        
    mut_pdbqt = f"{mutant}/{mutant}_resultat.pdbqt"
    
    if os.path.exists(mut_pdbqt):
        cmd.load(mut_pdbqt, "mut_lig", state=1)
        
        # On calcule le centre du mutant
        coords_mut = cmd.get_coords("mut_lig", 1)
        centre_mut = coords_mut.mean(axis=0)
        
        # Calcul de la distance pure en 3D (sans se soucier de l'ordre des atomes)
        distance = np.linalg.norm(centre_wt - centre_mut)
        
        if distance <= 2.5:
            status = "✅ Pile dans la poche"
        elif distance <= 5.0:
            status = "⚠️ Légèrement décalé (mais dedans)"
        else:
            status = "❌ Éjecté (Hors de la poche)"
            
        print(f"🔹 {mutant:<22} | Décalage du centre = {distance:>5.2f} Å | {status}")
        
        cmd.delete("mut_lig")
    else:
        print(f"🔹 {mutant:<22} | ❌ Fichier manquant")

print("="*65 + "\n")
cmd.quit()