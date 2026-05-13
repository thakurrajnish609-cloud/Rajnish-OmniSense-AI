import tkinter as tk
import subprocess
import os

class SafeGuardMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Rajnish SafeGuard AI v3.0")
        self.root.geometry("450x550")
        self.root.configure(bg="#2c3e50")

        tk.Label(root, text="SENSING & SAFETY HUB", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

        self.add_button("1. Skeleton Monitor (Camera)", self.launch_skeleton, "#27ae60")
        self.add_button("2. WiFi Wall Sensing", self.launch_wifi, "#2980b9")
        self.add_button("3. Smart Glove Analysis", self.launch_glove, "#e67e22")
        self.add_button("4. Frequency Meter (Hz)", self.launch_hz, "#8e44ad")

    def add_button(self, text, command, color):
        tk.Button(self.root, text=text, command=command, font=("Arial", 12, "bold"), 
                  bg=color, fg="white", width=30, height=2).pack(pady=10)

    def launch_skeleton(self):
        subprocess.Popen(["python3", "skeleton_m4.py"])

    def launch_wifi(self):
        subprocess.Popen(["python3", "wifi_wall_detect_v2.py"])

    def launch_glove(self):
        subprocess.Popen(["python3", "smart_glove_final.py"])

    def launch_hz(self):
        subprocess.Popen(["python3", "rajnish_hz_meter.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = SafeGuardMaster(root)
    root.mainloop()
