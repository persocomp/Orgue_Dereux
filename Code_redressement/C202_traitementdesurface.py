import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import numpy as np

# Chemin complet du fichier CSV
file_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\tableau.csv'

# Lire le fichier CSV
df = pd.read_csv(file_path)

# Supprimer les deux dernières lignes
df = df[:-2]

# Calculer les valeurs maximales et minimales de la deuxième colonne
max_value = df.iloc[:, 1].max()  # Plus grand nombre dans la deuxième colonne
min_value = df.iloc[:, 1].min()  # Plus petit nombre dans la deuxième colonne

# Soustraire min_value à chaque élément de la colonne des angles
df.iloc[:, 1] = df.iloc[:, 1] - min_value 

# Normaliser et ajuster les valeurs
total_value = abs(max_value) + abs(min_value) 
r_moyen = df.iloc[:, 0].mean()
Total_L = total_value * r_moyen
df.iloc[:, 1] = df.iloc[:, 1] / total_value
df.iloc[:, 1] = df.iloc[:, 1] * Total_L

# Convertir le DataFrame en une liste de points pour la surface 1
points_surface_1 = [(angle, r) for r, angle in zip(df.iloc[:, 0], df.iloc[:, 1])]

# Points de la surface 2 (rectangle fixe)
points_surface_2 = [(25, 0), (25, 3000), (50, 3000), (50, 0)]

# Crée des objets Polygone
surface_1 = Polygon(points_surface_1)
surface_2 = Polygon(points_surface_2)

# Calcule l'intersection des deux surfaces
intersection_surface = surface_1.intersection(surface_2)

# Affiche la surface de l'intersection
print("Surface de l'intersection:", intersection_surface.area)

# Visualisation des surfaces 
x1, y1 = surface_1.exterior.xy
x2, y2 = surface_2.exterior.xy
x_inter, y_inter = intersection_surface.exterior.xy

plt.figure(figsize=(8, 8))
plt.plot(x1, y1, label='Surface 1', color='blue')
plt.plot(x2, y2, label='Surface 2', color='red')
plt.plot(x_inter, y_inter, label='Intersection', color='green')

plt.fill(x_inter, y_inter, 'green', alpha=0.5)
plt.legend()
plt.title("Visualisation des Surfaces et de leur Intersection")
plt.xlabel("Axe X")
plt.ylabel("Axe Y")
plt.grid()
plt.axis('equal')  # Pour garder le même rapport d'aspect
plt.show()
