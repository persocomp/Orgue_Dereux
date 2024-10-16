import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Fonction pour calculer la distance en pixels entre deux points
def calculate_pixel_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Fonction pour calculer la distance réelle en tenant compte de la résolution
def calculate_real_distance(p1, p2, resolution):
    pixel_distance = calculate_pixel_distance(p1, p2)
    real_distance = pixel_distance / resolution
    real_distance = real_distance * 2.807
    return real_distance

# Charger l'image
image_path = r'C:\Users\dejon\Desktop\Projet_Orgue\orgue_disque_0001.png'  
img = mpimg.imread(image_path)

# Résolution de l'image 
resolution_dpi = 600  # Remplacer par la résolution réelle de votre image en DPI

# Afficher l'image
fig, ax = plt.subplots()
ax.imshow(img)

# Liste pour stocker les points cliqués
points = []

# Fonction de rappel pour les clics de souris
def onclick(event):
    if len(points) < 2:
        x, y = event.xdata, event.ydata
        points.append((x, y))
        ax.plot(x, y, 'ro')  # Marquer le point en rouge
        fig.canvas.draw()
        if len(points) == 2:
            # Tracer une ligne entre les deux points
            ax.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], 'r-')
            fig.canvas.draw()
            # Calculer et afficher la distance en pixels et en unités réelles
            pixel_distance = calculate_pixel_distance(points[0], points[1])
            real_distance = calculate_real_distance(points[0], points[1], resolution_dpi)
            print(f"Distance entre les points: {pixel_distance:.2f} pixels")
            print(f"Distance réelle entre les points: {real_distance:.2f} cm")

# Connecter l'événement de clic de souris à la fonction de rappel
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
