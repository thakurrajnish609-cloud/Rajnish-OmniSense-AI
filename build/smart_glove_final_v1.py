import os
import random
import time

def get_simulated_data():
    return random.uniform(0.01, 0.09)

def ai_brain(data_buffer):
    average_strength = sum(data_buffer) / len(data_buffer)
    if average_strength > 0.07:
        return "CRITICAL DANGER", 95
    elif average_strength > 0.04:
        return "POTENTIAL THREAT", 70
    else:
        return "SYSTEM SAFE", 99

memory = []
danger_count = 0

print("📢 AI Safety System with Voice: Active...")

try:
    while True:
        current_data = get_simulated_data()
        memory.append(current_data)
        if len(memory) > 5:
            memory.pop(0)
            
        status, confidence = ai_brain(memory)
        
        print(f"Signal: {current_data:.4f} | {status} ({confidence}%)")

        # अगर खतरा 90% से ऊपर है, तो लैपटॉप बोलेगा
        if status == "CRITICAL DANGER":
            danger_count += 1
            # MacBook का इन-बिल्ट वॉइस कमांड
            os.system('say "Danger, High Voltage detected"') 
            time.sleep(1) # आवाज़ पूरी होने का इंतज़ार

        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"\n--- Project Session Report ---")
    print(f"कुल खतरे पकड़े गए: {danger_count}")
    print("AI Brain hibernating... अगली बार मिलते हैं!")