import math
import serial
import threading
import socketio

from .Angle import Angle
from .DepthMeasurement import DepthMeasureMent

class Mode:
  def __init__(self, arduino : serial.Serial, cli : socketio.Client, width : int, height : int):
    self.measurement = DepthMeasureMent()
    self.angle = Angle(width, height)
    self.arduino = arduino
    self.cli = cli

    self.__mode = 0
    self.is_target = False
    self.garbages = []
    
    threading.Thread(name="uart", target=self.__uart, daemon=True).start()
    
  def run(self):
    if len(self.garbages) == 0:
      return
    
    if self.__mode == 0:
      # Chế độ tự động
      pass
    elif self.__mode == 1:
      # Chế độ thủ công
      pass
    else:
      # Chế độ ngẫu nhiên
      pass
  
  def calc_classify(self, clss : List[tuple]):
    r = []
         
    for x, y, w, h in clss:
      a = self.angle.get_angle(x, y, w, h)
      d = self.measurement.get_distance(w)
      
      a["distance"] = d
      a["see"] = True
          
      r.append(a)

    r.sort(key=self.__sort_element)
    return r
  
  def update_coordinates(self, e : dict):
    # e là dict có khoảng cách nhỏ nhất trước khi di chuyển (ước tính)
    for i in range(len(self.garbages)):
      a = f[i]["distance"]
      alpha = f[i]["deg"]
      
      b = e["distance"]
      beta = e["deg"]
      
      angle, dis = self.angle.get_relative(a, b, alpha, beta)
      if angle > 90:
        f[i]["see"] = False
      else:
        f[i]["see"] = True
      
      f[i]["deg"] = angle
      f[i]["distance"] = dis
  
  def sort(self):
    self.garbages.sort(key=self.__sort_element)
      
  def __sort_element(self, e : dict):
    return e["distance"]
  
  def __uart(self):
    arduino = self.arduino
    cli = self.cli
    
    while True:
      # Chạy nhận dữ liệu từ Arduino
      if arduino.in_waiting > 0:
          received_data = arduino.readline().decode('utf-8').rstrip()
          received_data = received_data.replace('\r\n')
          received_data = received_data.split('@')
          lat, lng, ntu, tds, battery, speed = [float(i) for i in received_data]
          
          
        
  def set_mode(self, mode : int):
    self.__mode = mode