# ROS2 GUI Control + Telemetry Visualization

## Overview

This project implements a custom desktop GUI built using **PySide6** that directly communicates with **ROS 2**.
It demonstrates publishing commands, visualizing telemetry data, and logging ROS data streams efficiently.

## Features

| Component      | Description                                 |
| -------------- | ------------------------------------------- |
| Start Button   | Publishes `"start"` to `/control_cmd` topic |
| Stop Button    | Publishes `"stop"` to `/control_cmd` topic  |
| Status Panel   | Shows simulated Battery % and Velocity      |
| Live Data Plot | Real-time sensor waveform (PyQtGraph)       |
| CSV Logging    | Saves ROS data to CSV when enabled          |

---

## Setup & Run

```bash
# Source ROS2 environment
source ~/ros2_humble/install/setup.bash

# Activate Python venv
cd ~/ros2_gui_test
source venv/bin/activate

# Launch GUI
python3 src/main.py
```

Dependencies:

```
PySide6
pyqtgraph
rclpy
numpy
```

---

## Design Decisions

This GUI was built using PySide6 for a light, embedded-friendly footprint.
A background MultiThreadedExecutor runs ROS 2 callbacks without blocking the Qt event loop, and Qt signals are used for thread-safe data transfer to UI widgets.

Sensor + state telemetry are simulated inside the node so the application runs hardware-independent.
PyQtGraph is used for fast real-time plotting.
CSV logging is implemented manually to ensure deterministic low-latency writing.

---

## Demo Video

Watch the GUI in action:
[https://youtu.be/vOkSku_qIhs](https://www.youtube.com/watch?v=vOkSku_qIhs)

---

## Deliverables Inside Repo

* `/src` → full application code
* `README.md` → documentation
* CSV sample log
