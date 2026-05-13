import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import os

# Mac की वॉर्निंग शांत करने के लिए
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class SmartGloveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("M4 Mac AI Dashboard")
        self.master.geometry("600x450")
        
        # बैकग्राउंड कलर सेट करें ताकि पता चले विंडो काम कर रही है
        self.master.configure(bg='gray')

        self.data_history = [0.0] * 30

        # ग्राफ का सेटअप (सफ़ेद न रख कर ग्रे रखें ताकि अंतर दिखे)
        self.fig = Figure(figsize=(5, 3), facecolor='#EEEEEE')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 1.0)
        self.line, = self.ax.plot(self.data_history, color='red', lw=2)
        
        # Canvas को पैक करना
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.status_label = tk.Label(self.master, text="SYSTEM INITIALIZING...", font=("Arial", 14), bg='gray', fg='white')
        self.status_label.pack(pady=10)

        # पक्का करने के लिए कि विंडो लोड हो गई है
        self.master.update_idletasks()
        self.update_graph()

    def update_graph(self):
        new_val = random.uniform(0.1, 0.9)
        self.data_history.append(new_val)
        self.data_history.pop(0)

        self.line.set_ydata(self.data_history)
        
        # ग्राफ को ज़बरदस्ती फिर से बनाने का आदेश (Force Draw)
        self.canvas.draw_idle() 
        
        if new_val > 0.7:
            self.status_label.config(text=f"DANGER DETECTED: {new_val:.2f}", fg="orange")
        else:
            self.status_label.config(text=f"MONITORING: {new_val:.2f}", fg="lightgreen")

        # 100ms में अपडेट (बहुत तेज़ ताकि Mac इसे इग्नोर न कर सके)
        self.master.after(100, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartGloveApp(root)
    root.mainloop()