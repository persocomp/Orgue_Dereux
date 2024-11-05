# -*- coding: utf-8 -*-
"""

@author: luk-m
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


image = cv2.imread('Capture01.png')

if image is None:
    print("Erreur: Image non trouvée")
else:
    #Convertion de l'image en niveaux de gris
    g_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Flou gaussien pour réduire le bruit
    FG_image = cv2.GaussianBlur(g_image, (15, 15), 1)

    # algorithme Canny
    edges = cv2.Canny(FG_image, threshold1=65, threshold2=150)
    #edges = cv2.erode(edges,None, iterations=1)
    #edges = cv2.dilate(edges,None, iterations=0)



    #Masque totale rouge
    mask = np.zeros_like(image)
    mask[:] = [0, 0, 255]  # Colorer tout le masque en rouge (RGB)

    # Extraction des valeurs des contours dans une liste
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Colorer l'intérieur des objets détectés en vert
    cv2.drawContours(mask, contours, -1, (0, 255, 0), thickness=cv2.FILLED)

    # /!\Superposerposition du masque coloré sur l'image originale
    result = cv2.addWeighted(image, 0.4, mask, 0.6, 0)

    # Afficher l'image originale, le masque et le résultat final
    plt.figure(figsize=(10, 5))
    
    # Image originale
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Image originale")
    plt.axis("off")
    
    # Image avec contours détectés
    plt.subplot(1, 3, 2)
    plt.imshow(edges, cmap='gray')
    plt.title("Contours détectés")
    plt.axis("off")
    
    # Résultat final
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Intérieur vert, extérieur rouge")
    plt.axis("off")
    
    # Afficher les résultats
    plt.show()
