import pandas as pd

# Chemin complet du fichier CSV
file_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\tableau.csv'  

# Lire le fichier CSV
df = pd.read_csv(file_path)

# Convertir le DataFrame en une liste de listes
data = df.values.tolist()

# Afficher le tableau
print("Tableau complet :")
for row in data:
    print(row)

# Exemple d'accès aux éléments individuels
print("\nAccès aux éléments individuels :")
for i, row in enumerate(data):
    for j, value in enumerate(row):
        print(f"Élément à la ligne {i+1}, colonne {j+1} : {value}")

# Exemple de traitement supplémentaire : modification d'un élément spécifique
# Modifier l'élément à la première ligne, deuxième colonne
data[0][1] = 42.0

print("\nTableau après modification :")
for row in data:
    print(row)
