#!/bin/bash

# Fichier de paramètres basiques temporaire pour les ions
cat << 'EOF' > ions.mdp
integrator  = steep
emtol       = 1000.0
emstep      = 0.01
nsteps      = 50000
nstlist     = 1
cutoff-scheme = Verlet
ns_type     = grid
coulombtype = cutoff
rcoulomb    = 1.0
rvdw        = 1.0
pbc         = xyz
EOF

for dir in 2AM9_*/; do
    echo "========================================"
    echo "Hydratation et Neutralisation : $dir"
    cd "$dir" || continue

    # 1. Correction de topol.top
    # Supprime l'ancienne inclusion tout en bas
    sed -i '/; Include ligand topology/d' topol.top
    sed -i '|#include "../DHT.itp"|d' topol.top
    
    # Ajoute la nouvelle inclusion juste sous le champ de force
    sed -i '/#include "oplsaa.ff\/forcefield.itp"/a \; Include ligand topology\n#include "../DHT.itp"' topol.top

    # 2. Création de la boîte
    echo "--> Création de la boîte (1 nm)..."
    gmx editconf -f complexe.gro -o complexe_box.gro -c -d 1.0 -bt cubic > /dev/null 2>&1

    # 3. Ajout de l'eau TIP4P
    echo "--> Ajout du solvant TIP4P..."
    gmx solvate -cp complexe_box.gro -cs tip4p.gro -o complexe_solv.gro -p topol.top > /dev/null 2>&1

    # 4. Compilation pour les ions (on utilise le ions.mdp à la racine)
    echo "--> Compilation pour l'ajout des ions..."
    gmx grompp -f ../ions.mdp -c complexe_solv.gro -p topol.top -o ions.tpr -maxwarn 1 > /dev/null 2>&1

    # 5. Injection des ions (en forçant le choix "SOL" automatiquement)
    echo "--> Injection des ions..."
    echo "SOL" | gmx genion -s ions.tpr -o complexe_ions.gro -p topol.top -pname NA -nname CL -neutral > /dev/null 2>&1

    echo "✅ Boîte prête et neutre pour $dir"
    cd ..
done

# Nettoyage du fichier mdp temporaire
rm ions.mdp

echo "========================================"
echo "🎉 Tous les systèmes sont solvatés et neutralisés !"
