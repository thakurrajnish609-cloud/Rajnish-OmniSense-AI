# Rajnish-OmniSense-AI 🛡️🤖

**OmniSense-AI** is a non-invasive industrial safety system. Unlike camera-based monitoring, it uses **WiFi CSI (Channel State Information)** to detect human activity and hazards, ensuring worker privacy while maintaining high-security standards.

## 🚀 Key Features
- **WiFi CSI Fall Detection:** Detects falls and slips using signal interference patterns (CSI), eliminating the need for cameras.
- **M2M Safety (Machine-to-Machine):** Real-time monitoring of proximity between humans and heavy machinery to prevent collisions.
- **IoT Smart Glove:** Integrated hardware for workers to interact safely with electrical and mechanical systems.
- **Unified Dashboard:** A real-time GUI for monitoring sensor health and receiving instant safety alerts.

## 📁 Repository Structure
- `src/omnisensing_core.py`: AI logic for processing WiFi CSI signals and signal-to-noise ratio (SNR) analysis.
- `src/smart_safety_glove.py`: Firmware logic for the IoT-enabled wearable glove.
- `src/Omni_GUI.py`: The main dashboard for visualizing safety logs and machine status.

## 🛠️ Tech Stack
- **Signal Processing:** WiFi CSI Analytics, Signal Filtering.
- **Languages:** Python.
- **AI/ML:** Pattern Recognition for fall events.
- **Hardware:** IoT Sensors, WiFi-enabled microcontrollers.

## 🔧 Installation
```bash
git clone [https://github.com/thakurrajnish609-cloud/Rajnish-OmniSense-AI.git](https://github.com/thakurrajnish609-cloud/Rajnish-OmniSense-AI.git)
pip install -r requirements.txt
python src/Omni_GUI.py
