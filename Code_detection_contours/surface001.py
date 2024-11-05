# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 00:44:23 2024

@author: luk-m
"""



import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Charger les images
# Charger les images
image1 = cv2.imread('bas02.png')
image2 = cv2.imread('Haut02.png')


# Fonction pour traiter une image, détecter les contours et appliquer les couleurs
def process_image(image):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Appliquer un flou pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Détecter les contours avec Canny
    edged = cv2.Canny(blurred, 50, 150)
    # Trouver les contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Créer un masque pour les couleurs intérieure et extérieure
    mask = np.zeros_like(image)
    for contour in contours:
        # Remplir l'intérieur du contour en vert
        cv2.drawContours(mask, [contour], -1, (0, 255, 0), thickness=cv2.FILLED)
        # Dessiner le contour en rouge
        cv2.drawContours(mask, [contour], -1, (0, 0, 255), thickness=3)
    
    return mask

# Redimensionner les images pour qu'elles aient les mêmes dimensions
height, width = image1.shape[:2]
image2_resized = cv2.resize(image2, (width, height))

# Traiter les deux images après le redimensionnement
processed_image1 = process_image(image1)
processed_image2 = process_image(image2_resized)

# Créer des masques binaires pour les zones vertes
green_mask1 = cv2.inRange(processed_image1, (0, 255, 0), (0, 255, 0)).astype(np.uint8)
green_mask2 = cv2.inRange(processed_image2, (0, 255, 0), (0, 255, 0)).astype(np.uint8)

# Trouver le chevauchement entre les zones vertes dans les deux masques
overlap_mask = cv2.bitwise_and(green_mask1, green_mask2)

# Créer une image blanche pour le fond
white_background = np.ones_like(image1) * 255

# Superposer le traitement des deux images sur un fond blanc
superimposed_image = cv2.addWeighted(processed_image1, 0.5, processed_image2, 0.5, 0)
superimposed_image[np.where(overlap_mask == 255)] = [255, 0, 0]

# Appliquer le fond blanc
white_background[np.where(superimposed_image != 0)] = superimposed_image[np.where(superimposed_image != 0)]

# Détection des contours des zones bleues et calcul de leurs surfaces
contours, _ = cv2.findContours(overlap_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Paramètre de conversion des pixels en mm² (à ajuster selon l'échelle réelle)
pixel_to_mm2 = 1.0  # Remplacez 1.0 par la valeur de conversion appropriée

# Liste pour stocker les informations des surfaces
surface_data = []

# Annoter chaque surface bleue avec uniquement son numéro et ajouter les données au tableau
for i, contour in enumerate(contours):
    # Calcul de la surface en pixels et conversion en mm²
    area_pixels = cv2.contourArea(contour)
    area_mm2 = area_pixels * pixel_to_mm2
    
    # Stocker les informations dans le tableau
    surface_data.append({"Surface ID": i + 1, "Surface Area (mm²)": area_mm2})

    # Calcul du centre du contour pour placer le numéro
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = contour[0][0]
    
    # Annoter l'image avec le numéro de la surface
    text = f"{i+1}"
    cv2.putText(white_background, text, (cX - 10, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Convertir les données en DataFrame pour affichage
surface_df = pd.DataFrame(surface_data)

# Afficher l'image annotée avec fond blanc
plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(white_background, cv2.COLOR_BGR2RGB))
plt.title("Image Superposée avec Numéros des Surfaces Bleues (Fond Blanc)")
plt.axis("off")
plt.show()

# Afficher le tableau des surfaces
print("Surface Area Summary:")
print(surface_df)
