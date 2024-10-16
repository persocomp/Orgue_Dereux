from shapely.geometry import Polygon
import matplotlib.pyplot as plt

# surfaces
points_surface_1 = [(0, 0), (4, 0), (4, 4), (0, 4)]
points_surface_2 = [(2, 2), (6, 2), (6, 6), (2, 6)]

# Crée des objets Polygone
surface_1 = Polygon(points_surface_1)
surface_2 = Polygon(points_surface_2)

# Calcule l'intersection des deux surfaces
intersection_surface = surface_1.intersection(surface_2)

# Affiche la surface de l'intersection
print("Surface de l'intersection:", intersection_surface.area)




#Visualisation des surfaces 

x1, y1 = surface_1.exterior.xy
x2, y2 = surface_2.exterior.xy
x_inter, y_inter = intersection_surface.exterior.xy

plt.plot(x1, y1, label='Surface 1')
plt.plot(x2, y2, label='Surface 2', color='red')
plt.plot(x_inter, y_inter, label='Intersection', color='green')

plt.fill(x_inter, y_inter, 'green', alpha=0.5)
plt.legend()
plt.show()
