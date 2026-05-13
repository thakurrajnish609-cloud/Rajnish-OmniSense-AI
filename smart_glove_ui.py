import tkinter as tk
from tkinter import messagebox
import random
import os

def check_device(device_name):
    # Simulated logic
    reading = random.uniform(0.1, 0.9)
    
    if reading > 0.7:
        status = "🛑 DANGER"
        color = "red"
        os.system(f'say "Warning! Danger detected in {device_name}"')
    else:
        status = "✅ SAFE"
        color = "green"
        os.system(f'say "{device_name} is safe"')

    # रिजल्ट अपडेट करना
    result_label.config(text=f"Reading: {reading:.2f}\nStatus: {status}", fg=color)

# मुख्य विंडो सेटअप
root = tk.Tk()
root.title("Smart Glove AI - Control Panel")
root.geometry("400x300")

tk.Label(root, text="Smart Glove Safety Monitor", font=("Arial", 16, "bold")).pack(pady=10)

# बटन बनाना
tk.Button(root, text="Test Charger", command=lambda: check_device("Charger"), width=20).pack(pady=5)
tk.Button(root, text="Test Power Cable", command=lambda: check_device("Power Cable"), width=20).pack(pady=5)
tk.Button(root, text="System Full Scan", command=lambda: check_device("Whole System"), width=20).pack(pady=5)

# रिजल्ट दिखाने की जगह
result_label = tk.Label(root, text="Select a device to test", font=("Arial", 12))
result_label.pack(pady=20)

root.mainloop()