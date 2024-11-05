import pandas as pd
import os

# Définir les données avec un nombre variable de lignes
data = {
    'X': [1.1, 2.2, 3.3, 4.4],
    'Y': [5.5, 6.6, 7.7, 8.8],
    'R': [9.9, 10.10, 11.11, 12.12],
    'alpha': [13.13, 14.14, 15.15, 16.16]
}

# Convertir les données en DataFrame
df = pd.DataFrame(data)

# Définir le répertoire de destination
directory = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel'  # Remplacez par votre chemin

# Chemin complet du fichier CSV
file_path = os.path.join(directory, 'tableau.csv')

# Créer le fichier CSV
df.to_csv(file_path, index=False)

print(f"Le fichier CSV a été créé avec succès à l'emplacement : {file_path}")
