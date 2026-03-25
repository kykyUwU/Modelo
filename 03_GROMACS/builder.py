import os
import glob

print("🚀 Lancement du Builder V3 (Routage Intelligent)...")

# --- PARAMÈTRES ET RÈGLES ---
wt_name = "2AM9_clean"
bad_mutants = ["2AM9_clean_W741A", "2AM9_clean_W741L"]       # Cross-Docking
targeted_mutants = ["2AM9_clean_Q711A", "2AM9_clean_R752A"]  # Les 2 ciblés dans Docking_2

# Fonction d'aiguillage automatique
def get_path(mutant):
    if mutant in targeted_mutants:
        return f"02_Docking/Docking_2/{mutant}"
    else:
        return f"02_Docking/Docking_1/{mutant}"

# On dresse la liste de TOUS tes mutants en scannant les deux dossiers
dossiers = glob.glob("02_Docking/Docking_1/2AM9_clean*/") + glob.glob("02_Docking/Docking_2/2AM9_clean*/")
# On nettoie les noms et on enlève les doublons avec set()
mutants = list(set([os.path.basename(os.path.normpath(d)) for d in dossiers]))

# ==========================================
# 1. Traitement du Wild-Type
# ==========================================
wt_path = get_path(wt_name)
print(f"\n⚡ Préparation du Wild-Type ({wt_name}) dans {wt_path}...")

# Sécurité : Si le PDB de la protéine n'est pas dans le dossier, on le copie depuis la racine
if not os.path.exists(f"{wt_path}/prot.pdb"):
    os.system(f"cp {wt_name}.pdb {wt_path}/prot.pdb 2>/dev/null")

# OpenBabel + PyMOL
os.system(f"obabel -ipdbqt {wt_path}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {wt_path}/ligand_brut.pdb 2>/dev/null")
os.system(f"pymol -c -q -d 'load {wt_path}/ligand_brut.pdb; h_add; save {wt_path}/ligand_H.pdb' >/dev/null 2>&1")

# ==========================================
# 2. Topologie Centrale ACPYPE
# ==========================================
print("🧪 Génération de la topologie centrale ACPYPE...")
os.makedirs("00_Ligand_Topo", exist_ok=True)
os.chdir("00_Ligand_Topo")
os.system(f"acpype -i ../{wt_path}/ligand_H.pdb -c gas -n 0 > /dev/null 2>&1")
os.system("mv ligand_H.acpype/* . 2>/dev/null")
os.system("rm -rf ligand_H.acpype")
os.chdir("..")

# Assemblage du WT
os.system(f"grep -v 'END' {wt_path}/prot.pdb > {wt_path}/complexe.pdb 2>/dev/null")
os.system(f"grep '^ATOM\\|^HETATM' {wt_path}/ligand_H.pdb >> {wt_path}/complexe.pdb 2>/dev/null")
os.system(f"echo 'END' >> {wt_path}/complexe.pdb")

# ==========================================
# 3. Traitement des Mutants
# ==========================================
for mutant in sorted(mutants):
    if mutant == wt_name:
        continue
        
    path = get_path(mutant)
    print(f"\n🧬 Traitement : {mutant}")
    print(f"   📂 Dossier source : {path}")
    
    # Sécurité PDB
    if not os.path.exists(f"{path}/prot.pdb"):
        os.system(f"cp {mutant}.pdb {path}/prot.pdb 2>/dev/null")
        
    # Aiguillage Cross-Docking vs Extraction normale
    if mutant in bad_mutants:
        print("   -> 🚨 Pose ratée : Cross-Docking (Copie du WT)")
        os.system(f"cp {wt_path}/ligand_H.pdb {path}/ligand_H.pdb 2>/dev/null")
    else:
        print("   -> ✅ Extraction de la pose native + PyMOL")
        os.system(f"obabel -ipdbqt {path}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {path}/ligand_brut.pdb 2>/dev/null")
        os.system(f"pymol -c -q -d 'load {path}/ligand_brut.pdb; h_add; save {path}/ligand_H.pdb' >/dev/null 2>&1")

    # Assemblage
    os.system(f"grep -v 'END' {path}/prot.pdb > {path}/complexe.pdb 2>/dev/null")
    os.system(f"grep '^ATOM\\|^HETATM' {path}/ligand_H.pdb >> {path}/complexe.pdb 2>/dev/null")
    os.system(f"echo 'END' >> {path}/complexe.pdb")

# ==========================================
# 4. Nettoyage
# ==========================================
os.system("rm -f 02_Docking/*/*/ligand_brut.pdb")
print("\n🎉 TERMINE ! Tous tes 'complexe.pdb' sont générés et rangés dans leurs dossiers respectifs.")