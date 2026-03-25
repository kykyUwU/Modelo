import os
import glob

print("🚀 Lancement du Builder Automatique (Environnement Conda)...")

# --- VARIABLES GLOBALES ---
wt_name = "2AM9_clean"
bad_mutants = ["2AM9_clean_W741A", "2AM9_clean_W741L"]

# ==========================================
# 1. Traitement du Wild-Type
# ==========================================
print(f"\n⚡ Préparation du Wild-Type ({wt_name})...")
os.makedirs(wt_name, exist_ok=True)
# On s'assure que le PDB de la protéine est bien copié dans son dossier
os.system(f"cp {wt_name}.pdb {wt_name}/prot.pdb 2>/dev/null") 

# OpenBabel extrait la Pose 1, PyMOL met TOUS les hydrogènes
os.system(f"obabel -ipdbqt {wt_name}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {wt_name}/ligand_brut.pdb 2>/dev/null")
os.system(f"pymol -c -q -d 'load {wt_name}/ligand_brut.pdb; h_add; save {wt_name}/ligand_H.pdb' >/dev/null 2>&1")

# ==========================================
# 2. Topologie Centrale ACPYPE
# ==========================================
print("🧪 Génération de la topologie centrale ACPYPE (Patientez)...")
os.makedirs("00_Ligand_Topo", exist_ok=True)
os.chdir("00_Ligand_Topo")
os.system(f"acpype -i ../{wt_name}/ligand_H.pdb -c gas -n 0 > /dev/null 2>&1")
os.system("mv ligand_H.acpype/* . 2>/dev/null")
os.system("rm -rf ligand_H.acpype")
os.chdir("..")

# Assemblage du WT
os.system(f"grep -v 'END' {wt_name}/prot.pdb > {wt_name}/complexe.pdb 2>/dev/null")
os.system(f"grep '^ATOM\\|^HETATM' {wt_name}/ligand_H.pdb >> {wt_name}/complexe.pdb 2>/dev/null")
os.system(f"echo 'END' >> {wt_name}/complexe.pdb")

# ==========================================
# 3. Traitement de tous les Mutants (dans tes dossiers triés)
# ==========================================
# On cherche directement tes dossiers mutants (grâce au slash à la fin)
dossiers_mutants = glob.glob("2AM9_clean_*/")

for dossier in dossiers_mutants:
    mutant = dossier.replace("/", "") # On enlève le slash pour avoir le nom propre
    
    if mutant == wt_name: 
        continue
        
    print(f"\n🧬 Traitement du mutant : {mutant}")
    
    # On s'assure que le PDB du mutant est bien dans son dossier
    os.system(f"cp {mutant}.pdb {mutant}/prot.pdb 2>/dev/null")
    
    # Aiguillage : Cross-Docking ou Docking Natif ?
    if mutant in bad_mutants:
        print("   -> 🚨 Cross-Docking (Copie de la pose du WT)")
        os.system(f"cp {wt_name}/ligand_H.pdb {mutant}/ligand_H.pdb 2>/dev/null")
    else:
        print("   -> ✅ Extraction de la pose native + PyMOL")
        os.system(f"obabel -ipdbqt {mutant}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {mutant}/ligand_brut.pdb 2>/dev/null")
        os.system(f"pymol -c -q -d 'load {mutant}/ligand_brut.pdb; h_add; save {mutant}/ligand_H.pdb' >/dev/null 2>&1")

    # Assemblage du complexe pour le mutant
    os.system(f"grep -v 'END' {mutant}/prot.pdb > {mutant}/complexe.pdb 2>/dev/null")
    os.system(f"grep '^ATOM\\|^HETATM' {mutant}/ligand_H.pdb >> {mutant}/complexe.pdb 2>/dev/null")
    os.system(f"echo 'END' >> {mutant}/complexe.pdb")

# ==========================================
# 4. Nettoyage final
# ==========================================
os.system("rm -f */ligand_brut.pdb")
print("\n🎉 TERMINE ! Tous tes dossiers triés contiennent maintenant leur 'complexe.pdb'.")