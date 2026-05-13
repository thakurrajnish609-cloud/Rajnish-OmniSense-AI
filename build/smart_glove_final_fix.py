import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

class SmartGloveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Engineering Project")
        self.master.geometry("700x550")
        
        # डेटा लिस्ट
        self.data_history = [0.1] * 20

        # UI
        tk.Label(self.master, text="LIVE SENSOR MONITOR", font=("Arial", 18, "bold")).pack(pady=10)

        # ग्राफ (कलर बदलकर ताकि सफ़ेद न दिखे)
        self.fig = Figure(figsize=(6, 4), facecolor='#D3D3D3') # हल्का ग्रे बैकग्राउंड
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 1.0)
        self.line, = self.ax.plot(self.data_history, color='blue', lw=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(self.master, text="Starting...", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # ज़बरदस्ती अपडेट करना (For M4 Mac)
        self.master.update()
        self.update_graph()

    def update_graph(self):
        new_val = random.uniform(0.1, 0.9)
        self.data_history.append(new_val)
        self.data_history.pop(0)

        self.line.set_ydata(self.data_history)
        
        if new_val > 0.7:
            self.status_label.config(text=f"DANGER: {new_val:.2f}", fg="red")
        else:
            self.status_label.config(text=f"SAFE: {new_val:.2f}", fg="green")

        self.canvas.draw()
        self.master.after(200, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    # वॉर्निंग को रोकने के लिए
    import os
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    app = SmartGloveApp(root)
    root.mainloop()