# -*- coding: utf-8 -*-
"""
@author: luk-m
"""

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import pandas as pd
import math


""" Rappel important
Bob désigne le disque de lecture
Alice désigne le disque de forme
"""

#---------Bloc 1--------------

# ========== 1. Créer la fenêtre tkinter ==========
root = tk.Tk()
root.title("Bob - Jaune à partir du 2e contour")

# ========== 2. Charger l’image en niveaux de gris ==========
image2_path = "Bon.png"
gray_image = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
if gray_image is None:
    raise ValueError("Image 'Bon.png' introuvable.")

# ========== 3. Binarisation + détection de contours ==========
_, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ========== 4. Convertir en couleur et remplir en jaune à partir du 2e contour ==========
output = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
for i, cnt in enumerate(contours):
    if i == 0:
        continue
    cv2.drawContours(output, [cnt], -1, (0, 255, 255), thickness=cv2.FILLED)


print(f"{len(contours)} contour(s) detecte(s), remplissage à partir du 2e.")

# ========== 5. Préparer image pour tkinter ==========
img2_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
img2_pil = Image.fromarray(img2_rgb)
img2_tk = ImageTk.PhotoImage(img2_pil)

# ========== 6. Créer le canvas et afficher l’image ==========
canvas = tk.Canvas(root, width=output.shape[1], height=output.shape[0])
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=img2_tk)
canvas.image = img2_tk

# ========== 7. Gérer le clic utilisateur ==========
centre_point = None
centre_image2 = None
marker = None

def on_click(event):
    global centre_point, marker
    centre_point = (event.x, event.y)
    print(f"OKOKOK Centre cliqué : {centre_point}")
    if marker:
        canvas.delete(marker)
    marker = canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, outline='red', width=2)

canvas.bind("<Button-1>", on_click)

# ========== 8. Lancer la fenêtre ==========
root.mainloop()
centre_image2 = centre_point
if centre_image2 is None:
    raise ValueError("Aucun centre n’a été sélectionné pour Bob.")
print("Centre final sélectionné (Bob) :", centre_image2)

#---------Bloc 2--------------

# === CHARGEMENT DE L'IMAGE BOB POUR TAILLE ===
# === UTILISER L’IMAGE DE BOB AVEC CONTOURS JAUNES (output) ===
bob_image = cv2.imread("Bon.png")
if bob_image is None:
    raise ValueError("Image 'Bon.png' introuvable.")

#Utiliser 'output' (avec jaune) pour la suite des traitements
resized_image2 = output.copy()
bob_shape = resized_image2.shape

# === CHARGEMENT DE L'IMAGE ALICE ===
alice_original = cv2.imread("Bas.png")
if alice_original is None:
    raise ValueError("Image 'Bas.png' introuvable.")

# === Vérification des dimensions d'Alice et Bob ===
print("O Dimensions Bob :", bob_image.shape)
print("O Dimensions Alice :", alice_original.shape)

if bob_image.shape != alice_original.shape:
    print("Les dimensions de Bob et Alice sont différentes. Des ajustements peuvent être nécessaires.")
else:
    print("Bob et Alice ont les mêmes dimensions. Aucun redimensionnement ni adaptation supplémentaire n’est requis.")

# === INITIALISATION ===
seuil_min, seuil_max = 65, 150
selection_points = []
selection_contours = []
centre_image1 = None

def detect_edges(img, thresh1, thresh2):
    g_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(g_image, (5, 5), 0)
    edges = cv2.Canny(blur, thresh1, thresh2)
    return edges

def overlay_mask(image, edges):
    mask = np.zeros_like(image)
    mask[:] = [0, 0, 255]
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask, contours, -1, (0, 255, 0), thickness=cv2.FILLED)
    return cv2.addWeighted(image, 0.4, mask, 0.6, 0), contours

def update_sliders(x):
    global seuil_min, seuil_max
    try:
        seuil_min = cv2.getTrackbarPos('Seuil min', 'Trackbars')
        seuil_max = cv2.getTrackbarPos('Seuil max', 'Trackbars')
        edges = detect_edges(alice_original, seuil_min, seuil_max)
        result, _ = overlay_mask(alice_original, edges)
        cv2.imshow("Aperçu Alice", result)
    except cv2.error as e:
        print(" Erreur sliders. Fenêtre fermée ?", e)

def click_event_alice(event, x, y, flags, param):
    global centre_image1, selection_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if centre_image1 is None:
            centre_image1 = (x, y)
            print(f"O Centre Alice sélectionné : {centre_image1}")
            cv2.circle(param, centre_image1, 6, (255, 0, 0), -1)
        else:
            idx = len(selection_points) + 1
            selection_points.append((x, y))
            cv2.circle(param, (x, y), 10, (255, 255, 0), 2)
            cv2.putText(param, str(idx), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("Contours Alice", param)

cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Seuil min', 'Trackbars', seuil_min, 255, update_sliders)
cv2.createTrackbar('Seuil max', 'Trackbars', seuil_max, 255, update_sliders)
cv2.namedWindow('Aperçu Alice', cv2.WINDOW_NORMAL)
cv2.waitKey(100)

edges = detect_edges(alice_original, seuil_min, seuil_max)
preview, contours_alice = overlay_mask(alice_original.copy(), edges)
cv2.imshow("Aperçu Alice", preview)
cv2.setMouseCallback("Aperçu Alice", click_event_alice, preview.copy())

print("\n Clique sur Alice : CENTRE puis FORMES. (Entrée pour valider)")
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 13 and centre_image1 is not None:
        break
    elif key == 27:
        cv2.destroyAllWindows()
        exit()
cv2.destroyAllWindows()

# === CONTOURS SÉLECTIONNÉS ===
for pt in selection_points:
    for cnt in contours_alice:
        if cv2.pointPolygonTest(cnt, pt, False) >= 0:
            selection_contours.append(cnt)
            break

mask1 = np.zeros_like(cv2.cvtColor(alice_original, cv2.COLOR_BGR2GRAY))
cv2.drawContours(mask1, selection_contours, -1, 255, thickness=cv2.FILLED)

print(f"V Centre Alice : {centre_image1}")
print(f"V {len(selection_contours)} forme(s) sélectionnée(s)")
"""
pixels_par_cm = 73.93
for i, cnt in enumerate(selection_contours, 1):
    area_px = cv2.contourArea(cnt)
    area_cm = area_px / (pixels_par_cm ** 2)
    print(f"    Forme {i} : {area_px:.2f} px² ≈ {area_cm:.2f} cm²")
"""
# Les blocs suivants peuvent être copiés-collés à partir de l'original sans modification
# car ils dépendent de mask1 et centre_image1 mis à jour ici.

#---------Bloc 2.5--------------

# === PARAMÈTRES ===
pas_defini = 0.01                  #à modifier pour augmenter le pas


# === FOND CARRÉ DIAGONALE DE BOB ===
h_bob, w_bob = resized_image2.shape[:2]
diagonal = int(np.ceil(math.sqrt(h_bob**2 + w_bob**2)))
canvas_size = diagonal
center_canvas = (canvas_size // 2, canvas_size // 2)


# === FOND CARRÉ DIAGONALE DE BOB ===
h_bob, w_bob = resized_image2.shape[:2]
diagonal = int(np.ceil(math.sqrt(h_bob**2 + w_bob**2)))
canvas_size = diagonal
center_canvas = (canvas_size // 2, canvas_size // 2)

# === PRÉPARER LE MASQUE BINAIRE D’ALICE (VERT) POUR INTERSECTION ===
mask_alice_vert = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
for cnt in selection_contours:
    cv2.drawContours(mask_alice_vert, [cnt], -1, (0, 255, 0), thickness=cv2.FILLED)

dx_alice = center_canvas[0] - centre_image1[0]
dy_alice = center_canvas[1] - centre_image1[1]
mat_translation_alice = np.float32([[1, 0, dx_alice], [0, 1, dy_alice]])
mask_alice_vert = cv2.warpAffine(mask_alice_vert, mat_translation_alice, (canvas_size, canvas_size))

mask_alice_hsv = cv2.cvtColor(mask_alice_vert, cv2.COLOR_BGR2HSV)
lower_green = np.array([50, 150, 150])
upper_green = np.array([70, 255, 255])
mask_alice_bin = cv2.inRange(mask_alice_hsv, lower_green, upper_green)


# ---------Bloc 3--------------

#---------Bloc 3--------------




# === ALICE CENTRÉE SUR LE FOND ===
dx_alice = center_canvas[0] - centre_image1[0]
dy_alice = center_canvas[1] - centre_image1[1]
mat_translation = np.float32([[1, 0, dx_alice], [0, 1, dy_alice]])
mask1_centered = cv2.warpAffine(mask1, mat_translation, (canvas_size, canvas_size))

# === CRÉER LES MASQUES DE CHAQUE FORME SÉLECTIONNÉE ===
form_masks = []
for cnt in selection_contours:
    mask = np.zeros_like(mask1)
    cv2.drawContours(mask, [cnt], -1, 255, thickness=cv2.FILLED)
    mask_centered = cv2.warpAffine(mask, mat_translation, (canvas_size, canvas_size))
    form_masks.append(mask_centered)

# === PRÉPARATION DES RÉSULTATS EN PIXELS ===
resultats = {f"{i+1}": [] for i in range(len(form_masks))}  # Colonnes : 1, 2, ...
angles = np.arange(0, 360.01, pas_defini)

# === Préparation unique de Bob ===
canvas_bob = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
x_offset = (canvas_size - w_bob) // 2
y_offset = (canvas_size - h_bob) // 2
canvas_bob[y_offset:y_offset+h_bob, x_offset:x_offset+w_bob] = resized_image2

# Calcul du vrai centre cliqué sur Bob dans le canevas
center_bob_canvas = (x_offset + centre_image2[0], y_offset + centre_image2[1])
dx_bob = center_canvas[0] - center_bob_canvas[0]
dy_bob = center_canvas[1] - center_bob_canvas[1]

# Translation unique
mat_translation_bob = np.float32([[1, 0, dx_bob], [0, 1, dy_bob]])
bob_aligned = cv2.warpAffine(canvas_bob, mat_translation_bob, (canvas_size, canvas_size))


# === BOUCLE DE ROTATION + INTERSECTION ===
for angle in angles:
    # --- Créer fond pour Bob ---
    canvas_bob = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
    x_offset = (canvas_size - w_bob) // 2
    y_offset = (canvas_size - h_bob) // 2
    canvas_bob[y_offset:y_offset+h_bob, x_offset:x_offset+w_bob] = resized_image2
    # Rotation de Bob sur place autour du centre_canvas
    rot_mat = cv2.getRotationMatrix2D(center_canvas, angle, 1.0)
    bob_rotated = cv2.warpAffine(bob_aligned, rot_mat, (canvas_size, canvas_size))



    # --- Convertir en HSV pour détecter le jaune avec tolérance ---
    bob_hsv = cv2.cvtColor(bob_rotated, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([25, 150, 150])   # Plage basse du jaune
    upper_yellow = np.array([35, 255, 255])   # Plage haute du jaune
    mask_bob_bin = cv2.inRange(bob_hsv, lower_yellow, upper_yellow)

    # --- Intersection Bob & Alice ---
    mask_intersection = cv2.bitwise_and(mask_bob_bin, mask_alice_bin)
    
# === AFFICHAGE pour vérifier les détections ===
    cv2.imshow("Jaune détecté", mask_bob_bin)
    #cv2.imshow("Intersection", mask_intersection)
    #Obesrvation visuelle de la roation de Bob très utile !!!!!!!-----------------
    #maintenant mise en argument
    #key = cv2.waitKey(0)
    #if key == 27:  # Appuie sur Échap pour quitter en cours de boucle
    #    break


    # --- Compter les pixels bleus par forme sélectionnée ---
    for i, form_mask in enumerate(form_masks):
        intersection_bleue = cv2.bitwise_and(mask_intersection, form_mask)
        pixels_bleus = cv2.countNonZero(intersection_bleue)
        resultats[f"{i+1}"].append(pixels_bleus)

    print(f"O Intersections calculées à {angle:.2f}°")


#  === EXPORT EXCEL (format demandé) ===
df = pd.DataFrame(resultats, index=angles)
df.index.name = "Angle (°)"
df.to_excel("intersections_bob_rotation.xlsx")
print(" Fichier 'intersections_bob_rotation.xlsx' généré avec succès.")





#---------Bloc 3.5--------------
#///////////////////////////




# === BLOC 4 : Affichage des superpositions avec zones BLEUES ===



# === BLOC 4 — Affichage BLEU + superposition de Bob (jaune) sur Alice (vert sélectionné) ===

angles_to_show = [0, 90, 180,220, 245, 260, 270, 300, 310, 330, 345, 360]

for angle in angles_to_show:
    # --- Partir de l'image output jaune (Bob traité) ---
    canvas_bob = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
    
    x_offset = (canvas_size - output.shape[1]) // 2
    y_offset = (canvas_size - output.shape[0]) // 2
    canvas_bob[y_offset:y_offset+output.shape[0], x_offset:x_offset+output.shape[1]] = output

    center_bob_canvas = (x_offset + centre_image2[0], y_offset + centre_image2[1])

    # === Étape 1 : Translation pour centrer Bob ===
    dx_bob = center_canvas[0] - center_bob_canvas[0]
    dy_bob = center_canvas[1] - center_bob_canvas[1]
    mat_translation_bob = np.float32([[1, 0, dx_bob], [0, 1, dy_bob]])
    bob_translated = cv2.warpAffine(canvas_bob, mat_translation_bob, (canvas_size, canvas_size))

    # === Étape 2 : Rotation autour du centre global ===
    rot_mat = cv2.getRotationMatrix2D(center_canvas, angle, 1.0)
    bob_rotated = cv2.warpAffine(bob_translated, rot_mat, (canvas_size, canvas_size))

    # === Créer le masque JAUNE uniquement (Bob) ===
    mask_bob_bin = cv2.inRange(bob_rotated, (0, 255, 255), (0, 255, 255))
    """cv2.imshow("Bob - Jaune détecté", mask_bob_bin)
    cv2.waitKey(1)
"""
    # === Intersection entre Bob (jaune) et Alice (vert) ===
    mask_intersection = cv2.bitwise_and(mask_bob_bin, mask_alice_bin)
    """cv2.imshow("Intersection (bleu)", mask_intersection)
    cv2.waitKey(1)
"""
    # === Créer affichage final ===
    display = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)

    # --- Mettre Alice en vert ---
    display[np.where(mask_alice_bin == 255)] = [0, 255, 0]

    # --- Ajouter Bob en jaune (superposition partielle) ---
    bob_yellow_areas = np.where(mask_bob_bin == 255)
    display[bob_yellow_areas] = [0, 255, 255]

    # --- Ajouter zones BLEUES où intersection ---
    blue_areas = np.where(mask_intersection == 255)
    display[blue_areas] = [255, 0, 0]

    # === Afficher ===
    # === Redimensionner pour affichage (ex : 60 % de taille originale) ===
    scale_percent = 60  # ou 50, 75, etc.
    width = int(display.shape[1] * scale_percent / 100)
    height = int(display.shape[0] * scale_percent / 100)
    resized_display = cv2.resize(display, (width, height), interpolation=cv2.INTER_AREA)

    # === Afficher image redimensionnée ===
    cv2.imshow(f"Bob sur Alice", resized_display)
    cv2.waitKey(0)

cv2.destroyAllWindows()

