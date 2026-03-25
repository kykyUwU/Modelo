from pymol import cmd

# Charge ton fichier (remplace par le vrai nom)
cmd.load("2AM9.pdb", "prot")

# 1. Garder uniquement la protéine (vire HOH, ions, ligands)
cmd.remove("not polymer")

# 2. Garder B pour 711 et A pour le reste
# On supprime le A de 711 ET le B de tout le reste
cmd.remove("(resi 711 and alt A) or (not resi 711 and alt B)")

# 3. Supprimer les étiquettes A/B pour normaliser
cmd.alter("all", "alt=''")

# 4. Renommer les résidus (ex: META -> MET)
# On ne garde que les 3 premières lettres
cmd.alter("all", "resn=resn[:3]")

# 5. Sauvegarder
cmd.sort()
cmd.save("prot_ready.pdb")

print("✨ Fichier prot_ready.pdb généré avec succès.")