import random
import time

def get_simulated_data():
    # यह असली दुनिया के शोर (Noise) की नकल करेगा
    return random.uniform(0.01, 0.09)

def ai_brain(data_buffer):
    # पिछले डेटा का औसत (Average) निकालना
    average_strength = sum(data_buffer) / len(data_buffer)
    
    if average_strength > 0.07:
        return "CRITICAL DANGER", 95 # 95% Confidence
    elif average_strength > 0.04:
        return "POTENTIAL THREAT", 70 # 70% Confidence
    else:
        return "SYSTEM SAFE", 99

# डेटा को याद रखने के लिए एक लिस्ट (Buffer)
memory = []

print("🧠 AI Brain Phase: Learning from patterns...")

try:
    while True:
        current_data = get_simulated_data()
        memory.append(current_data)
        
        # सिर्फ पिछले 5 रीडिंग्स को याद रखना
        if len(memory) > 5:
            memory.pop(0)
            
        status, confidence = ai_brain(memory)
        
        print(f"Signal: {current_data:.4f} | Status: {status} ({confidence}% Confidence)")
        time.sleep(0.8)
except KeyboardInterrupt:
    print("\nAI Brain hibernating...")