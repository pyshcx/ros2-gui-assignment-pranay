import math
import threading
import numpy as np

from PySide6.QtCore import QObject, Signal

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String

class _CoreNode(Node):
    def __init__(self):
        super().__init__('control_panel_node')
        self.pub_cmd = self.create_publisher(String, '/control_cmd', 10)

        self.start_time = self.get_clock().now().nanoseconds / 1e9
        self.timer_state = self.create_timer(0.2, self._tick_state)
        self.timer_sensor = self.create_timer(0.03, self._tick_sensor)

        self._battery = 100.0
        self._velocity = 0.0
        self._t_last = self.start_time

        self.cb_state = None
        self.cb_sensor = None

    def publish_cmd(self, text: str):
        msg = String()
        msg.data = text
        self.pub_cmd.publish(msg)
        self.get_logger().info(f"Published: {text}")

    def _tick_state(self):
        now = self.get_clock().now().nanoseconds / 1e9
        dt = max(1e-3, now - self._t_last)
        self._t_last = now
        self._velocity = 0.5 + 0.5 * math.sin(0.5 * (now - self.start_time))
        self._battery = max(0.0, self._battery - (0.01 + 0.02 * self._velocity) * dt)
        if self.cb_state:
            self.cb_state(self._battery, self._velocity)

    def _tick_sensor(self):
        t = self.get_clock().now().nanoseconds / 1e9 - self.start_time
        val = math.sin(2 * math.pi * 0.5 * t) + 0.1 * np.random.randn()
        if self.cb_sensor:
            self.cb_sensor(t, float(val))

class ROSInterface(QObject):
    sig_state_update = Signal(float, float)
    sig_sensor_update = Signal(float, float)

    def __init__(self):
        super().__init__()
        rclpy.init(args=None)
        self._node = _CoreNode()

        self._node.cb_state = lambda b,v: self.sig_state_update.emit(b, v)
        self._node.cb_sensor = lambda t,x: self.sig_sensor_update.emit(t, x)

        self._executor = MultiThreadedExecutor()
        self._executor.add_node(self._node)
        self._spin_thread = threading.Thread(target=self._executor.spin, daemon=True)
        self._spin_thread.start()

    def publish_start(self):
        self._node.publish_cmd('start')

    def publish_stop(self):
        self._node.publish_cmd('stop')

