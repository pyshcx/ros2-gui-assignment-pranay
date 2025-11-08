# ROS2 GUI Control + Telemetry Visualization

## Objective
Desktop GUI built from scratch using PySide6 that communicates with ROS2.
Features:
- Start / Stop buttons → publish to `/control_cmd`
- Status display → battery %, velocity
- Live plot of simulated sensor data
- CSV logging

## Setup
```bash
source ~/ros2_humble/install/setup.bash
cd ~/ros2_gui_test
source venv/bin/activate
python3 src/main.py

## Demo Video

Watch the demo here:  
https://youtu.be/vOkSku_qIhs
