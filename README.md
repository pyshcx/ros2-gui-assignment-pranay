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

### Module Responsibilities

| File               | Role                                                                |
| ------------------ | ------------------------------------------------------------------- |
| `main.py`          | Launches the Qt application                                         |
| `gui.py`           | Builds UI, connects signals, updates plot + status panel            |
| `ros_interface.py` | Runs the ROS2 node on a background executor, emits telemetry to GUI |
| `logger.py`        | Writes CSV log rows                                                 |

---

### Architecture Diagram

![Architecture](diagram_arch.png)

---

### How ROS Communication is Handled

ROS2 communication is performed by a dedicated `rclpy` node running inside a background `MultiThreadedExecutor`.
This keeps the Qt UI thread free and responsive.

When the user clicks **Start** or **Stop**, Qt emits a custom signal which triggers:

```
/control_cmd → std_msgs/String("start" or "stop")
```

The node publishes these commands via `.publish()`.

Telemetry values are generated using ROS timers (`create_timer()`):

| Frequency | Data                 |
| --------: | -------------------- |
|      5 Hz | Battery %, Velocity  |
|     33 Hz | Sensor waveform data |

These callbacks **do not** directly modify the Qt UI.
Instead, they emit Qt signals back into the GUI thread.
This ensures fully thread-safe UI updates.

CSV logging is also signal-driven:
whenever telemetry arrives, and logging is enabled, rows are appended to CSV immediately.

This clean separation (UI ↔ ROS node ↔ logger) makes the system modular, and suitable for embedded deployment with limited resources.

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
