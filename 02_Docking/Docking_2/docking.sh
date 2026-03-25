pymol -c -q -d "load 2AM9_clean/2AM9_clean_resultat.pdbqt, lig; print(cmd.get_coords('lig', 1).mean(axis=0)); quit"

CX=26.566906
CY=2.070909
CZ=4.5342274

# Petite boîte stricte pour empêcher le ligand de fuir
SIZE=20

echo "🎯 Lancement du docking ciblé au chausse-pied..."

# On ne boucle QUE sur tes deux mutants rebelles
for mutant in "2AM9_clean_Q711A" "2AM9_clean_R752A"; do
    
    echo "⚙️ Forçage de $mutant dans la poche..."
    
    vina --receptor "$mutant/${mutant}.pdbqt" \
         --ligand "ligand.pdbqt" \
         --center_x $CX --center_y $CY --center_z $CZ \
         --size_x $SIZE --size_y $SIZE --size_z $SIZE \
         --exhaustiveness 16 \
         --num_modes 20 \
         --energy_range 15 \
         --out "$mutant/${mutant}_resultat.pdbqt" > "$mutant/${mutant}_log.txt"
         
    echo "✅ $mutant terminé !"

done

echo "🎉 Docking ciblé terminé !"