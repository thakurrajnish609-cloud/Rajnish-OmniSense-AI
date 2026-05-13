import tkinter as tk
import numpy as np
import sounddevice as sd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ==========================================
# प्रोजेक्ट: AI Sound Monitoring System
# मुख्य इंजीनियर: रजनीश ठाकुर (Rajnish Thakur)
# डिवाइस: MacBook Air M4
# ==========================================

class SoundMonitorRajnish:
    def __init__(self, master):
        self.master = master
        self.master.title(f"AI Sound Monitor - Lead Engineer: Rajnish Thakur")
        self.master.geometry("600x500")
        
        # ऑडियो डेटा सेटिंग्स
        self.buffer_size = 100
        self.audio_history = np.zeros(self.buffer_size)

        # ग्राफ का डिज़ाइन
        self.fig = Figure(figsize=(5, 3.5), facecolor='#000000')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#111111')
        self.ax.set_ylim(0, 0.8) 
        self.ax.tick_params(colors='cyan')
        self.ax.set_title("Rajnish's Live Audio Feed", color='cyan', fontsize=12)
        
        # गुलाबी/मैजेंटा रंग की लाइन जो आवाज़ के साथ हिलेगी
        self.line, = self.ax.plot(self.audio_history, color='#ff00ff', lw=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=20)

        # स्टेटस लेबल
        self.status_label = tk.Label(
            master, 
            text="STATUS: LISTENING...", 
            fg="#00ff00", 
            bg="#000000", 
            font=("Courier", 14, "bold")
        )
        self.status_label.pack()

        # माइक्रोफ़ोन शुरू करने की कोशिश
        try:
            self.stream = sd.InputStream(callback=self.audio_callback)
            self.stream.start()
            self.update_plot()
        except Exception as e:
            self.status_label.config(text="MIC ERROR", fg="red")
            print(f"रजनीश, माइक चेक करें: {e}")

    def audio_callback(self, indata, frames, time, status):
        # आवाज़ की तीव्रता (Volume) को नंबर में बदलना
        volume_norm = np.linalg.norm(indata) * 0.1
        self.audio_history = np.roll(self.audio_history, -1)
        self.audio_history[-1] = volume_norm

    def update_plot(self):
        self.line.set_ydata(self.audio_history)
        self.canvas.draw_idle()
        self.master.after(50, self.update_plot)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#000000')
    app = SoundMonitorRajnish(root)
    root.mainloop()