import serial
import threading
import time
import socketio
from .control import control

class Read:
  def __init__(self, socket : socketio.Client, arduino : serial.Serial, namespace : str):
    self.arduino = arduino
    self.socket = socket
    self.namespace = namespace
  
    # Tiến trình chạy chung
    threading.Thread(name="arduino", target=self.__arduino, daemon=True).start()
       
  def __arduino(self):
    time.sleep(3.5)
    self.arduino.write(bytes("Arduino ưi! Bạn còn sống không?", "utf-8"))
    
    while True:
      if self.arduino.in_waiting:
        received_data = self.arduino.readline().decode("utf-8") \
          .replace('#', '').split('@')
        if len(received_data) > 1:
          ntu, tds = map(float, received_data)
          env = {
            "ntu" : ntu,
            "tds" : tds
          }
          self.socket.emit("env", data=env, namespace=self.namespace)