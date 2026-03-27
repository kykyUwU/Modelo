#!/bin/bash

for dir in 2AM9_*/; do
    echo "========================================"
    echo "Construction du complexe dans : $dir"
    cd "$dir" || continue

    # 1. Réparation de la protéine
    echo "--> Réparation de prot.pdb..."
    pdbfixer prot.pdb --add-atoms=heavy --output=prot_fixed.pdb > /dev/null 2>&1

    # 2. Génération de la topologie de la protéine
    echo "--> Création de prot.gro et topol.top (OPLS-AA / TIP4P)..."
    # L'option -ff oplsaa permet de passer le menu interactif automatiquement
    gmx pdb2gmx -f prot_fixed.pdb -o prot.gro -p topol.top -ignh -ff oplsaa -water tip4p > /dev/null 2>&1

    # 3. Modification de topol.top pour inclure le ligand
    echo "--> Édition de topol.top..."
    # On ajoute l'inclusion du .itp juste avant la section [ system ]
    sed -i '/\[ system \]/i ; Include ligand topology\n#include "../00_Ligand_Topo/DHT.itp"\n' topol.top
    # On ajoute 1 molécule de ligand tout à la fin
    echo "UNL                 1" >> topol.top

    # 4. Fusion des fichiers .gro
    echo "--> Fusion en complexe.gro..."
    cp prot.gro complexe.gro
    
    # Récupération des nombres d'atomes à la ligne 2
    n_prot=$(sed -n '2p' prot.gro)
    n_lig=$(sed -n '2p' ligand.gro)
    n_total=$((n_prot + n_lig))
    
    # Remplacement de la ligne 2 par le total
    sed -i "2s/.*/ $n_total/" complexe.gro
    # Suppression de la dernière ligne (boîte)
    sed -i '$d' complexe.gro
    # Ajout des atomes du ligand (en ignorant les 2 premières lignes et la dernière)
    tail -n +3 ligand.gro | head -n -1 >> complexe.gro
    # Remise de la boîte à la fin
    tail -n 1 prot.gro >> complexe.gro

    echo "✅ Complexe terminé pour $dir"
    cd ..
done

echo "========================================"
echo "🎉 Tous les complexes sont prêts !"
