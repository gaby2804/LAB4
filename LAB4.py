import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

fs = 2000
duration = 60
samples = fs * duration
channel = "Dev3/ai1"

data = []
timestamps = []

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(channel)
    task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

    print(f"Adquiriendo datos de {channel} a {fs} Hz durante {duration} segundos...")
    task.start()

    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            new_data = task.read(number_of_samples_per_channel=fs, timeout=5)
            data.extend(new_data)
            timestamps.extend(np.linspace(time.time() - start_time, time.time() - start_time, len(new_data)))
        except nidaqmx.errors.DaqError as e:
            print(f" Advertencia: {e}")
            break

    task.stop()

# Guardar los datos en un archivo CSV
filename = "senal_adquirida.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tiempo (s)", "Voltaje (V)"])
    for t, v in zip(timestamps, data):
        writer.writerow([t, v])


plt.figure(figsize=(10, 5))
plt.plot(timestamps, data, label="Voltaje (V)", color="b")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title(f"Señal Adquirida de {channel}")
plt.legend()
plt.grid()
plt.show()
