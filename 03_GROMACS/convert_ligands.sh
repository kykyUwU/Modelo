#!/bin/bash

# Boucle sur tous les dossiers qui commencent par 2AM9_
for dir in 2AM9_*/; do
    echo "Traitement de : $dir"
    cd "$dir" || continue

    # Vérification de la présence du fichier de docking
    if [ -f "ligand_H.pdb" ]; then
        # Conversion du PDB en GRO sans modifier les coordonnées
        gmx editconf -f ligand_H.pdb -o ligand.gro > /dev/null 2>&1
        echo "--> ligand.gro généré avec succès."
    else
        echo "--> Erreur : ligand_H.pdb introuvable."
    fi

    # Retour à la racine pour passer au dossier suivant
    cd ..
done

echo "Conversion terminée pour tous les dossiers."
