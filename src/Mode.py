import math
import serial
import threading
from .Angle import Angle
from .DepthMeasurement import DepthMeasureMent
from .MatrixPoint import MatrixPoint

class Mode:
  def __init__(self, ser : serial.Serial, gps : serial.Serial, width, height, ws = 1.0, hs = 1.0):
    self.measurement = DepthMeasureMent()
    self.angle = Angle(width, height)
    self.matrixpoint = MatrixPoint(ws, hs)
    self.arduino = ser
    self.gps = gps

    self.__mode = 0
    self.is_target = False
    self.garbages = []
    
    threading.Thread(name="arduino", target=self.__uart_arduino, daemon=True).start()
    threading.Thread(name="gps", target=self.__uart_gps, daemon=True).start()
    
  def run(self, target):
    if len(self.garbages) == 0 or target == None:
      # Chuyển đổi chế độ tự động
      trace, st = self.matrixpoint.bfs_exp_0_nearest()
      t = trace[len(trace) - 1]
      if st == False:
        # Kết thúc hành trình, về nhà
        house = self.matrixpoint.four_pos_matrix[0][0]["tl"]
        house = [house["lng"], house["lat"]]
        
      
    # if self.__mode == 0:
    #   # Chế độ tự động
    #   pass
    # elif self.__mode == 1:
    #   # Chế độ thủ công
    #   pass
    # else:
    #   # Chế độ ngẫu nhiên
    #   pass
    # Lệnh điều khiển
    # --> Gửi tới arduino
    # Lệnh gửi tới arduino
    # R;motor_1;motor_2;angle#
    
    return False 
    
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
  
  def __uart_arduino(self):
    while True:
      # Chạy nhận dữ liệu từ Arduino
      if self.arduino.in_waiting:
        received_data = self.arduino.readline().strip() \
          .replace('\r\n', '').split(';')
        if received_data[0] == "lnglat":
          lng, lat = map(float, received_data[1:])
          self.matrixpoint(lng, lat)
        if received_data[0] == "env":
          # Dữ liệu môi trường
          pass
  
  def __uart_gps(self):
    while True:
      pass
  
  def set_mode(self, mode : int):
    self.__mode = mode