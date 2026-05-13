import tkinter as tk
from tkinter import font, messagebox
import os
import subprocess

# आपका सही पाथ
BASE_PATH = "/Users/rajnish/My_AI_Project/"

def run_script(script_name):
    script_path = os.path.join(BASE_PATH, script_name)
    
    # चेक करें कि फाइल मौजूद है या नहीं
    if not os.path.exists(script_path):
        script_path = os.path.expanduser(f"~/My_AI_Project/{script_name}")

    if os.path.exists(script_path):
        print(f"Starting: {script_name}...")
        # subprocess डैशबोर्ड को बिना रोके बैकग्राउंड में स्क्रिप्ट चलाएगा
        subprocess.Popen(["python3", script_path])
    else:
        messagebox.showerror("Error", f"File not found:\n{script_name}")

# UI Design
root = tk.Tk()
root.title("Rajnish OmniSense v7.2")
root.geometry("500x500")
root.configure(bg='#0f172a')

# Fonts
title_font = font.Font(family='Helvetica', size=22, weight='bold')
btn_font = font.Font(family='Helvetica', size=12, weight='bold')

# स्टाइल के लिए एक फंक्शन
def create_btn(text, script):
    return tk.Button(root, text=text, command=lambda: run_script(script),
                     width=35, height=2, font=btn_font, 
                     bg="#e0e0e0", fg="black", activebackground="#38bdf8", 
                     cursor="hand2", bd=2)

# Header
tk.Label(root, text="SENSING & SAFETY HUB", font=title_font, fg="#38bdf8", bg="#0f172a").pack(pady=60)

# Buttons - सिर्फ नंबर 1 और 2 रखे गए हैं
create_btn("🏃 1. SKELETON MONITOR", "OmniSensing_Core2.py").pack(pady=15)
create_btn("🧤 2. SMART GLOVES ANALYSIS", "smart_glove_v3.py").pack(pady=15)

# Footer
tk.Label(root, text="System Status: Online", font=("Helvetica", 10), fg="#94a3b8", bg="#0f172a").pack(side="bottom", pady=40)

print("Dashboard is running with 2 main modules!")
root.mainloop()
