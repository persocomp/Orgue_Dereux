import pandas as pd
import matplotlib.pyplot as plt

# Chemin complet du fichier CSV
file_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\tableau.csv'  

# Lire le fichier CSV
df = pd.read_csv(file_path)

# Supprimer les deux dernières lignes
#df = df[:-2]

# Calculer les valeurs maximales et minimales de la deuxième colonne
max_value = df.iloc[:, 1].max()  # Plus grand nombre dans la deuxième colonne
min_value = df.iloc[:, 1].min()  # Plus petit nombre dans la deuxième colonne

# Soustraire min_value à chaque élément de la colonne des angles
df.iloc[:, 1] = df.iloc[:, 1] - min_value 

# Calculer la longueur totale et la moyenne de r
total_value = abs(max_value) + abs(min_value) 
r_moyen = df.iloc[:, 0].mean()
Total_L = total_value * r_moyen

# Normaliser les angles et ajuster les valeurs
df.iloc[:, 1] = df.iloc[:, 1] / total_value
df.iloc[:, 1] = df.iloc[:, 1] * Total_L

# Convertir le DataFrame en une liste de listes
data = df.values.tolist()

# Afficher le tableau
print("Tableau complet avec Delta_Angle :")
for row in data:
    print(row)

# Exemple d'accès aux éléments individuels
print("\nAccès aux éléments individuels :")
for i, row in enumerate(data):
    for j, value in enumerate(row):
        print(f"Élément à la ligne {i+1}, colonne {j+1} : {value}")

# Création du graphique
plt.figure(figsize=(10, 6))
plt.plot(df.iloc[:, 1], df.iloc[:, 0], 'bo-', markersize=5)  # 'bo-' pour les points en bleu avec des lignes
plt.title('Graphique de la première colonne contre la deuxième colonne')
plt.xlabel('Deuxième colonne (angles)')
plt.ylabel('Première colonne (r)')
plt.grid(True)
plt.axhline(0, color='black', lw=0.5)  # Ligne horizontale à y=0
plt.axvline(0, color='black', lw=0.5)  # Ligne verticale à x=0
plt.show()





# Afficher les résultats
print(f"\nLe plus grand nombre dans la deuxième colonne : {max_value}")
print(f"\nLe plus petit nombre dans la deuxième colonne : {min_value}")
print(f"\nLa moyenne des valeurs de la première colonne (r) : {r_moyen:.2f}")
print(f"\nTotal_L : {Total_L:.2f}")

print("\nTableau après modification :")
for row in data:
    print(row)
