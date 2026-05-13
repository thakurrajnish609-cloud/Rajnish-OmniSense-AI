import time
import random
import datetime

def get_sensor_data():
    return random.uniform(0, 0.08)

def ai_decision_engine(signal_strength):
    if signal_strength > 0.06:
        return "DANGER"
    elif signal_strength > 0.02:
        return "WARNING"
    else:
        return "SAFE"

print("📊 AI System: Logging & Analysis Mode Active...")

try:
    # एक नई फाइल बनाना डेटा सेव करने के लिए
    with open("ai_sensor_logs.csv", "w") as file:
        file.write("Timestamp,Signal_Strength,Decision\n") # Header
        
        while True:
            data = get_sensor_data()
            decision = ai_decision_engine(data)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # डेटा को फाइल में लिखना
            file.write(f"{timestamp},{data:.4f},{decision}\n")
            
            # टर्मिनल पर दिखाना
            icon = "🛑" if decision == "DANGER" else "⚠️" if decision == "WARNING" else "✅"
            print(f"[{timestamp}] {icon} {decision} | Strength: {data:.4f}")
            
            time.sleep(1)
except KeyboardInterrupt:
    print("\n💾 डेटा 'ai_sensor_logs.csv' में सुरक्षित सेव कर दिया गया है।")