import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib.image as mpimg
import pandas as pd
import os

class PolarToCartesianConverter:
    def __init__(self):
        self.points = []  # Points in Cartesian coordinates
        self.lines = []
        self.data = []  # To store R and Theta values for CSV
        self.fig_redressed, self.ax_redressed = plt.subplots()
        self.ax_redressed.set_title('Redressed Coordinates')
        self.ax_redressed.set_xlabel('Theta (radians)')
        self.ax_redressed.set_ylabel('R')
        self.ax_redressed.set_xlim(-7, 7)  
        self.ax_redressed.set_ylim(-2000, 2000)

    def add_point(self, r, theta):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.points.append((x, y))
        self.data.append((r, theta))  # Save R and Theta for CSV
        self.draw_polygon()
        self.update_redressed_plot()

    def draw_polygon(self):
        for line in self.lines:
            line.remove()
        self.lines.clear()
        if len(self.points) > 1:
            for i in range(1, len(self.points)):
                line, = self.ax_redressed.plot(
                    [self.points[i-1][0], self.points[i][0]],
                    [self.points[i-1][1], self.points[i][1]], 'r-'
                )
                self.lines.append(line)
            self.fig_redressed.canvas.draw_idle()

    def update_redressed_plot(self):
        if len(self.points) == 0:
            return
        r_values = np.array([np.sqrt(x**2 + y**2) for x, y in self.points])
        theta_values = np.array([np.arctan2(y, x) for x, y in self.points])
        self.ax_redressed.clear()
        self.ax_redressed.set_title('Redressed Coordinates')
        self.ax_redressed.set_xlabel('Theta (radians)')
        self.ax_redressed.set_ylabel('R')
        self.ax_redressed.set_xlim(-7, 7)  
        self.ax_redressed.set_ylim(-2000, 2000)  
        for i in range(len(theta_values)):
            self.ax_redressed.plot(theta_values[i], r_values[i], 'ro')
        self.ax_redressed.plot(theta_values, r_values, 'r-')
        self.fig_redressed.canvas.draw_idle()

    def close_polygon(self):
        if len(self.points) > 2:
            r_last = np.sqrt(self.points[-1][0]**2 + self.points[-1][1]**2)
            theta_last = np.arctan2(self.points[-1][1], self.points[-1][0])
            r_first = np.sqrt(self.points[0][0]**2 + self.points[0][1]**2)
            theta_first = np.arctan2(self.points[0][1], self.points[0][0])
            self.ax_redressed.plot([theta_last, theta_first], [r_last, r_first], 'r-')
            self.update_redressed_plot()
            self.save_to_csv()
    
    #Saugarde du fichier. 
    def save_to_csv(self):
        df = pd.DataFrame(self.data, columns=['R', 'Theta'])
        directory = r'C:\Users\dejon\OneDrive\master2\ORGUE\fichier_excel'  #Chemin d'accès et nom du fichier.
        file_path = os.path.join(directory, 'uncentimetre.csv')
        df.to_csv(file_path, index=False)
        print(f"CSV file : {file_path}")

    def show(self):
        plt.show()


class PolarPlot:
    def __init__(self, converter, image_path, resolution_dpi):
        self.converter = converter
        self.image_path = image_path
        self.resolution_dpi = resolution_dpi
        self.img = mpimg.imread(image_path)  #Charger l'image
        self.fig_img, self.ax_img = plt.subplots()
        self.ax_img.imshow(self.img)
        self.ax_img.set_title('Image with Polar Coordinates')
        self.points = []  # Points in polar coordinates
        self.center = None
        self.cid_img = self.fig_img.canvas.mpl_connect('button_press_event', self.onclick_image)
        self.cid_key = self.fig_img.canvas.mpl_connect('key_press_event', self.onkey)

    def onclick_image(self, event):
        if event.inaxes:
            if event.button == 3:  #Click droit pour pouvoir zoomer à l'aude du click gauche
                if self.center is None:
                    self.center = (event.xdata, event.ydata)
                    self.ax_img.plot(self.center[0], self.center[1], 'go')  # Mark center in green
                    self.fig_img.canvas.draw()
                    print(f"Center set at: ({self.center[0]:.2f}, {self.center[1]:.2f})")
                else:
                    x, y = event.xdata, event.ydata
                    self.points.append((x, y))
                    self.ax_img.plot(x, y, 'ro')  # Mark point in red
                    self.fig_img.canvas.draw()
                    self.draw_polygon_image()
                    self.convert_to_polar_and_add_point(x, y)

    #Fonction pour dessiner le polygone. 
    def draw_polygon_image(self):
        if len(self.points) > 1:
            for i in range(1, len(self.points)):
                self.ax_img.plot([self.points[i-1][0], self.points[i][0]],
                                 [self.points[i-1][1], self.points[i][1]], 'r-')
            self.fig_img.canvas.draw_idle()

    #Conversion pour avoir r et théta.
    def convert_to_polar_and_add_point(self, x, y):
        r = np.sqrt((x - self.center[0])**2 + (y - self.center[1])**2)
        theta = np.arctan2(y - self.center[1], x - self.center[0])
        theta_degrees = np.degrees(theta)  # Conversion à degrés
    
    # Normaliser theta pour qu'il soit entre 0 et 2pi radian et retirer les parties négatives.
        if theta_degrees < 0:
            theta_degrees += 360
        theta_degrees = np.deg2rad(theta_degrees)
        self.converter.add_point(r, theta_degrees)


    #Fonction qui sert à fermer le polygone. 
    def close_polygon_image(self):
        if len(self.points) > 2:
            self.ax_img.plot([self.points[-1][0], self.points[0][0]],
                             [self.points[-1][1], self.points[0][1]], 'r-')
            self.fig_img.canvas.draw_idle()
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
            self.converter.update_redressed_plot()

    def show(self):
        plt.show()



root = tk.Tk()
root.withdraw()  
image_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\image_code_test2\1-a6b028fb.png'  # Chemin de l'image
resolution_dpi = 600                                                       # Résolution de l'image
converter = PolarToCartesianConverter()
polar_plot = PolarPlot(converter, image_path, resolution_dpi)
polar_plot.show()
converter.show()
root.mainloop()
