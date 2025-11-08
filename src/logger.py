import csv
import os
from datetime import datetime

class CsvLogger:
    def __init__(self):
        self.file = None
        self.writer = None
        self.is_active = False

    def start(self, path: str):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        self.file = open(path, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['ros_time_sec', 'battery_pct', 'velocity_mps', 'sensor_value'])
        self.is_active = True

    def write_state(self, battery_pct: float, velocity_mps: float):
        if not self.is_active:
            return
        self.writer.writerow([self._now_sec(), f"{battery_pct:.3f}", f"{velocity_mps:.3f}", ''])

    def write_sensor(self, t_sec: float, value: float):
        if not self.is_active:
            return
        self.writer.writerow([f"{t_sec:.6f}", '', '', f"{value:.6f}"])

    def stop(self):
        if self.file:
            self.file.flush()
            self.file.close()
        self.file = None
        self.writer = None
        self.is_active = False

    def _now_sec(self) -> float:
        return datetime.utcnow().timestamp()

