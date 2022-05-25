import math
import serial
import threading
import pynmea2
import time
from .Angle import Angle
from .DepthMeasurement import DepthMeasureMent
from .MatrixPoint import MatrixPoint
from typing import List

class Mode:
  def __init__(self, ser : serial.Serial, gps : serial.Serial, width, height, ws = 1.0, hs = 1.0):
    self.measurement = DepthMeasureMent()
    self.angle = Angle(width, height)
    self.matrixpoint = MatrixPoint(ws, hs)
    self.arduino = ser
    self.gps = gps  
    self.motor = 100
    self.is_target = False
    self.garbages = []
    self.is_ok = False
    
    threading.Thread(name="arduino", target=self.__uart_arduino, daemon=True).start()
    threading.Thread(name="gps", target=self.__uart_gps, daemon=True).start()
    
  def run(self, target, prev_target):
    if len(self.garbages) == 0 or target == None:
      # Chuyển đổi chế độ tự động
      trace, st = self.matrixpoint.bfs_exp_0_nearest()
      t = trace[len(trace) - 1]
      if st == False:
        # Kết thúc hành trình, về nhà
        house = self.matrixpoint.four_pos_matrix[0][0]["tl"]
        house = [house["lng"], house["lat"]]
        deg, left_right = self.matrixpoint.backward(house, prev_target)
        self.ctrl_motor(deg, left_right)
      else:
        h = self.matrixpoint.four_pos_matrix[t[0]][t[1]]["tl"]
        deg, left_right = self.matrixpoint.backward(h, prev_target)
        self.ctrl_motor(deg, left_right)
      return False
   
    self.target = target
    if self.target["dis"] < 0:
      # Yêu cầu đổi em khác
      return True
    deg, left_right = self.target["deg"], self.target["left"]
    self.ctrl_motor(deg, left_right) 
    return False

  def ctrl_motor(self, deg, left_right):
    if left_right:
      deg = -deg
    n = str(self.motor) + ';' + str(self.motor) + ';' + str(deg) + ";#"
    self.arduino.write(bytes(n, 'utf-8'))  
  
  def turnlr(self, left_right):
      angle = 45
      if left_right:
        angle = - angle
      n = self(self.motor) + ';' + str(self.motor) + ';' + str(angle) + ';#'
      self.arduino.write(bytes(n, 'utf-8'))
      
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
  
  def set_speed(self, speed):
      self.motor = speed
      
  def __sort_element(self, e : dict):
    return e["distance"]
  
  def __uart_arduino(self):
    time.sleep(3)
    self.arduino.write(bytes("Arduino ưi! Bạn còn sống không", "utf-8"))
    time.sleep(2)
    
    while True:
      # Chạy nhận dữ liệu từ Arduino
      if self.arduino.in_waiting:
        received_data = self.arduino.readline().decode('utf-8').rstrip()
        received_data = received_data.replace('#','')
        data = received_data.split('@')
        if len(data) > 1:
            ntu, tds = data
  
  def __uart_gps(self):
    is_started = False
    while True:
      pynmea2.NMEAStreamReader()
      newdata = self.gps.readline()
      newdata = newdata.decode("utf-8")
      if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
         
        if not is_started:
          self.matrixpoint(lat, lng)
          is_started = True
          self.is_ok = True
          
        # Gọi hàm cập nhật vị trí
        self.matrixpoint.forward(lng, lat, self.target)