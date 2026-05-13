import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import csv  # डेटा सेव करने के लिए
from datetime import datetime

class SmartGlovePro:
    def __init__(self, master):
        self.master = master
        self.master.title("AI VoltGuard - Advanced Logging")
        self.master.geometry("700x500")
        
        self.data_history = [0.0] * 50
        
        # CSV फाइल सेटअप (Data Logging)
        self.filename = "voltage_log.csv"
        with open(self.filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Voltage", "Status"])

        # ग्राफ सेटअप
        self.fig = Figure(figsize=(6, 4), facecolor='#121212')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1e1e1e')
        self.ax.tick_params(colors='white')
        self.line, = self.ax.plot(self.data_history, color='#00d1ff', lw=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=20)

        self.info_label = tk.Label(master, text="Initializing...", fg="white", bg="#121212", font=("Arial", 12))
        self.info_label.pack()

        self.update_system()

    def update_system(self):
        val = random.uniform(0.1, 0.9)
        status = "NORMAL" if val < 0.8 else "DANGER"
        timestamp = datetime.now().strftime("%H:%M:%S")

        # डेटा को फाइल में सेव करना
        with open(self.filename, mode='a', newline='') as f:
            csv.writer(f).writerow([timestamp, f"{val:.2f}", status])

        # ग्राफ अपडेट
        self.data_history.append(val)
        self.data_history.pop(0)
        self.line.set_ydata(self.data_history)
        self.canvas.draw_idle()

        self.info_label.config(text=f"Time: {timestamp} | Value: {val:.2f}V | Status: {status}")
        
        self.master.after(500, self.update_system)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#121212')
    app = SmartGlovePro(root)
    root.mainloop()