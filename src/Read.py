import serial
import threading
import time
import socketio
from .control import control

class Read:
  is_started = False
  
  def __init__(self, socket : socketio.Client, arduino : serial.Serial, namespace : str):
    self.arduino = arduino
    self.socket = socket
    self.namespace = namespace
    self.motor = 100
  
    # Tiến trình chạy chung
    threading.Thread(name="arduino", target=self.__arduino, daemon=True).start()
       
  def __arduino(self):
    time.sleep(3.5)
    self.arduino.write(bytes("Arduino ưi! Bạn còn sống không?", "utf-8"))
    
    Read.is_started = True
    
    while True:
      if self.arduino.in_waiting:
        received_data = self.arduino.readline().decode("utf-8") \
          .replace('#', '').split('@')
        print(received_data, "arduino")
        if len(received_data) > 1:
          ntu, tds = map(float, received_data)
          env = {
            "time": str(5),
            "turbidity" : ntu,
            "dissolved_solid" : tds,
            "speed": 12,
            "battery": 87,
            "motor_speed": self.motor
          }
          self.socket.emit("record", data=env, namespace=self.namespace)