import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from scipy.spatial import ConvexHull

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
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        # Créer une figure pour les coordonnées redressées
        self.fig_redressed, self.ax_redressed = plt.subplots()
        self.ax_redressed.set_title('Redressed Coordinates')
        self.ax_redressed.set_xlabel('Theta (radians)')
        self.ax_redressed.set_ylabel('R')

        # Fixer les limites des axes redressés
        self.ax_redressed.set_xlim(0, 1)  # Plage des angles
        self.ax_redressed.set_ylim(0, 1)           # Plage des valeurs de R

    def add_point(self, r, theta):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.points.append((x, y))
        self.ax.plot(x, y, 'bo')  # 'bo' means blue points
        self.ax.annotate(f'({x:.2f}, {y:.2f})', (x, y))
        self.fig.canvas.draw_idle()  # Mettre à jour le canvas
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
        theta_values = np.array([np.arctan2(y, x) for x, y in self.points])

        # Effacer le graphique précédent
        self.ax_redressed.clear()
        self.ax_redressed.set_title('Redressed Coordinates')
        self.ax_redressed.set_xlabel('Theta (radians)')
        self.ax_redressed.set_ylabel('R')

        # Fixer les limites des axes redressés
        self.ax_redressed.set_xlim(0,1)  # Plage des angles
        self.ax_redressed.set_ylim(0, 1)           # Plage des valeurs de R

        # Tracer les graphiques redressés
        for i in range(len(theta_values)):
            self.ax_redressed.plot(theta_values[i], r_values[i], 'ro')  # 'ro' means red points

        # Relier les points avec une ligne
        self.ax_redressed.plot(theta_values, r_values, 'r-')  

        # Calculer et afficher l'aire
        self.calculate_area_redressed(theta_values, r_values)

        self.fig_redressed.canvas.draw_idle()

    def calculate_area_redressed(self, theta, r):
        """Calculer l'aire du polygone en coordonnées redressées."""
        if len(theta) > 2:
            # En utilisant la formule d'aire de polygone
            area = 0.0
            for i in range(len(theta)):
                j = (i + 1) % len(theta)  # Connexion au premier point
                area += r[i] * r[j] * (theta[j] - theta[i])
            area = 0.5 * abs(area)

            if self.area_text:
                self.area_text.remove()

            self.area_text = self.ax_redressed.text(0.05, 0.95, f'Area: {area:.2f}', transform=self.ax_redressed.transAxes, 
                                                     fontsize=12, verticalalignment='top')
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

    def calculate_area(self):
        """Calculer l'aire du polygone en utilisant l'enveloppe convexe"""
        if len(self.points) > 2:
            points = np.array(self.points)
            hull = ConvexHull(points)
            area = hull.volume

            if self.area_text:
                self.area_text.remove()

            self.area_text = self.ax.text(0.05, 0.95, f'Area: {area:.2f}', transform=self.ax.transAxes, 
                                           fontsize=12, verticalalignment='top')
            self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

class PolarPlot:
    def __init__(self, converter):
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.ax.set_title('Polar Coordinates')
        self.points = []  # Points en coordonnées polaires
        self.converter = converter
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.onkey)

        # Fixer les limites des axes polaires
        self.ax.set_ylim(0, 1)  # Limites de R

    def onclick(self, event):
        if event.inaxes:
            r = event.ydata
            theta = event.xdata
            self.points.append((r, theta))
            self.ax.plot(theta, r, 'ro')  # 'ro' means red points
            self.ax.annotate(f'({r:.2f}, {theta:.2f})', (theta, r))
            self.fig.canvas.draw_idle()  # Mettre à jour le canvas
            self.converter.add_point(r, theta)  # Convertir et ajouter au graphique cartésien
            self.draw_polygon()

    def draw_polygon(self):
        """Tracer les segments entre les points en coordonnées polaires."""
        if len(self.points) > 1:
            for i in range(1, len(self.points)):
                line, = self.ax.plot([self.points[i-1][1], self.points[i][1]],
                                     [self.points[i-1][0], self.points[i][0]], 'r-')
            self.fig.canvas.draw_idle()

    def close_polygon(self):
        if len(self.points) > 2:
            # Connecter le dernier point au premier en polaire
            line, = self.ax.plot([self.points[-1][1], self.points[0][1]],
                                 [self.points[-1][0], self.points[0][0]], 'r-')
            self.fig.canvas.draw_idle()

    def onkey(self, event):
        if event.key == 'q':
            plt.close('all')
            root.quit()
        elif event.key == ' ':
            self.close_polygon()
            self.converter.close_polygon()  # Fermer le polygone dans le graphique cartésien

    def show(self):
        plt.show()

# Créez une fenêtre Tkinter pour contrôler la fermeture du programme
root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale

converter = PolarToCartesianConverter()
polar_plot = PolarPlot(converter)

# Afficher les deux graphiques
polar_plot.show()
converter.show()

root.mainloop()
