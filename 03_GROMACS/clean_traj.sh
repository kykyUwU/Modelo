#!/bin/bash

for dir in 2AM9_clean*/; do
    echo "========================================"
    echo "Nettoyage visuel pour : $dir"
    cd "$dir" || continue

    if [ -f "md_0_1.tpr" ] && [ -f "md_0_1.trr" ]; then
        # 1. Centrer la protéine et recoller la boîte (1 = Protein, 0 = System)
        echo "--> Centrage dans la boîte..."
        echo -e "1\n0" | gmx trjconv -s md_0_1.tpr -f md_0_1.trr -o traj_centre.xtc -pbc mol -center > /dev/null 2>&1

        # 2. Supprimer la rotation/translation (4 = Backbone, 0 = System)
        echo "--> Lissage des mouvements..."
        echo -e "4\n0" | gmx trjconv -s md_0_1.tpr -f traj_centre.xtc -o traj_fixe.xtc -fit rot+trans > /dev/null 2>&1

        echo "✅ Trajectoire propre générée : traj_fixe.xtc"
    else
        echo "❌ Fichiers MD introuvables. Le calcul est-il terminé ?"
    fi

    cd ..
done

echo "========================================"
echo "Toutes les trajectoires sont prêtes !"
