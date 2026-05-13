import tkinter as tk
from tkinter import messagebox
import time
import random
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Mac Setup
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class SmartGlovePro:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Glove AI - Machine & Human Safety")
        self.master.geometry("1000x900") 
        self.master.configure(bg='#F0F0F0')

        self.data_history = [0.0] * 50
        self.heart_history = [70] * 50 # हार्टबीट का डेटा स्टोर करने के लिए
        self.sampling_interval = 0.5 

        # --- UI Header ---
        tk.Label(master, text="Smart Glove Multi-Safety System", font=("Arial", 18, "bold"), bg='#F0F0F0').pack(pady=10)
        
        self.status_label = tk.Label(master, text="SYSTEM READY", font=("Arial", 22, "bold"), fg="green", bg='#F0F0F0')
        self.status_label.pack(pady=5)

        # --- Dashboard Panel ---
        self.info_frame = tk.Frame(master, bg='#F0F0F0')
        self.info_frame.pack(pady=10)
        
        self.freq_label = tk.Label(self.info_frame, text="Frequency: 0.0 Hz", font=("Arial", 12, "bold"), fg="#5856D6", bg='#F0F0F0')
        self.freq_label.grid(row=0, column=0, padx=20)

        self.prediction_label = tk.Label(self.info_frame, text="AI Status: Analyzing...", font=("Arial", 12, "bold"), fg="#007AFF", bg='#F0F0F0')
        self.prediction_label.grid(row=0, column=1, padx=20)

        # नया हार्टबीट डिस्प्ले
        self.heart_label = tk.Label(self.info_frame, text="Heart Rate: 72 BPM", font=("Arial", 12, "bold"), fg="#FF2D55", bg='#F0F0F0')
        self.heart_label.grid(row=0, column=2, padx=20)

        # --- Graph Setup (दो ग्राफ: एक मशीन के लिए, एक हार्ट के लिए) ---
        self.fig = Figure(figsize=(8, 5), facecolor='#F0F0F0')
        
        # मशीन ग्राफ (Top)
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_ylim(0, 1.2)
        self.ax1.axhline(y=0.8, color='r', linestyle='--', label="Danger")
        self.line1, = self.ax1.plot(self.data_history, color='#007AFF', lw=2, label="Machine Voltage")
        self.ax1.legend(loc='upper right', fontsize=8)

        # हार्टबीट ग्राफ (Bottom)
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.set_ylim(50, 150)
        self.line2, = self.ax2.plot(self.heart_history, color='#FF2D55', lw=2, label="Human Pulse")
        self.ax2.legend(loc='upper right', fontsize=8)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20)

        # --- EXIT BUTTON ---
        self.exit_btn = tk.Button(master, text="EXIT SYSTEM", command=self.master.destroy, 
                                  bg="#FF3B30", fg="white", font=("Arial", 14, "bold"), width=20, height=1)
        self.exit_btn.pack(pady=15)

        self.update_system()

    def update_system(self):
        # 1. मशीन डेटा और अलर्ट्स
        val = random.uniform(0.1, 0.95)
        self.data_history.append(val)
        self.data_history.pop(0)
        self.line1.set_ydata(self.data_history)

        # 2. हार्टबीट डेटा (Simulated)
        heart_val = int(random.uniform(65, 85))
        if val > 0.88: heart_val += random.randint(10, 20) # करंट लगने पर धड़कन बढ़ना
        self.heart_history.append(heart_val)
        self.heart_history.pop(0)
        self.line2.set_ydata(self.heart_history)
        self.heart_label.config(text=f"Heart Rate: {heart_val} BPM")

        self.canvas.draw_idle()

        # 3. वॉइस अलर्ट्स
        if val > 0.88:
            self.status_label.config(text=f"!!! DANGER: VOLTAGE LEAKAGE !!!", fg="red")
            os.system('say "Warning, High Voltage and Heart Rate Alert" &')
        elif heart_val > 110:
            self.status_label.config(text="!!! HEALTH ALERT: HIGH BPM !!!", fg="#FF2D55")
        else:
            self.status_label.config(text=f"SYSTEM STABLE: {val:.2f}", fg="green")

        self.master.after(500, self.update_system)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartGlovePro(root)
    root.mainloop()
