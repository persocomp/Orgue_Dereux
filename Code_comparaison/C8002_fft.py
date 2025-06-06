import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq

def load_wav(file):
    rate, data = wavfile.read(file)
    if data.ndim > 1:  # Stéréo → Mono
        data = data.mean(axis=1)
    return rate, data

def compute_fft(rate, data):
    N = len(data)
    yf = fft(data)
    xf = fftfreq(N, 1 / rate)
    magnitude = 2.0/N * np.abs(yf[:N//2])
    freqs = xf[:N//2]
    return freqs, magnitude

def plot_comparison(freqs_list, mags_list, labels):
    plt.figure(figsize=(14, 7))
    colors = ['b', 'g', 'r']
    for freqs, mags, label, color in zip(freqs_list, mags_list, labels, colors):
        plt.semilogx(freqs, mags, label=label, color=color)
    plt.axvline(20, color='gray', linestyle='--', label='Limite audible (20 Hz)')
    plt.axvline(20000, color='gray', linestyle='--', label='Limite audible (20 kHz)')
    plt.title("Comparaison fréquentielle des trois fichiers .wav")
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def is_inaudible(freqs, magnitudes, threshold=0.01):
    mask = (freqs >= 20) & (freqs <= 20000)
    audible = magnitudes[mask] > threshold
    return not np.any(audible)

def plot_abs_diff_two_graphs(freqs, mag_ref, mag_1, mag_2, label_1, label_2):
    plt.figure(figsize=(12, 5))
    diff_1 = np.abs(mag_ref - mag_1)
    plt.semilogx(freqs, diff_1, label=f"Différence absolue |Hugues - {label_1}|", color='blue')
    plt.axvline(20, color='gray', linestyle='--')
    plt.axvline(20000, color='gray', linestyle='--')
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Amplitude différence absolue")
    plt.title(f"Différence spectrale absolue entre Hugues et {label_1}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 5))
    diff_2 = np.abs(mag_ref - mag_2)
    plt.semilogx(freqs, diff_2, label=f"Différence absolue |Hugues - {label_2}|", color='green')
    plt.axvline(20, color='gray', linestyle='--')
    plt.axvline(20000, color='gray', linestyle='--')
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Amplitude différence absolue")
    plt.title(f"Différence spectrale absolue entre Hugues et {label_2}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_abs_diff_pierre_lukkman(freqs, mag_pierre, mag_lukkman):
    plt.figure(figsize=(12, 5))
    diff = np.abs(mag_pierre - mag_lukkman)
    plt.semilogx(freqs, diff, label="|Pierre - Lukkman|", color='magenta')
    plt.axvline(20, color='gray', linestyle='--')
    plt.axvline(20000, color='gray', linestyle='--')
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Amplitude différence absolue")
    plt.title("Différence spectrale absolue entre Pierre et Lukkman")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



# Chargement des fichiers
rate1, data1 = load_wav(r"C:\Users\dejon\OneDrive\master2\ORGUE\Comparaison\WavHugues\sortie4.wav")
rate2, data2 = load_wav(r"C:\Users\dejon\OneDrive\master2\ORGUE\Comparaison\WavLukkman\sortie4.wav")
rate3, data3 = load_wav(r"C:\Users\dejon\OneDrive\master2\ORGUE\Comparaison\WavPierre\sortie4.wav")

# Calcul FFT
freq1, mag1 = compute_fft(rate1, data1)
freq2, mag2 = compute_fft(rate2, data2)
freq3, mag3 = compute_fft(rate3, data3)

# Affichage
plot_comparison(
    [freq1, freq2, freq3],
    [mag1, mag2, mag3],
    ["Fichier 1", "Fichier 2", "Fichier 3"]
)
plot_abs_diff_two_graphs(freq1, mag1, mag2, mag3, "Lukkman", "Pierre")
plot_abs_diff_pierre_lukkman(freq1, mag3, mag2)

# Analyse d’inaudibilité
print("Fichier 1 inaudible :", is_inaudible(freq1, mag1))
print("Fichier 2 inaudible :", is_inaudible(freq2, mag2))
print("Fichier 3 inaudible :", is_inaudible(freq3, mag3))
