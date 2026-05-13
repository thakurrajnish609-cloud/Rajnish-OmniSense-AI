import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import numpy as np

class SmartGloveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Engineering Project: Smart Glove Dashboard")
        self.master.geometry("600x500")

        # डेटा स्टोर करने के लिए लिस्ट
        self.data_history = list(np.zeros(20))

        # GUI Components
        tk.Label(self.master, text="Real-time Voltage Simulation", font=("Arial", 16)).pack(pady=10)

        # ग्राफ बनाना
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 1)
        self.line, = self.ax.plot(self.data_history, color='orange', lw=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        self.status_label = tk.Label(self.master, text="System: Monitoring...", font=("Arial", 14), fg="blue")
        self.status_label.pack(pady=20)

        # ग्राफ अपडेट करना शुरू करें
        self.update_graph()

    def update_graph(self):
        # नया रैंडम डेटा (सिमुलेशन)
        new_val = random.uniform(0.1, 0.9)
        self.data_history.append(new_val)
        self.data_history.pop(0)

        # ग्राफ की लाइन अपडेट करना
        self.line.set_ydata(self.data_history)
        
        # स्टेटस चेक करना
        if new_val > 0.7:
            self.status_label.config(text=f"⚠️ DANGER DETECTED: {new_val:.2f}", fg="red")
        else:
            self.status_label.config(text=f"✅ SYSTEM SAFE: {new_val:.2f}", fg="green")

        self.canvas.draw()
        # हर 500ms (आधे सेकंड) में खुद को कॉल करेगा
        self.master.after(500, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartGloveApp(root)
    root.mainloop()