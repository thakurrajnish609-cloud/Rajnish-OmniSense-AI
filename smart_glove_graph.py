import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from matplotlib.animation import FuncAnimation

# फिल्टर सेटिंग्स
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_filter(data, lowcut, highcut, fs):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return lfilter(b, a, data)

# ग्लोबल वेरिएबल्स
FS = 44100
LOW, HIGH = 48.0, 52.0
plot_data = np.zeros(1000)

# ग्राफ सेटअप
fig, ax = plt.subplots()
line, = ax.plot(plot_data, color='lime')
ax.set_ylim(-0.1, 0.1) # ग्राफ की ऊंचाई
ax.set_title("Live Electricity Signal (50Hz Filtered)")
ax.set_facecolor('black')

def callback(indata, frames, time, status):
    global plot_data
    filtered = apply_filter(indata[:, 0], LOW, HIGH, FS)
    # ग्राफ के लिए डेटा अपडेट करना
    plot_data = np.roll(plot_data, -len(filtered))
    plot_data[-len(filtered):] = filtered

def update_plot(frame):
    line.set_ydata(plot_data)
    return line,

# स्ट्रीम शुरू करना
with sd.InputStream(callback=callback, channels=1, samplerate=FS):
    ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
    plt.show()