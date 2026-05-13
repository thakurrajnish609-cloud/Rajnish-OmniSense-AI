import numpy as np
import sounddevice as sd
import datetime

# सेटिंग्स (जापान के 3-कोर वायर के लिए आपकी रिसर्च के अनुसार)
FS = 44100
LOW_LIMIT = 0.005  # मामूली हलचल
HIGH_LIMIT = 0.05  # असली बिजली का खतरा

print("🚀 Smart Glove Collector: Recording Started...")
print("डेटा 'power_logs.txt' फाइल में सेव हो रहा है।")

def analyze_and_log(indata, frames, time, status):
    # सिग्नल की ताकत मापना
    strength = np.max(np.abs(indata))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    status_msg = ""
    if strength > HIGH_LIMIT:
        status_msg = "🛑 [DANGER]"
    elif strength > LOW_LIMIT:
        status_msg = "⚠️ [CAUTION]"
    else:
        status_msg = "🟢 [SAFE]"

    # टर्मिनल पर दिखाना
    output = f"{timestamp} | {status_msg} | Power: {strength:.6f}"
    print(output, end='\r' if strength <= LOW_LIMIT else '\n')

    # डेटा को फाइल में सेव करना (Logging)
    if strength > LOW_LIMIT: # सिर्फ काम का डेटा सेव करेंगे
        with open("power_logs.txt", "a") as f:
            f.write(output + "\n")

# स्ट्रीम शुरू करना
try:
    with sd.InputStream(callback=analyze_and_log, channels=1, samplerate=FS):
        sd.sleep(1000000)
except KeyboardInterrupt:
    print("\nStopping... डेटा 'power_logs.txt' में सुरक्षित है।")