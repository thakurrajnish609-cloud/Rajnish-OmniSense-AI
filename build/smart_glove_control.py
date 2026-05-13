import os
import time
import random

def ai_engine(val):
    if val > 0.8:
        return "🛑 CRITICAL DANGER"
    elif val > 0.5:
        return "⚠️ WARNING"
    else:
        return "✅ SAFE"

print("--- Smart Glove: Manual Testing Mode ---")
print("1. Test Charger")
print("2. Test Power Cable")
print("3. System Scan")

choice = input("Enter choice (1-3): ")

if choice == '1':
    reading = random.uniform(0.1, 0.4)
elif choice == '2':
    reading = random.uniform(0.5, 0.9)
else:
    reading = random.uniform(0.0, 0.2)

status = ai_engine(reading)
print(f"\nFinal Reading: {reading:.2f}")
print(f"Status: {status}")

if "DANGER" in status:
    os.system('say "Danger detected in the cable"')
else:
    os.system('say "System is safe"')