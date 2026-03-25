# Boucle
for prot_pdb in 2AM9_clean*.pdb; do
    
    # Extract Name
    mutant=$(basename "$prot_pdb" .pdb)
    
    #obabel
    obabel -ipdb "$prot_pdb" -opdbqt -O "${mutant}.pdbqt" -xr -p 7.4 --partialcharge gasteiger 2>/dev/null

done