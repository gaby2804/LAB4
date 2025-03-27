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

![](https://github.com/gaby2804/Informe-Lab-1/blob/main/se%C3%B1al%20emg.jpg)
