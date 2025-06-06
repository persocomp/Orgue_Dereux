import pandas as pd
import numpy as np
from scipy.io.wavfile import write
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# === Paramètres à définir ===
csv_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\CSVHugues\Final2.csv'
frequence_rotation = 55 # En Hz
duree = 5  # En secondes
frequence_echantillonnage = 44100  # En Hz
output_path = r'C:\Users\dejon\OneDrive\master2\ORGUE\Comparaison\WavLukkman\sortie8.wav'

# === Lecture du CSV ===
df = pd.read_csv(csv_path)
angles = df.iloc[:, 0].values  # en degrés
angles = np.deg2rad(angles)    # conversion en radians
amplitudes = df.iloc[:, 1].values

# === Interpolation de l'amplitude selon l'angle ===
interpolateur = interp1d(angles, amplitudes, kind='linear', fill_value="extrapolate")

# === Création du signal temporel ===
nb_echantillons = int(frequence_echantillonnage * duree)
t = np.linspace(0, duree, nb_echantillons)
angle_par_seconde = 2 * np.pi * frequence_rotation
angles_t = np.mod(angle_par_seconde * t, 2 * np.pi)
signal = interpolateur(angles_t)



plt.figure(figsize=(10, 4))
plt.plot(t[:1000], signal[:10000])  # Zoom sur le début (1000 échantillons)
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.title("Signal temporel généré à partir du profil angulaire")
plt.grid(True)
plt.tight_layout()
plt.show()


# Normalisation et conversion en int16 pour le format Wav
signal_normalise = signal / np.max(np.abs(signal))
signal_int16 = np.int16(signal_normalise * 32767)

# Écriture du fichier WAV 
write(output_path, frequence_echantillonnage, signal_int16)
print(f" Fichier WAV généré avec succès : {output_path}")




#  Analyse fréquentielle
N = len(signal_normalise)  # Nombre d'échantillons
yf = fft(signal_normalise)  # FFT du signal
xf = fftfreq(N, 1 / frequence_echantillonnage)  # Axes des fréquences

# On garde uniquement les fréquences positives (spectre réel)
xf_pos = xf[:N // 2]
yf_pos = np.abs(yf[:N // 2])

# Affichage du spectre
plt.figure(figsize=(10, 4))
plt.plot(xf_pos, yf_pos)
plt.title("Spectre fréquentiel du signal")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0, frequence_echantillonnage / 2)  
plt.grid(True)
plt.tight_layout()
plt.show()