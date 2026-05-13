import tkinter as tk
import numpy as np
import sounddevice as sd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ==========================================
# प्रोजेक्ट: Real-time Frequency (Hz) Analyzer
# मुख्य इंजीनियर: रजनीश ठाकुर (Rajnish Thakur)
# ==========================================

class FrequencyAnalyzerRajnish:
    def __init__(self, master):
        self.master = master
        self.master.title("Rajnish's AI Frequency Meter (Hz)")
        self.master.geometry("700x550")
        
        self.fs = 44100  # Sample Rate (Hz)
        self.chunk_size = 2048 # डेटा का टुकड़ा
        
        # ग्राफ सेटअप (Hz दिखाने के लिए)
        self.fig = Figure(figsize=(6, 4), facecolor='#000000')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#111111')
        self.ax.set_xlim(20, 2000) # इंसानी आवाज़ की मुख्य रेंज
        self.ax.set_ylim(0, 10)
        self.ax.set_xlabel("Frequency (Hz)", color='cyan')
        self.ax.set_ylabel("Intensity", color='cyan')
        self.ax.tick_params(colors='white')
        
        self.line, = self.ax.plot([], [], color='#00ff00', lw=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=10)

        self.hz_label = tk.Label(
            master, text="Peak Frequency: 0 Hz", 
            fg="yellow", bg="#000000", font=("Courier", 16, "bold")
        )
        self.hz_label.pack()

        # माइक्रोफ़ोन शुरू करें
        self.stream = sd.InputStream(
            samplerate=self.fs, channels=1, 
            blocksize=self.chunk_size, callback=self.audio_callback
        )
        self.stream.start()
        self.update_plot()

    def audio_callback(self, indata, frames, time, status):
        # FFT का जादू: आवाज़ की लहरों को Hz में बदलना
        magnitude = np.abs(np.fft.rfft(indata[:, 0]))
        freqs = np.fft.rfftfreq(len(indata[:, 0]), 1/self.fs)
        
        self.plot_data = (freqs, magnitude)
        
        # सबसे ऊंची फ्रीक्वेंसी (Hz) का पता लगाना
        peak_idx = np.argmax(magnitude)
        self.peak_hz = freqs[peak_idx]

    def update_plot(self):
        if hasattr(self, 'plot_data'):
            self.line.set_data(self.plot_data[0], self.plot_data[1])
            self.hz_label.config(text=f"Peak Frequency: {int(self.peak_hz)} Hz")
            self.canvas.draw_idle()
        self.master.after(50, self.update_plot)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#000000')
    app = FrequencyAnalyzerRajnish(root)
    root.mainloop()