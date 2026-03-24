#!/bin/bash

# Boucle sur tous les fichiers 2AM9xxx.pdbqt
for prot in 2AM9*.pdbqt; do
    
    # On extrait le nom de base
    basename=$(basename "$prot" .pdbqt)
    
    echo "$basename"
    
    # Vina
    vina --receptor "$prot" --config config.txt --out "${basename}_resultat.pdbqt" > "${basename}_log.txt"
    
    echo "$basename done"

done

echo "End"