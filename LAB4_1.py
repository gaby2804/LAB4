import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal.windows import hamming
from scipy.fftpack import fft
import os
import scipy.stats as stats

file_path = r"C:\Users\Silag\Downloads\LABORATORIO 4\senal_adquirida2.xlsx"
df = pd.read_excel(file_path)

output_dir = os.path.join(os.path.dirname(file_path), "imagenes_fft")
os.makedirs(output_dir, exist_ok=True)

picos = np.array([
    [1.019, 3.272], [1.019, 3.268], [1.019, 3.266], [1.019, 3.220],
    [3.009, 2.980], [3.009, 3.255], [3.009, 3.112], [3.009, 3.258],
    [4.006, 3.069], [4.006, 3.039], [6.001, 2.903], [6.001, 2.859],
    [7.015, 2.906], [7.015, 2.838], [8.014, 3.258], [8.014, 2.858],
    [8.014, 2.835], [10.009, 3.242], [11.005, 3.253], [13.010, 3.191],
    [14.005, 3.253], [16.015, 2.977], [16.015, 3.135], [17.015, 2.968],
    [17.015, 3.256], [18.004, 3.075], [19.016, 2.828], [19.016, 3.006],
    [24.005, 2.828], [25.005, 2.820], [25.005, 2.904], [25.005, 3.034],
    [26.013, 2.806], [26.013, 2.950], [27.007, 3.258], [32.005, 3.088],
    [32.005, 3.261], [32.005, 2.905], [34.011, 2.803], [39.013, 3.252],
    [40.009, 3.254], [42.001, 2.803], [43.014, 3.180], [43.014, 3.029],
    [44.008, 2.907], [51.011, 3.013], [51.011, 3.029], [55.009, 2.922],
    [55.009, 2.878], [55.009, 3.091], [56.008, 2.954], [56.008, 2.848],
])

ventana_tamaño = 52
fs = 2000

medias_fft = []
desviaciones_fft = []
n_muestras = []

for tiempo, _ in picos:
    idx = (np.abs(df['Tiempo'] - tiempo)).idxmin()
    ventana = df['Voltaje'][max(0, idx - ventana_tamaño) : idx + ventana_tamaño]
    
    if len(ventana) < 2:
        continue
    
    ventana_hamming = ventana.values * hamming(len(ventana))
    espectro = np.abs(fft(ventana_hamming))[:len(ventana)//2]
    freqs = np.fft.fftfreq(len(ventana), d=1/fs)[:len(ventana)//2]
    
    media_fft = np.mean(espectro)
    desviacion_fft = np.std(espectro)
    
    medias_fft.append(media_fft)
    desviaciones_fft.append(desviacion_fft)
    n_muestras.append(len(espectro))
    
    plt.figure()
    plt.plot(freqs, espectro)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Amplitud')
    plt.title(f'FFT en t={tiempo:.3f}s')
    plt.grid()
    
    output_path = os.path.join(output_dir, f'FFT_t{tiempo:.3f}.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

medias_fft = np.array(medias_fft)
desviaciones_fft = np.array(desviaciones_fft)
n_muestras = np.array(n_muestras)

print("\nResultados de cada ventana en el dominio de la frecuencia:")
for i, (t, media, std) in enumerate(zip(picos[:, 0], medias_fft, desviaciones_fft)):
    print(f"Tiempo: {t:.3f}s | Media: {media:.3f} | Desviación estándar: {std:.3f}")


n1 = n_muestras[0]  
n2 = n_muestras[1]  

print(f"\nNúmero de muestras por ventana: n1={n1}, n2={n2}")


mu1 = 2.934
mu2 = 2.638
sigma1 = 10.846
sigma2 = 14.175

t_stat = (mu1 - mu2) / np.sqrt((sigma1**2 / n1) + (sigma2**2 / n2))
df = min(n1 - 1, n2 - 1)

alpha_01 = stats.t.ppf(1 - 0.005, df=df)

print(f"\nPrueba de hipótesis con α=0.01:")
print(f"Estadístico t: {t_stat:.5f}")
print(f"Grados de libertad: {df}")
print(f"Valor crítico para α=0.01: ±{alpha_01:.5f}")

if abs(t_stat) > alpha_01:
    print("Rechazamos la hipótesis nula al 1% de significancia: Hay fuerte evidencia de diferencia.")
else:
    print("No se rechaza la hipótesis nula al 1% de significancia: No hay suficiente evidencia.")