from shapely.geometry import Polygon
import matplotlib.pyplot as plt
aire = 10
# surfaces


# Crée des objets Polygone
def conversion_polygone(points_surface_1,points_surface_2):
    surface_1 = Polygon(points_surface_1)
    surface_2 = Polygon(points_surface_2)
    return surface_1 , surface_2
# Calcule l'intersection des deux surfaces

def calculAire(surface_1,surface_2):
    intersection_surface = surface_1.intersection(surface_2)
    # Affiche la surface de l'intersection
    print("Surface de l'intersection:", intersection_surface.area)
    #visualisation(intersection_surface,surface_1,surface_2)
    return intersection_surface.area

def update_surface(points_surface_1,points_surface_2):
    new_surface_1 , new_surface_2 = conversion_polygone(points_surface_1,points_surface_2)

def cinematique (points_surface_2):
    points_surface_2 = [(x - 1, y) for (x, y) in points_surface_2]
    print (points_surface_2)
    return points_surface_2

#Visualisation des surfaces 
def visualisation (intersection_surface,surface_1,surface_2):
    x1, y1 = surface_1.exterior.xy
    x2, y2 = surface_2.exterior.xy
    x_inter, y_inter = intersection_surface.exterior.xy

    plt.plot(x1, y1, label='Surface 1')
    plt.plot(x2, y2, label='Surface 2', color='red')
    plt.plot(x_inter, y_inter, label='Intersection', color='green')

    plt.fill(x_inter, y_inter, 'green', alpha=0.5)
    plt.legend()
    plt.show()

def main():
    points_surface_1 = [(0, 0), (4, 0), (4, 4), (0, 4)]
    points_surface_2 = [(2, 2), (6, 2), (6, 6), (2, 6)]
    while True :
        surface_1,surface_2 = conversion_polygone(points_surface_1,points_surface_2)
        aire = calculAire(surface_1,surface_2)
        if(aire != 0) : 
            points_surface_2 = cinematique (points_surface_2)
        else :
            print("fini!")
            break

main()      