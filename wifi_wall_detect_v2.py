import os
import time
import subprocess

def get_wifi_signal():
    try:
        # macOS के नए वर्शन के लिए आधुनिक कमांड
        cmd = "wdutil info"
        output = subprocess.check_output(cmd.split()).decode('utf-8')
        
        for line in output.split('\n'):
            # RSSI (Signal Strength) को ढूँढना
            if 'RSSI' in line and ':' in line:
                # 'RSSI : -45 dBm' में से नंबर निकालना
                signal = line.split(':')[1].strip().split(' ')[0]
                return int(signal)
    except Exception as e:
        return None
    return None

print("📡 Wall-Sensing Mode Active (M4 Optimized)...")
print("Monitoring WiFi waves for movement. Press Ctrl+C to stop.")

last_signal = get_wifi_signal()

try:
    while True:
        current_signal = get_wifi_signal()
        
        if current_signal is not None and last_signal is not None:
            diff = abs(current_signal - last_signal)
            
            # अगर सिग्नल में 4 या उससे ज़्यादा का बदलाव है (हलचल का संकेत)
            if diff >= 4:
                print(f"⚠️ MOVEMENT DETECTED BEHIND WALL! Signal Change: {diff}")
                # आवाज़ वाला अलार्म
                os.system('say "Movement detected!" &')
            
            last_signal = current_signal
        
        time.sleep(0.5) # हर आधे सेकंड में चेक करें

except KeyboardInterrupt:
    print("\nSystem Stopped.")