import numpy as np
import matplotlib.pyplot as plt

# Paramètres du polygone
rayon = 1
angle_debut = 0  # en radians
angle_fin = np.pi / 2  # en radians (par exemple, 90 degrés)
nombre_points = 5

# Génération des angles pour les sommets du polygone
angles = np.linspace(angle_debut, angle_fin, nombre_points)

# Coordonnées polaires pour les sommets du polygone
r = rayon
theta = angles

# Conversion des coordonnées polaires en coordonnées cartésiennes
x_poly = r * np.cos(theta)
y_poly = r * np.sin(theta)

# Redresser le polygone pour obtenir une ligne droite
# Nous allons simplement prendre l'angle comme x et r comme y
x_line = theta
y_line = r * np.ones_like(theta)

# Tracé des points du polygone
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(x_poly, y_poly, 'o-', label='Polygone')
plt.scatter(0, 0, color='red', label='Centre du cercle')  # Ajout du centre du cercle
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polygone en coordonnées cartésiennes')
plt.axis('equal')
plt.legend()

# Tracé des points redressés
plt.subplot(1, 2, 2)
plt.plot(x_line, y_line, 'o-', label='Ligne droite redressée')
plt.xlabel('Angle (radians)')
plt.ylabel('Rayon')
plt.title('Polygone redressé en ligne droite')
plt.legend()

plt.show()
