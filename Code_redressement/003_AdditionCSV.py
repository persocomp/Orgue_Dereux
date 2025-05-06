import csv
import glob

# Récupère tous les fichiers CSV dans le dossier
fichiers_csv = glob.glob(r"C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\addition\*.csv")

colonnes1 = []
somme_col2 = []

for i, fichier in enumerate(fichiers_csv):
    with open(fichier, newline='', encoding='utf-8') as f:
        lecteur = csv.reader(f)
        next(lecteur)  

        for j, ligne in enumerate(lecteur):
            if i == 0:
                # Première passe : on initialise les listes
                colonnes1.append(ligne[0])
                somme_col2.append(float(ligne[1]))
            else:
                if ligne[0] != colonnes1[j]:
                    raise ValueError(f"Les colonnes 1 ne correspondent pas à la ligne {j+2} du fichier {fichier}")
                somme_col2[j] += float(ligne[1])

# Écriture du fichier résultat
chemin_resultat = r"C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\addition\resultat.csv"
with open(chemin_resultat, "w", newline='', encoding='utf-8') as f:

    writer = csv.writer(f)
    writer.writerow(["Nom", "Somme"]) 
    for val1, val2 in zip(colonnes1, somme_col2):
        writer.writerow([val1, val2])

print("Fichier 'resultat.csv' généré avec succès.")
