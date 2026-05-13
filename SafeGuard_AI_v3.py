import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import random

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SafeGuardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RAJNISH SafeGuard AI v3.0")
        self.geometry("1000x600")

        # Sidebar for Controls
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="right", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="AI ALERT PANEL", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        # Status Light (Circle)
        self.status_light = tk.Canvas(self.sidebar, width=100, height=100, bg="#2b2b2b", highlightthickness=0)
        self.status_light.pack(pady=10)
        self.circle = self.status_light.create_oval(10, 10, 90, 90, fill="green")

        self.status_text = ctk.CTkLabel(self.sidebar, text="SAFE (0.015 Risk)", text_color="green", font=("Arial", 16))
        self.status_text.pack(pady=5)

        # Buttons
        self.log_btn = ctk.CTkButton(self.sidebar, text="[LOG DATA]", fg_color="green")
        self.log_btn.pack(pady=10, padx=20)

        self.set_btn = ctk.CTkButton(self.sidebar, text="[SETTINGS]")
        self.set_btn.pack(pady=10, padx=20)

        # Main Dashboard Area
        self.main_view = ctk.CTkFrame(self)
        self.main_view.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.header = ctk.CTkLabel(self.main_view, text="LIVE ELECTRICAL RISK ANALYTICS", font=("Arial", 24))
        self.header.pack(pady=10)

        # Frequency Display
        self.freq_label = ctk.CTkLabel(self.main_view, text="PEAK FREQUENCY: 60 Hz", font=("Arial", 40, "bold"), text_color="#00fbff")
        self.freq_label.pack(pady=20)

        # Matplotlib Graph
        self.fig = Figure(figsize=(6, 4), facecolor="#2b2b2b")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1a1a1a")
        self.ax.tick_params(colors='white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_view)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.update_graph()

    def update_graph(self):
        # Simulating Japan Grid Frequency (50-60 Hz)
        base_freq = random.choice([50, 60])
        noise = random.uniform(-1, 1)
        current_freq = base_freq + noise

        # Update Labels
        self.freq_label.configure(text=f"PEAK FREQUENCY: {current_freq:.2f} Hz")
        
        # Change light if noise is high
        if abs(noise) > 0.8:
            self.status_light.itemconfig(self.circle, fill="red")
            self.status_text.configure(text="DANGER DETECTED", text_color="red")
        else:
            self.status_light.itemconfig(self.circle, fill="green")
            self.status_text.configure(text="SAFE (Normal Grid)", text_color="green")

        # Draw Graph
        self.ax.clear()
        x = np.linspace(0, 250, 100)
        y = np.sin(2 * np.pi * current_freq * x / 1000) + np.random.normal(0, 0.1, 100)
        self.ax.plot(x, y, color="#00fbff")
        self.ax.set_ylim(-2, 2)
        
        self.canvas.draw()
        self.after(100, self.update_graph)

if __name__ == "__main__":
    app = SafeGuardApp()
    app.mainloop()