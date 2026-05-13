import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter

# फिल्टर सेटिंग: सिर्फ 48Hz से 52Hz (Pure Electricity Range)
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_filter(data, lowcut, highcut, fs):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return lfilter(b, a, data)

FS = 44100
LOW, HIGH = 48.0, 52.0 # जापानी बिजली की फ्रीक्वेंसी पर लॉक

print("🛠️ Project Restarted: Smart Safety Mode Active")
print("तारों के पास ले जाकर चेक करें...")

def callback(indata, frames, time, status):
    filtered = apply_filter(indata[:, 0], LOW, HIGH, FS)
    curr_strength = np.max(np.abs(filtered))
    
    # अगर करंट की ताकत 0.05 से ऊपर जाती है (इसे आप अपनी सुविधा अनुसार बदल सकते हैं)
    if curr_strength > 0.05: 
        print(f"⚠️ DANGER: Live Wire Detected! | {curr_strength:.4f}")
    else:
        # यहाँ सिर्फ नंबर दिखेगा ताकि आप 'Safe' लेवल समझ सकें
        print(f"✅ Scanning... Level: {curr_strength:.4f}", end='\r')

with sd.InputStream(callback=callback, channels=1, samplerate=FS):
    sd.sleep(1000000)