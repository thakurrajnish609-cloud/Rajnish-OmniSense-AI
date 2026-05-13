import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

class SmartGloveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Engineering Project: Smart Glove Dashboard")
        self.master.geometry("700x550")
        self.master.configure(bg='#2c3e50') # डार्क बैकग्राउंड

        # डेटा स्टोर करने के लिए लिस्ट (20 पॉइंट्स)
        self.data_history = [0.0] * 20

        # हैडिंग
        tk.Label(self.master, text="LIVE VOLTAGE MONITORING", font=("Arial", 20, "bold"), 
                 bg='#2c3e50', fg='white').pack(pady=15)

        # ग्राफ का सेटअप
        self.fig = Figure(figsize=(6, 4), facecolor='#ecf0f1')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 1.0)
        self.ax.set_title("Simulated Sensor Input")
        self.ax.grid(True, linestyle='--', alpha=0.6) # ग्रिड लाइन्स
        
        # लाइन का कलर और मोटाई
        self.line, = self.ax.plot(self.data_history, color='#e67e22', lw=3, marker='o')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=10)

        # स्टेटस लेबल
        self.status_label = tk.Label(self.master, text="Initializing AI...", font=("Arial", 16, "bold"), 
                                     bg='#2c3e50', fg='#f1c40f')
        self.status_label.pack(pady=20)

        self.update_graph()

    def update_graph(self):
        # रैंडम डेटा (AI Simulation)
        new_val = random.uniform(0.1, 0.9)
        self.data_history.append(new_val)
        self.data_history.pop(0)

        # ग्राफ अपडेट करना
        self.line.set_ydata(self.data_history)
        
        if new_val > 0.7:
            self.status_label.config(text=f"🛑 DANGER: {new_val:.2f} V", fg="#e74c3c")
        elif new_val > 0.4:
            self.status_label.config(text=f"⚠️ WARNING: {new_val:.2f} V", fg="#f39c12")
        else:
            self.status_label.config(text=f"✅ SAFE: {new_val:.2f} V", fg="#2ecc71")

        self.canvas.draw()
        # 300ms (थोड़ा तेज़ अपडेट)
        self.master.after(300, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartGloveApp(root)
    root.mainloop()