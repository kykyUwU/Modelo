#!/bin/bash

# Vérification des fichiers communs à la racine
for f in DHT.itp ions.mdp minim.mdp nvt.mdp npt.mdp md.mdp; do
    if [ ! -f "$f" ]; then
        echo "Erreur : le fichier $f est introuvable à la racine."
        exit 1
    fi
done

# Boucle sur les dossiers propres
for dir in 2AM9_clean*/; do
    echo "========================================"
    echo "Traitement de : $dir"
    cd "$dir" || continue

    # 1. Préparation des topologies et géométries (si pas déjà fait)
    if [ ! -f "complexe.gro" ]; then
        echo "--> Réparation et topologie protéine..."
        pdbfixer prot.pdb --add-atoms=heavy --output=prot_fixed.pdb > /dev/null 2>&1
        gmx pdb2gmx -f prot_fixed.pdb -o prot.gro -p topol.top -ignh -ff oplsaa -water tip4p > /dev/null 2>&1

        echo "--> Conversion ligand..."
        gmx editconf -f ligand_H.pdb -o ligand.gro > /dev/null 2>&1

        echo "--> Édition de topol.top..."
        # Ajout du ligand juste sous le champ de force
        sed -i '/#include "oplsaa.ff\/forcefield.itp"/a \; Include ligand topology\n#include "../DHT.itp"' topol.top
        echo "UNL                 1" >> topol.top

        echo "--> Fusion en complexe.gro..."
        cp prot.gro complexe.gro
        n_prot=$(sed -n '2p' prot.gro)
        n_lig=$(sed -n '2p' ligand.gro)
        n_total=$((n_prot + n_lig))
        sed -i "2s/.*/ $n_total/" complexe.gro
        sed -i '$d' complexe.gro
        tail -n +3 ligand.gro | head -n -1 >> complexe.gro
        tail -n 1 prot.gro >> complexe.gro
    fi

    # 2. Boîte, Solvatation et Ions (avec 150 mM)
    if [ ! -f "complexe_ions.gro" ]; then
        echo "--> Création boîte et solvatation..."
        gmx editconf -f complexe.gro -o complexe_box.gro -c -d 1.0 -bt cubic > /dev/null 2>&1
        gmx solvate -cp complexe_box.gro -cs tip4p.gro -o complexe_solv.gro -p topol.top > /dev/null 2>&1
        
        echo "--> Ajout des ions (neutralisation + 150 mM NaCl)..."
        gmx grompp -f ../ions.mdp -c complexe_solv.gro -p topol.top -o ions.tpr -maxwarn 1 > /dev/null 2>&1
        echo "SOL" | gmx genion -s ions.tpr -o complexe_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15 > /dev/null 2>&1
    fi

    # 3. Minimisation
    if [ ! -f "em.gro" ]; then
        echo "--> Minimisation de l'énergie..."
        gmx grompp -f ../minim.mdp -c complexe_ions.gro -p topol.top -o em.tpr > /dev/null 2>&1
        gmx mdrun -v -deffnm em > /dev/null 2>&1
    fi

    # 4. Équilibration NVT
    if [ ! -f "nvt.gro" ]; then
        echo "--> Équilibration NVT (Température)..."
        gmx grompp -f ../nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr > /dev/null 2>&1
        gmx mdrun -deffnm nvt > /dev/null 2>&1
    fi

    # 5. Équilibration NPT
    if [ ! -f "npt.gro" ]; then
        echo "--> Équilibration NPT (Pression)..."
        gmx grompp -f ../npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr > /dev/null 2>&1
        gmx mdrun -deffnm npt > /dev/null 2>&1
    fi

    # 6. Production MD (1 ns)
    if [ ! -f "md_0_1.gro" ]; then
        echo "--> Production MD (1 ns)..."
        gmx grompp -f ../md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr > /dev/null 2>&1
        gmx mdrun -deffnm md_0_1 > /dev/null 2>&1
    else
        echo "--> Production MD déjà terminée."
    fi

    cd ..
done

echo "========================================"
echo "Pipeline complet terminé pour tous les dossiers 2AM9_clean_* !"
