for dossier in 2AM9_clean*/; do
    
    # Récupère le nom du mutant
    mutant=$(basename "$dossier")
    echo "⚙️ Docking de $mutant..."
    
    # La commande Vina avec ton config.txt + forçage des 20 poses
    vina --config config.txt \
         --receptor "$dossier/${mutant}.pdbqt" \
         --ligand "ligand.pdbqt" \
         --num_modes 20 \
         --energy_range 15 \
         --out "$dossier/${mutant}_resultat.pdbqt" > "$dossier/${mutant}_log.txt"
         
done

echo "🎉 Docking terminé !"