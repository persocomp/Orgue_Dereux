import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import numpy as np


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

# Affiche les points de la surface 1 pour le débogage
print("Points de la Surface 1 :", points_surface_1)

# Points de la surface 2 (rectangle fixe)
rectangle_width = 20000
rectangle_height = 5

# Fonction pour créer des objets Polygone
def conversion_polygone(points_surface_1, points_surface_2):
    surface_1 = Polygon(points_surface_1)
    surface_2 = Polygon(points_surface_2)
    return surface_1, surface_2

# Calcule l'intersection des deux surfaces
def calculAire(surface_1, surface_2):
    intersection_surface = surface_1.intersection(surface_2)
    return intersection_surface.area

def main():
    # Position de départ du rectangle
    x_offset = 1 - rectangle_height
    step_size = 1  # Pas de déplacement en x
    intersection_areas = []
    x_steps = []
    step_x = 0 

    while True:
        # Définir les nouveaux points de surface 2 (rectangle rouge)
        points_surface_2 = [
            (x_offset, 0), 
            (x_offset, rectangle_width), 
            (x_offset + rectangle_height, rectangle_width), 
            (x_offset + rectangle_height, 0)
        ]
        
        # Créer les polygones
        surface_1, surface_2 = conversion_polygone(points_surface_1, points_surface_2)

        # Calculer l'intersection
        area = calculAire(surface_1, surface_2)

        # Enregistrer les résultats
        intersection_areas.append(area)
        x_steps.append(step_x)

        # Affiche l'aire d'intersection à chaque étape
        print(f"Position: {step_x}, Aire d'Intersection: {area}")

        # Avancer le rectangle
        x_offset += step_size
        step_x += 1 

        # Si l'aire d'intersection est nulle, sortir de la boucle
        if area == 0:
            intersection_areas.append(0)  # Ajouter zéro pour la dernière position
            x_steps.append(step_x)         # Enregistrer la position finale
            break

    # Créer un DataFrame à partir des listes
    results_df = pd.DataFrame({
        'step_x': x_steps,
        'intersection_area': intersection_areas
    })

    # Afficher le DataFrame
    print("\nDataFrame des Résultats :")
    print(results_df)

    # Ajouter une variable à toute la colonne step_x
       # Exemple de variable à ajouter
    variable_to_add = min_value  # Exemple de variable à ajouter
    
    results_df['step_x_divided'] = results_df['step_x'] / Total_L
    results_df['step_x_multiplied'] = results_df['step_x_divided'] * total_value
    results_df['step_x_multiplied'] += variable_to_add
        # Appliquer la transformation spécifique aux valeurs de step_x_multiplied
    results_df['step_x_transformed'] = results_df['step_x_multiplied'].apply(
         lambda x: abs(x) if x < 0 else (3.14 if x == 0 else x + 1)
    )

    # Afficher le DataFrame modifié
    print("\nDataFrame des Résultats après ajout :")
    print(results_df)

    # Tracer le graphique
    x1, y1 = surface_1.exterior.xy
    plt.figure(figsize=(8, 8))
    plt.plot(x1, y1, label='Surface 1', color='blue')
    plt.figure(figsize=(10, 5))
    plt.plot(results_df['step_x_multiplied'], results_df['intersection_area'], marker='o', color='blue')
    plt.title("Variation de la Surface d'Intersection avec le Déplacement du Rectangle")
    plt.xlabel("Angle du disque (rad)")
    plt.ylabel("Surface d'Intersection")
    plt.grid()
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.show()

main()
