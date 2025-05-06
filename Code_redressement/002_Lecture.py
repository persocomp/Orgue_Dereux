import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import numpy as np

rmax = 1475
# Chemin complet du fichier CSV
file_path2 = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\FormeTetelecture\FormeRectangle.csv'
file_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\Formedemiseenerreur\Passageparzero.csv'
# Lire le fichier CSV
df = pd.read_csv(file_path)
df = df[:-2]  # Supprimer les deux dernières lignes

# Calculs pour surface 1
max_value = df.iloc[:, 1].max()
min_value = df.iloc[:, 1].min()
total_value = abs(max_value) + abs(min_value)
r_moyen = df.iloc[:, 0].mean()
Total_L = 2* r_moyen* np.pi

df.iloc[:, 1] = np.where(df.iloc[:, 1] > 0,np.abs(df.iloc[:, 1] - np.pi) + np.pi,df.iloc[:, 1])
df.iloc[:, 1] = np.where(df.iloc[:, 1] < 0, np.abs(df.iloc[:, 1]), df.iloc[:, 1])

print("dflioc",df.iloc[:,1])
df.iloc[:, 1] = df.iloc[:, 1] * df.iloc[:, 0]
points_surface_1 = [(angle, r) for r, angle in zip(df.iloc[:, 0], df.iloc[:, 1])]
print("pointsurface11111111 ", points_surface_1)
print("Points de la Surface 1 :", points_surface_1)

# Lire la surface 2 (forme à déplacer)
df2 = pd.read_csv(file_path2)
df2 = df2[:-2]
rayons = df2.iloc[:, 0].values
df2.iloc[:, 1] = np.where(df2.iloc[:, 1] > 0,np.abs(df2.iloc[:, 1] - np.pi) + np.pi,df2.iloc[:, 1])
df2.iloc[:, 1] = np.where(df2.iloc[:, 1] < 0, np.abs(df2.iloc[:, 1]), df2.iloc[:, 1])
df2.iloc[:, 1] = df2.iloc[:, 1] * df2.iloc[:, 0]

points_surface_2_base = [(angle, r) for r, angle in zip(df2.iloc[:, 0], df2.iloc[:, 1])]
    #  Conversion des radians en "longueur linéaire"
# FOMRE 3 
points_surface_3_base = [(x , y) for (x, y) in points_surface_2_base]
radian_to_length = Total_L / total_value
decalage = 6.28 * rmax

    #  Appliquer un décalage de 6.28 rad (vers la gauche donc -)
# Appliquer un décalage proportionnel au rayon à chaque point
points_surface_2_base = [(x - (2*np.pi*r), y) for (x, y), r in zip(points_surface_2_base, rayons)]

print("Points de la Surface 2 :", points_surface_2_base)




# Fonction de conversion en polygone
def conversion_polygone(points_surface_1, points_surface_2,points_surface_3_base):
    return Polygon(points_surface_1), Polygon(points_surface_2), Polygon(points_surface_3_base)

# Calcul d'aire d'intersection
def calculAire12(surface_1, surface_2):
    return surface_1.intersection(surface_2).area

def CalculAire13(surface_1,surface_3):
    return surface_1.intersection(surface_3).area    

def calculAire(surface_1, surface_2,surface_3):
    airetot = calculAire12(surface_1, surface_2) + CalculAire13(surface_1,surface_3)
    return airetot

def main():
    x_offset = 0
    step_size = 1
    intersection_areas = []
    x_steps = []
    step_x = 0  


    #  Affichage des formes initiales dans une figure séparée
    surface_1, surface_2_init, surface_3_init = conversion_polygone(points_surface_1, points_surface_2_base,points_surface_3_base)
    plt.figure(figsize=(10, 6))
    x1, y1 = surface_1.exterior.xy
    plt.plot(x1, y1, label='Surface 1', color='blue')
    x2, y2 = surface_2_init.exterior.xy
    plt.plot(x2, y2, label='Surface 2 (initiale)', color='green')
    x3, y3 = surface_3_init.exterior.xy
    plt.plot(x3, y3, label='Surface 3', color='red')

    plt.title("Position initiale des deux surfaces")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show()

    #  Boucle de déplacement
    while step_x <= 2*np.pi:
        # Décaler chaque point vers la droite
        points_surface_2 = [(x + (step_x * r), y) for (x, y), r in zip(points_surface_2_base, rayons)]
        points_surface_3 = [(x + (step_x * r), y) for (x, y), r in zip(points_surface_3_base, rayons)]

        # Polygones + aire
        surface_1, surface_2, surface_3 = conversion_polygone(points_surface_1, points_surface_2, points_surface_3)
        area = calculAire(surface_1, surface_2,surface_3)

        intersection_areas.append(area)
        x_steps.append(step_x)
        #print(f"Position: {step_x}, Aire d'Intersection: {area}")

        x_offset += step_size
        step_x += 0.05  

        

    #  Résultats
    results_df = pd.DataFrame({'step_x': x_steps, 'intersection_area': intersection_areas})
    results_df['step_x'] = (results_df['step_x'])

    print("\nDataFrame des Résultats :")
    print(results_df)

    #  Sauvegarde
    output_csv_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel\results2.csv'
    results_df.to_csv(output_csv_path, index=False)
    print(f"\nCSV enregistré : {output_csv_path}")

    #  Affichage graphique final
    plt.figure(figsize=(10, 5))
    plt.plot(results_df['step_x'], results_df['intersection_area'], marker='o', color='blue')
    plt.title("Variation de la Surface d'Intersection avec le Déplacement de la Forme")
    plt.xlabel("Angle du disque (rad)")
    plt.ylabel("Surface d'Intersection")
    plt.grid()
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.show()

main()
