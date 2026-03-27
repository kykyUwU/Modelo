import os
import glob

print("🚀 Lancement du Builder V4 (Depuis 03_GROMACS)...")

# --- PARAMÈTRES ---
wt_name = "2AM9_clean"
bad_mutants = ["2AM9_clean_W741A", "2AM9_clean_W741L"]
targeted_mutants = ["2AM9_clean_Q711A", "2AM9_clean_R752A"]

# --- LE SECRET EST ICI : ".." pour remonter d'un dossier ---
base_docking = "../02_Docking"

def get_source_path(mutant):
    if mutant in targeted_mutants:
        return f"{base_docking}/Docking_2/{mutant}"
    else:
        return f"{base_docking}/Docking_1/{mutant}"

# On scanne les dossiers dans l'architecture parent
dossiers = glob.glob(f"{base_docking}/Docking_1/2AM9_clean*/") + glob.glob(f"{base_docking}/Docking_2/2AM9_clean*/")
mutants = list(set([os.path.basename(os.path.normpath(d)) for d in dossiers]))

# Sécurité si le WT n'a pas été capté
if wt_name not in mutants:
    mutants.append(wt_name)

# Fonction intelligente pour retrouver le PDB original de la protéine
def copy_prot(mutant, dest_folder):
    paths_to_check = [
        f"{get_source_path(mutant)}/{mutant}.pdb", # Dans le dossier de docking
        f"{base_docking}/{mutant}.pdb",            # À la racine de 02_Docking
        f"../01_Preparation/{mutant}.pdb"          # Au cas où il serait encore dans la prép
    ]
    for p in paths_to_check:
        if os.path.exists(p):
            os.system(f"cp {p} {dest_folder}/prot.pdb")
            return True
    print(f"   ❌ AVERTISSEMENT : Impossible de trouver le PDB original pour {mutant}")
    return False

# ==========================================
# 1. Traitement du Wild-Type
# ==========================================
print(f"\n⚡ Préparation du Wild-Type ({wt_name})...")
wt_src = get_source_path(wt_name)
os.makedirs(wt_name, exist_ok=True) # Crée le dossier dans 03_GROMACS

copy_prot(wt_name, wt_name)
os.system(f"obabel -ipdbqt {wt_src}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {wt_name}/ligand_brut.pdb 2>/dev/null")
os.system(f"pymol -c -q -d 'load {wt_name}/ligand_brut.pdb; h_add; save {wt_name}/ligand_H.pdb' >/dev/null 2>&1")

# ==========================================
# 2. Topologie Centrale ACPYPE
# ==========================================
print("🧪 Génération de la topologie centrale ACPYPE...")
os.makedirs("00_Ligand_Topo", exist_ok=True)
os.chdir("00_Ligand_Topo")
os.system(f"acpype -i ../{wt_name}/ligand_H.pdb -c gas -n 0 > /dev/null 2>&1")
os.system("mv ligand_H.acpype/* . 2>/dev/null")
os.system("rm -rf ligand_H.acpype")
os.chdir("..")

# Assemblage WT
os.system(f"grep -v 'END' {wt_name}/prot.pdb > {wt_name}/complexe.pdb 2>/dev/null")
os.system(f"grep '^ATOM\\|^HETATM' {wt_name}/ligand_H.pdb >> {wt_name}/complexe.pdb 2>/dev/null")
os.system(f"echo 'END' >> {wt_name}/complexe.pdb")

# ==========================================
# 3. Traitement des Mutants
# ==========================================
for mutant in sorted(mutants):
    if mutant == wt_name:
        continue
        
    src = get_source_path(mutant)
    print(f"\n🧬 Traitement : {mutant}")
    os.makedirs(mutant, exist_ok=True) # Crée le dossier dans 03_GROMACS
    
    copy_prot(mutant, mutant)
        
    if mutant in bad_mutants:
        print("   -> 🚨 Pose ratée : Cross-Docking (Copie du WT)")
        os.system(f"cp {wt_name}/ligand_H.pdb {mutant}/ligand_H.pdb 2>/dev/null")
    else:
        print(f"   -> ✅ Extraction native depuis {src}")
        os.system(f"obabel -ipdbqt {src}/*_resultat.pdbqt -f 1 -l 1 -opdb -O {mutant}/ligand_brut.pdb 2>/dev/null")
        os.system(f"pymol -c -q -d 'load {mutant}/ligand_brut.pdb; h_add; save {mutant}/ligand_H.pdb' >/dev/null 2>&1")

    # Assemblage
    os.system(f"grep -v 'END' {mutant}/prot.pdb > {mutant}/complexe.pdb 2>/dev/null")
    os.system(f"grep '^ATOM\\|^HETATM' {mutant}/ligand_H.pdb >> {mutant}/complexe.pdb 2>/dev/null")
    os.system(f"echo 'END' >> {mutant}/complexe.pdb")

# ==========================================
# 4. Nettoyage
# ==========================================
os.system("rm -f */ligand_brut.pdb")
print("\n🎉 TERMINE ! Tous tes dossiers sont créés proprement dans 03_GROMACS.")