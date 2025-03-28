# Procesamiennto de una señal electromiografica asociada a la fatiga muscular.
## Introducción
La electromiografia (EMG) mide y analiza la actividad electrica de los musculos, la cual es informacion importante en el diagnosticos y monitoreo de diferentes condiciones neuromusculares. Por medio de este laboratorio, se realizo la captura de la señal EMG emitida por el musculo del antebrazo, por medio de la colocacion de electrodos. Posterior a este proceso, se procesaron las señales para detectar cuando se evidenciaba la fatiga muscular, por medio de tecnicas de filtrado, analisis espectral, los cuales permitieron observar la evolucion de la señal en el tiempo.

### Ventana Hamming
La ventana Hamming es una funcion matematica, util para procesar las señales y minimizar las distorsiones causadas por la discontinuidad en los bordes de la señal analizada cuando necesitamos dividirla. La ventana hace que se dismuya el efecto de fuga espectral o perdida de datos, que puede ocurrir cuandio se hacen analisis en subdiviciones establecidas, cuando se aplica esta ventana, lo que sucede con la señal, es que esta es multiplicada en cada punto de la señal por un valor ponderado, haciendo que la transicion de la señal sea mas suave en el trnascurso del tiempo.

### Transformada de fourier
La transformada de fourier (FFT) hace que la señal en el dominio del tiempo tenga la capacidad de pasar al dominio de la frecuencia. Su uso es fundamnetal a la hora de analizar los componentes de frecuencia de la señal, sobretodo cuando se observa su cambio a travez del tiempo o frecuencias dominantes en la señal. La funcion utilizada realiza el calculo de la FFT para que la señal pase del dominio del tiempo al de la frecuencia.

## Adquision de datos
El proceso que se llevo a cabo para adquirir las señales EMG  del musculo del antebrazo fue en primer lugar poner los electrodos en la superficie de los musculos a evaluar. El sistemas de adquisicion que se utilizo fue por medio del DAQ, el cual permitio registrar la actividad electrica arrojada por el musculo durante la contraccio  continua hasta la fatiga. Los electrodos fueron conectados al modulo y al DAQ, por medio de Python se adquirio la señal con una frecuencia de muestreo de 2000 Hz por 60 segundos, se adquirieron 120,000 muestras en total, para capturar adecuadamente la señal sin perder datos importantes de la misma, monitoreando el musculo en tiempo real para corroborar que los datos adquiridos fueran correctos. Todo esto se configuro en el canal analogico Dev3/ai1 y los datos se fuardaon en un archivo CSV para ser procesados.

```pyton
import nidaqmx
import numpy as np
import time
import csv

def adquirir_senal(channel="Dev3/ai1", fs=2000, duration=60, filename="senal_adquirida.csv"):
    samples = fs * duration
    data = []
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel)
        task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        task.start()
        for _ in range(duration):
            data.extend(task.read(number_of_samples_per_channel=fs, timeout=5))
        task.stop()
    np.savetxt(filename, data, delimiter=",")
    return filename
```

## Procesamiento de la señal
Para el procesamiento de la señal, en primer lugar se cargaron los datos, leyendo la señal por medio de senal_adquirida2,xlsx, en donde se vio la siquiente señal EMG. 

![](https://github.com/gaby2804/LAB4/blob/main/SENAL.png)

En la señal se detectaron los picos de la señal, los cuales fueron 52 impulsos significativos, por esta razon se produjeron 52 ventanas alrededor de los picos que se detectaron. El siguiente paso fue realizar los calculos de la FFT para cada ventana y se almacenaron los espectros obtenidos. Ademas, se  hicieron los debidos calculos estadisticos por medio del siguiente codigo:

```pyton
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft

def procesar_senal(filepath="senal_adquirida2.xlsx"):
    df = pd.read_excel(filepath)
    senal = df.values.flatten()
    return senal

def calcular_fft(ventana):
    N = len(ventana)
    fft_result = np.abs(fft(ventana))[:N//2]
    return fft_result
```
Después de realizar los cálculos en el dominio de la frecuencia, se implementó una prueba de hipótesis de dos colas con el siguiente fragmento de código para determinar si los impulsos llegaron a la fatiga, considerando sus medias y desviaciones estándar. Se estableció un nivel de significancia de α = 0.01 con el objetivo de garantizar un alto rigor estadístico y reducir la probabilidad de cometer un error tipo I. La prueba se basa en la distribución t de Student, ideal cuando el tamaño de las muestras es limitado.
```pyton

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

```
Dado que el estadístico de prueba no está en la región crítica, no hay suficiente evidencia para rechazar la hipótesis nula. Es decir, no podemos concluir que se haya alcanzado la fatiga con el nivel de significancia del 1%. 
![](https://github.com/gaby2804/LAB4/blob/main/Estadisticos.PNG)


## Conclusiones

La adquisicion de datos se pudo llevar a cabo de manera efectiva con una frecuencia de muestreo conveniente para el tiempo de fatiga muscular del individuo, dando acceso a uan correcta captacion de la señal EMG. El debido procesamiento de dicha señal permitio evidenciar 52 picos significativos o de interes necesarios para ser analizados, por medio de la aplicacion de la FFT para poder realizar la extraccion de caracteristicas frecuenciales.

Por medio de la implementacion de la transformada de fourier se pudo observar detalladamente la estructura frecuencial de los impulsos adquiridos, de esta manera completar el analisis estadistico con el calculo de la media y desviacion estandar de las ventanas creadas, para lograr caracterizar adecuadamente las variaciones de la señal y ver su comportamiento con un poco mas de profundidad.

El análisis de la señal electromiográfica nos permitió observar en detalle la actividad eléctrica del músculo del antebrazo y detectar los momentos clave de contracción. Sin embargo, los resultados obtenidos sugieren que, dentro del tiempo evaluado, no hubo una diferencia lo suficientemente significativa como para concluir que se alcanzó la fatiga muscular.
### Reequisitos:
- python 3.9
- matplotlib
- nidaqmx
- numpy
- pandas
- scipy
- csv
- time
