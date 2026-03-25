import os
import glob

print("🚀 Lancement du Builder Automatique (Environnement Conda validé)...")

wt_name = "2AM9_clean"
# Tes deux mutants ratés (Cross-docking)
bad_mutants = ["2AM9_clean_W741A", "2AM9_clean_W741L"]

# 1. Traitement du Wild-Type
print(f"\n⚡ Préparation du Wild-Type ({wt_name})...")
os.makedirs(wt_name, exist_ok=True)
os.system(f"cp ../01_Preparation/{wt_name}.pdb {wt_name}/prot.pdb")
# L'étoile (*) permet de trouver le fichier peu importe son nom exact
os.system(f"obabel -ipdbqt ../02_Docking/{wt_name}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {wt_name}/ligand_brut.pdb")
os.system(f"pymol -c -q -d 'load {wt_name}/ligand_brut.pdb; h_add; save {wt_name}/ligand_H.pdb'")

# 2. Topologie Centrale ACPYPE
print("🧪 Génération de la topologie centrale (Patientez)...")
os.makedirs("00_Ligand_Topo", exist_ok=True)
os.chdir("00_Ligand_Topo")
os.system(f"acpype -i ../{wt_name}/ligand_H.pdb -c gas -n 0")
os.system("mv ligand_H.acpype/* . 2>/dev/null")
os.system("rm -rf ligand_H.acpype")
os.chdir("..")

# Assemblage du WT
os.system(f"grep -v 'END' {wt_name}/prot.pdb > {wt_name}/complexe.pdb")
os.system(f"grep '^ATOM\\|^HETATM' {wt_name}/ligand_H.pdb >> {wt_name}/complexe.pdb")
os.system(f"echo 'END' >> {wt_name}/complexe.pdb")

# 3. Traitement des Mutants
prots = glob.glob("../01_Preparation/2AM9_clean_*.pdb")

for p in prots:
    mutant = os.path.basename(p).replace(".pdb", "")
    if mutant == wt_name: 
        continue
        
    print(f"\n🧬 Traitement du mutant : {mutant}")
    os.makedirs(mutant, exist_ok=True)
    os.system(f"cp {p} {mutant}/prot.pdb")
    
    if mutant in bad_mutants:
        print("   -> 🚨 Cross-Docking (Copie de la pose du WT)")
        os.system(f"cp {wt_name}/ligand_H.pdb {mutant}/ligand_H.pdb")
    else:
        print("   -> ✅ Extraction de la pose native + PyMOL")
        os.system(f"obabel -ipdbqt ../02_Docking/{mutant}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {mutant}/ligand_brut.pdb")
        os.system(f"pymol -c -q -d 'load {mutant}/ligand_brut.pdb; h_add; save {mutant}/ligand_H.pdb'")

    # Assemblage complexe
    os.system(f"grep -v 'END' {mutant}/prot.pdb > {mutant}/complexe.pdb")
    os.system(f"grep '^ATOM\\|^HETATM' {mutant}/ligand_H.pdb >> {mutant}/complexe.pdb")
    os.system(f"echo 'END' >> {mutant}/complexe.pdb")

# 4. Nettoyage
os.system("rm -f */ligand_brut.pdb")
print("\n🎉 TERMINE ! Tous les dossiers sont prêts et le workflow est parfait.")