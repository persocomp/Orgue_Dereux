import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib.image as mpimg 


class PolarToCartesianConverter:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Cartesian Coordinates')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.points = []  # Points en coordonnées cartésiennes
        self.lines = []
        self.area_text = None  # Variable pour le texte de surface

        # Fixer les limites des axes cartésiens
        self.ax.set_xlim(-2000, 2000)
        self.ax.set_ylim(-2000, 2000)

        # Créer une figure pour les coordonnées redressées
        self.fig_redressed, self.ax_redressed = plt.subplots()
        self.ax_redressed.set_title('Redressed Coordinates')
        self.ax_redressed.set_xlabel('Theta (radians)')
        self.ax_redressed.set_ylabel('R')

        # Fixer les limites des axes redressés
        self.ax_redressed.set_xlim(-2000, 2000)  # Plage des angles
        self.ax_redressed.set_ylim(-2000, 2000)  # Plage des valeurs de R
        


    def add_point(self, r, theta):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.points.append((x, y))
        self.ax.plot(x, y, 'bo')  
        self.ax.annotate(f'({x:.2f}, {y:.2f})', (x, y))
        self.fig.canvas.draw_idle()  
        self.draw_polygon()
        self.update_redressed_plot()

    def draw_polygon(self):
        # Supprimer les lignes de polygone existantes
        for line in self.lines:
            line.remove()
        self.lines.clear()

        if len(self.points) > 1:
            # Tracer les lignes entre les points
            for i in range(1, len(self.points)):
                line, = self.ax.plot([self.points[i-1][0], self.points[i][0]],
                                     [self.points[i-1][1], self.points[i][1]], 'r-')
                self.lines.append(line)
            self.fig.canvas.draw_idle()

    def update_redressed_plot(self):
        """Met à jour le graphique des coordonnées redressées."""
        if len(self.points) == 0:
            return
        
        # Extraire les angles et distances des points
        r_values = np.array([np.sqrt(x**2 + y**2) for x, y in self.points])
        theta_values = np.array([np.arctan2(y, x)*np.sqrt(x**2 + y**2) for x, y in self.points])

        # Effacer le graphique précédent
        self.ax_redressed.clear()
        self.ax_redressed.set_title('Redressed Coordinates')
        self.ax_redressed.set_xlabel('Theta (radians)')
        self.ax_redressed.set_ylabel('R')

        # Fixer les limites des axes redressés
        self.ax_redressed.set_xlim(-2000, 2000)  # Plage des angles
        self.ax_redressed.set_ylim(-2000, 2000)  # Plage des valeurs de R

        # Tracer les graphiques redressés
        for i in range(len(theta_values)):
            self.ax_redressed.plot(theta_values[i], r_values[i], 'ro') 

        # Relier les points avec une ligne
        self.ax_redressed.plot(theta_values, r_values, 'r-')  

        self.fig_redressed.canvas.draw_idle()

    

    def close_polygon(self):
        if len(self.points) > 2:
            # Connecter le dernier point au premier dans le graphique cartésien
            line, = self.ax.plot([self.points[-1][0], self.points[0][0]],
                                [self.points[-1][1], self.points[0][1]], 'r-')
            self.lines.append(line)
            self.fig.canvas.draw_idle()
            
            # Récupérer les valeurs r et theta pour le dernier et le premier point
            r_last = np.sqrt(self.points[-1][0]**2 + self.points[-1][1]**2)
            theta_last = np.arctan2(self.points[-1][1], self.points[-1][0])
            
            r_first = np.sqrt(self.points[0][0]**2 + self.points[0][1]**2)
            theta_first = np.arctan2(self.points[0][1], self.points[0][0])
            
            # Connecter le dernier point au premier dans le graphique redressé
            self.ax_redressed.plot([theta_last, theta_first], [r_last, r_first], 'r-')

            # Mettre à jour le graphique redressé
            self.update_redressed_plot()

            # Redessiner la ligne de fermeture
            self.ax_redressed.plot([theta_last, theta_first], [r_last, r_first], 'r-')

    def show(self):
        plt.show()



class PolarPlot:
    def __init__(self, converter, image_path, resolution_dpi):
        self.converter = converter
        self.image_path = image_path
        self.resolution_dpi = resolution_dpi

        # Charger l'image
        self.img = mpimg.imread(image_path)

        # Créer la figure et les axes pour l'image
        self.fig_img, self.ax_img = plt.subplots()
        self.ax_img.imshow(self.img)
        self.ax_img.set_title('Image with Polar Coordinates')
        self.points = []  # Points en coordonnées polaires
        self.center = None

        self.cid_img = self.fig_img.canvas.mpl_connect('button_press_event', self.onclick_image)
        self.cid_key = self.fig_img.canvas.mpl_connect('key_press_event', self.onkey)

    def onclick_image(self, event):
        if event.inaxes:
            if event.button == 3:
                if self.center is None:
                    self.center = (event.xdata, event.ydata)
                    self.ax_img.plot(self.center[0], self.center[1], 'go')  # Marquer le centre en vert
                    self.fig_img.canvas.draw()
                    print(f"Centre défini à: ({self.center[0]:.2f}, {self.center[1]:.2f})")
                else:
                    x, y = event.xdata, event.ydata
                    self.points.append((x, y))
                    self.ax_img.plot(x, y, 'ro')  # Marquer le point en rouge
                    self.fig_img.canvas.draw()
                    self.draw_polygon_image()
                    self.convert_to_polar_and_add_point(x, y)

    def draw_polygon_image(self):
        """Tracer les segments entre les points sur l'image."""
        if len(self.points) > 1:
            for i in range(1, len(self.points)):
                self.ax_img.plot([self.points[i-1][0], self.points[i][0]],
                                 [self.points[i-1][1], self.points[i][1]], 'r-')
            self.fig_img.canvas.draw_idle()

    def convert_to_polar_and_add_point(self, x, y):
        """Convertir les coordonnées (x, y) en coordonnées polaires par rapport au centre et ajouter au graphique cartésien."""
        r = np.sqrt((x - self.center[0])**2 + (y - self.center[1])**2)
        theta = np.arctan2(y - self.center[1], x - self.center[0])
        self.converter.add_point(r, theta)

            
    def close_polygon_image(self):
        if len(self.points) > 2:
            # Connecter le dernier point au premier dans l'image
            self.ax_img.plot([self.points[-1][0], self.points[0][0]],
                             [self.points[-1][1], self.points[0][1]], 'r-')
            self.fig_img.canvas.draw_idle()
            
            # Ajouter les points finaux pour le redressement
            r_last = np.sqrt((self.points[-1][0] - self.center[0])**2 + (self.points[-1][1] - self.center[1])**2)
            theta_last = np.arctan2(self.points[-1][1] - self.center[1], self.points[-1][0] - self.center[0])
            
            r_first = np.sqrt((self.points[0][0] - self.center[0])**2 + (self.points[0][1] - self.center[1])**2)
            theta_first = np.arctan2(self.points[0][1] - self.center[1], self.points[0][0] - self.center[0])
            
            self.converter.add_point(r_last, theta_last)
            self.converter.add_point(r_first, theta_first)
            
            self.converter.close_polygon()


    def onkey(self, event):
        if event.key == 'enter':
            self.converter.close_polygon()
            self.close_polygon_image()
            self.converter.calculate_area()
            self.converter.update_redressed_plot()

    def show(self):
        plt.show()


# Créez une fenêtre Tkinter pour contrôler la fermeture du programme
root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale

image_path = r'C:\Users\dejon\Desktop\Projet_Orgue\orgue_disque_0001.png'  # Remplacer par le chemin de votre image
resolution_dpi = 600  # Résolution de l'image en DPI

converter = PolarToCartesianConverter()
polar_plot = PolarPlot(converter, image_path, resolution_dpi)

# Afficher les deux graphiques
polar_plot.show()
converter.show()

root.mainloop()
