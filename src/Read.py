import serial
import threading
import time
import socketio
from .control import control

def rating(ntu, tds):
  rt_ntu = ""
  rt_tds = ""
  
  if  ntu > 100:
    rt_ntu = "Không thể chấp nhận được"
  elif  ntu > 50:
    rt_ntu = "Kém"
  elif  ntu > 25:
    rt_ntu = "Tạm được"
  elif  ntu > 10:
    rt_ntu = "Khá ổn"
  elif  ntu > 5:
    rt_ntu = "Ổn định"
  else:  rt_ntu = "Rất tốt"

  if  tds > 1500:
    rt_tds = "Không thể chấp nhận được"
  elif  tds > 1200:
    rt_tds = "Kém"
  elif  tds > 900:
    rt_tds = "Tạm được"
  elif  tds > 600:
    rt_tds = "Khá ổn"
  elif  tds > 300:
    rt_tds = "Ổn định"
  else:  rt_tds = "Rất tốt"

  return rt_ntu, rt_tds

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
          .replace('#', '') \
          .replace('\r\n', '').split('@')
        
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

          eval_ntu, eval_tds = rating(ntu, tds)
          self.socket.emit("notification", data={
            "can" : "ntu : " + eval_ntu
          }, namespace=self.namespace)

          self.socket.emit("notification", data={
            "can" : "tds : " + eval_ntu
          }, namespace=self.namespace)