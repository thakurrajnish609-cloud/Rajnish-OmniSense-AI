import tkinter as tk
from tkinter import font
import os

# फंक्शन: बटन 1 दबाने पर आपका 'Radar Style' स्केलेटन चलेगा
def launch_skeleton():
    print("Launching OmniSensing Core (Radar Style)...")
    # हमने Python 3.12 और आपकी नई फाइल का नाम यहाँ जोड़ दिया है
    os.system("python3.12 OmniSensing_Core.py")

# GUI बनाना
root = tk.Tk()
root.title("Rajnish OmniSense v7.1")
root.geometry("400x500")
root.configure(bg='#1a237e') # गहरा नीला रंग जैसा आपकी फोटो में है

# फॉन्ट सेटिंग्स
title_font = font.Font(family="Helvetica", size=18, weight="bold")
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# हेडिंग
label = tk.Label(root, text="SENSING & SAFETY HUB", font=title_font, 
                 fg="white", bg="#1a237e", pady=30)
label.pack()

# बटन 1: SKELETON MONITOR (अब यह काम करेगा!)
btn1 = tk.Button(root, text="1. SKELETON MONITOR", width=30, height=2,
                 font=button_font, command=launch_skeleton)
btn1.pack(pady=10)

# बाकी बटन (अभी सिर्फ नाम के लिए, बाद में आप इनमें भी कोड जोड़ सकते हैं)
btn2 = tk.Button(root, text="2. SMART GLOVES ANALYSIS", width=30, height=2, font=button_font)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="3. HEARTBEAT (WIFI)", width=30, height=2, font=button_font)
btn3.pack(pady=10)

btn4 = tk.Button(root, text="4. FALL ALARM SYSTEM", width=30, height=2, font=button_font)
btn4.pack(pady=10)

print("Dashboard is running! Press Button 1 to start sensing.")
root.mainloop()