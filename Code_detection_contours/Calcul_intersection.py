# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 03:06:36 2024

@author: luk-m
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


img1 = cv2.imread('bas02.png')
img2 = cv2.imread('haut02.png')

# Convertion en niveau de gris
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Application du flou gaussien
blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)
blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)

# Detection des contours à l'aide de l'algo de Canny
edges1 = cv2.Canny(blur1, 50, 150)
edges2 = cv2.Canny(blur2, 50, 150)

# Extraction des valeurs des contours dans une liste
contours1, _ = cv2.findContours(edges1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



# Redimensionement de l'image 1 à la taille de l'image 2
img1_resized = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
gray1_resized = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)

# Permet de créer un masque des deux images 
mask1 = np.zeros_like(gray1_resized)
mask2 = np.zeros_like(gray2)

# Permet de tracer les contours sauvegarder
cv2.drawContours(mask1, contours1, -1, (255), thickness=cv2.FILLED)
cv2.drawContours(mask2, contours2, -1, (255), thickness=cv2.FILLED)

# Recherche d'intersection (par un ET logique entre les deux masques), on a un masque en sortie
intersection = cv2.bitwise_and(mask1, mask2)


# Creation de l'image de superposition avec la surface d'intersection en jaune
output = cv2.addWeighted(img1_resized, 0.5, img2, 0.5, 0)
output[intersection > 0] = [0, 255, 255]  # Set intersection area to yellow

# Recherche des contours d'intersection 
intersection_contours, _ = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Calcul des aires d'intersection
areas = [cv2.contourArea(cnt) for cnt in intersection_contours]

# Affichage des valeurs des surfaces
areas_dict = {f'Intersection {i+1}': area for i, area in enumerate(areas)}

# Affichage des valeurs des surfaces
for i, cnt in enumerate(intersection_contours):
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(output, f'{areas_dict[f"Intersection {i+1}"]:.1f}', (cX, cY), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)


# Affichage des résultats
plt.figure(figsize=(10, 10))
plt.subplot(1, 3, 1)
plt.title('Image 1')
plt.imshow(cv2.cvtColor(img1_resized, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Image 2')
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Mise en évidence des surfaces d\'intersection')
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.tight_layout()
plt.show()


print(areas_dict)

