#######
  # Trục Lng --> Trục Ox
  # Trục Lat --> Trục Oy
#######
import serial
import threading
import pynmea2
import time
import socketio

from .Read import Read
from .lnglat import change_to_lat, change_to_lng, latlng
from .sensor_hn import read
from .equation import create_linear_equation, angle_between_two_linears
from .control import control
from .kalman_filter import KalmanFilter

def check_point_ctd(ti, tj, row_matrix, col_matrix):
  return ti >= 0 and ti <= row_matrix - 1 \
  and tj >= 0 and tj <= col_matrix - 1

i_filter = KalmanFilter(1.5, 0.5, 2)
j_filter = KalmanFilter(2, 0.5, 2)

class MatrixPoint:
  I = [0, 0, 1, -1] # Phiên mã (trái, phải, trên)
  J = [1, -1, 0, 0] # Phiên mã (trái, phải, trên)
  
  is_started = False
  WARNING_VC = 3 # Mã vật cản
  VISITED = 1 # Mã đã duyệt
  NOT_VISITED = 0 # Mã chưa duyệt
  PRIORITY = 2 # Mã ưu tiên tới
    
  def __init__(self, socket : socketio.Client, namespace : str, gps : serial.Serial, arduino : serial.Serial, w = 1, h = 1, wb = 100, hb = 100):
    assert wb % w == 0
    assert hb % h == 0
    
    self.socket = socket
    self.namespace = namespace
    # Giả định w ứng với x
    # Giả định h ứng với y
    self.row_matrix = int(wb / w)
    self.col_matrix = int(hb / h)
    
    self.w = w
    self.h = h
    self.meet = 0 # Biến lưu tổng số lần nhận dạng rác
    self.is_full = 2500
    self.is_run_socket = True
    
    self.klng = None
    self.klat = None
    self.lng_st = None
    self.lat_st = None
    self.matrix = []
    self.current_pos = [None, None]
    self.prev = [None, None]
    
    self.gps = gps
    self.arduino = arduino
    self.motor = 100
    self.is_trace = 0
            
    # Tiến trình chạy chung
    threading.Thread(name="gps", target=self.__gps, daemon=True).start()
    
  def __call__(self, lng : float, lat : float):
    # Gọi hàm này là lấy lng, lat làm tọa độ chuẩn
    try:
      self.klat = change_to_lat(self.h)
      self.klng = change_to_lng(lat, self.w)
      
      self.lng_st = lng
      self.lat_st = lat
    finally:
      self.four_pos_mat = []
      for __ in range(self.row_matrix):
        self.matrix.append([MatrixPoint.NOT_VISITED] * self.col_matrix)
        
      self.matrix[0][0] = MatrixPoint.VISITED
      self.current_pos = [0, 0]
      self.prev = [0, 0]
  
  def check_outpoint(self, lng, lat):
    """Kiểm tra điểm đã rời khỏi ô hiện tại chưa

    Args:
      lng (_type_): _description_
      lat (_type_): _description_

    Returns:
      _type_: _description_
    """
    i_, j_ = self.convert_lnglat_into_ij(lng, lat)
    i, j = int(i_), int(j_)
    return self.current_pos[0] != i and self.current_pos[1] != j, i_, j_
  
  def flood(self):
    """Loang đánh dấu điều kiện (đánh dấu vật cản)
    """
    r = read()
    i, j = self.current_pos
    for code in range(3):
      ti = i + MatrixPoint.I[code]
      tj = j + MatrixPoint.J[code]
      st = r[code]  
      if check_point_ctd(ti, tj, self.row_matrix, self.col_matrix) and st:
        self.matrix[ti][tj] = MatrixPoint.WARNING_VC
  
  def trace(self, trace):
    # Kích hoạt cho chương trình chạy theo hướng truy vết
    self.is_trace = 1
    
    while len(trace) > 0:
      if self.is_trace == 1 and MatrixPoint.is_started and Read.is_started:
        target = trace.pop(0)
        current_target = create_linear_equation(self.current_pos, target)
        prev_current = create_linear_equation(self.prev, self.current_pos)
        
        deg = angle_between_two_linears(current_target, prev_current)
        left_right = current_target[2] >= prev_current[2]
        
        # Gửi thông báo lên server
        t = {
          "deg" : deg,
          "left" : left_right
        }
        
        print ("Hành trình thực hiện ", t)
        self.socket.emit("notification", t, namepsace=self.namespace)       
        
        control(self.arduino, 0, deg, left_right)
        time.sleep(2.)
        control(self.arduino, self.motor, 0, False)
        
        self.is_trace = 2
    
    self.is_trace = 0
      
  def convert_lnglat_into_ij(self, lng, lat):
    """Chuyển đổi kinh độ vĩ độ thành các vị trí trên ma trận điểm

    Args:
      lng (_type_): _description_
      lat (_type_): _description_

    Returns:
      _type_: _description_
    """
    return (lng - self.lng_st) / self.klng, (lat - self.lat_st) / self.klat
  
  def __gps(self):
    count_gps = 0
    while True:
      pynmea2.NMEAStreamReader()
      newdata = self.gps.readline()
      newdata = newdata.decode("utf-8")
      
      if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        count_gps += 1

        if lat != 0.0 and lng != 0.0:
          if self.is_run_socket and (not MatrixPoint.is_started):
            self.socket.emit("notification", {
              "standard" : True
            }, namespace=self.namespace)
        
          MatrixPoint.is_started = True
          self.__call__(lng, lat)
          
        else:
          if self.is_run_socket:          
            self.socket.emit("notification", {
              "standard" : False
            }, namespace=self.namespace)
          MatrixPoint.is_started = False
          
        if MatrixPoint.is_started:
          state, i, j = self.check_outpoint(lng, lat)
          
          # Lọc tầng 1          
          i = i_filter.update_estimate(i)
          j = j_filter.update_estimate(j)
          
          # Lọc tầng 2
          i = i_filter.update_estimate(i)
          j = j_filter.update_estimate(j)
          
          if state:
            # Cập nhật lại tọa độ mới
            self.prev = self.current_pos
            self.current_pos[0] = int(i)
            self.current_pos[1] = int(j)
            self.matrix[self.current_pos[0]][self.current_pos[1]] = MatrixPoint.VISITED
            self.flood()
            self.is_trace = 1
          
          if count_gps >= 2 and lat!=0 and lng !=0:
            pos = {
              "lat": lat,
              "lng": lng,
              "i" : i,
              "j" : j
            }
            if self.socket.connected:
              self.socket.emit("gps", data=pos, namespace=self.namespace)
            count_gps = 0
          