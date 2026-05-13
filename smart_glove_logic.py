import time
import random

# यह फंक्शन भविष्य में सेंसर से डेटा लेगा, अभी हम इसे 'Fake Data' दे रहे हैं
def get_sensor_data():
    # 0.0 से 0.1 के बीच रैंडम नंबर (सेंसर की नकल)
    return random.uniform(0, 0.08)

def ai_decision_engine(signal_strength):
    if signal_strength > 0.06:
        return "🛑 DANGER: High Voltage!"
    elif signal_strength > 0.02:
        return "⚠️ WARNING: Wire Detected"
    else:
        return "✅ SAFE: No Field"

print("🧠 AI Logic Testing Mode Active...")
print("सेंसर डेटा का इंतज़ार हो रहा है (Simulated)...\n")

try:
    while True:
        # 1. डेटा कलेक्ट करना
        data = get_sensor_data()
        
        # 2. AI का फैसला
        result = ai_decision_engine(data)
        
        # 3. आउटपुट दिखाना
        print(f"Current Signal: {data:.4f} --> Decision: {result}")
        
        time.sleep(1) # हर 1 सेकंड में चेक करेगा
except KeyboardInterrupt:
    print("\nTesting Stopped.")