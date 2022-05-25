import math
import numpy as np

earth_radius = 3960.0
radians_to_degrees = 180 / math.pi
degress_to_radians = math.pi / 180

def change_to_lat(miles):
  return (miles * earth_radius) / radians_to_degrees

def change_to_lng(lat, miles): 
  r = earth_radius * math.cos(lat * degress_to_radians)
  return (miles / r) * radians_to_degrees

# Lng --> Trục X
# Lat --> Trục Y
class MatrixPoint:
  I = [1, 0, -1, 0, 1, -1, -1, 1]
  J = [0, -1, 0, 1, 1, 1, -1, -1]
  
  def __init__(self, ws, hs, mws = 100, mhs = 100):
    assert mws % ws == 0
    assert mhs % hs == 0
    
    # Giả sử 
    # ws là trục X ứng với hệ trục Trái Đất
    # hs là trục Y ứng với hệ trục Trái Đất
    self.x = int(mws / ws)
    self.y = int(mhs / hs)
    self.ws = ws
    self.c = 0
    
    # Khoảng cách ứng với lat (Y)
    self.klat = change_to_lat(hs)
    
    self.lng = None
    self.lat = None
    
    self.current_pos = [0, 0]
    
  def __call__(self, lat : float, lng : float):
    self.klng = change_to_lng(lat, self.ws)
    
    self.lat = lat
    self.lng = lng
    
    # Build matrix
    # Ma trận đánh dấu
    self.matrix = []
    
    # Ma trận nhớ lat và lng
    self.four_pos_matrix = []
    
    for __ in range(self.x):
      t = []
      tx = lng
      ty = lat
      for __ in range(self.y):
        t.append({
          "tl" : self.__build_ls_latlng(tx, ty),
          "br" : self.__build_ls_latlng(tx + self.klng, ty + self.klat)
        })
      self.four_pos_matrix.append(t)
      self.matrix.append([0] * self.y)
      lat += self.klat
    
    
    self.matrix[0][0] = 1
    self.c = 1
    
  def __build_ls_latlng(self, lng, lat):
    return [lng, lat]
  
  def check(self, lng, lat, i, j):
    obj = self.four_pos_matrix[i][j]
    if lng >= obj["tl"][0] and lat >= obj["tl"][1]:
      if lng <= obj["br"][0] and lat <= obj["br"][1]:
        return True
    return False
  
  def forward(self, lng, lat, target):
    self.lng = lng
    self.lat = lat
    
    for i in MatrixPoint.I:
      for j in MatrixPoint.J:
        if self.current_pos[0] + i >= 0 and self.current_pos[1] + j >= 0 \
          and self.current_pos[0] + i <= self.x and self.current_pos[1] + j <= self.y \
          and self.check(lng, lat, self.current_pos[0] + i, self.current_pos[1] + j):
          new_i = self.current_pos[0] + i
          new_j = self.current_pos[1] + j
          self.matrix[new_i][new_j] = 1
          self.current_pos = [new_i, new_j]
          self.c += 1
          if target != None:
            target["dis"] -= self.ws
          return
  
  def bfs_exp_0_nearest(self):
    # BFS tìm điểm có tọa độ là 0 (hiểu là chưa tới)
    visited = []
    for __ in range(self.x):
      visited.append([False] * self.y)
    
    
    trace = [self.current_pos]
    visited[self.current_pos[0]][self.current_pos[1]] = True
    
    def __bfs(i_, j_, trace, visited):
      t = []
      for i in MatrixPoint.I:
        for j in MatrixPoint.J:
          ci = i_ + i
          cj = j_ + j
          print(ci, cj)
          if ci >= 0 and ci <= self.x \
          and cj >= 0 and cj <= self.y \
          and visited[ci][cj] == False:
            visited[ci][cj] = True
            t.append([ci, cj])
            if self.matrix[ci][cj] == 0:
              # Hành trình
              trace.append([ci, cj])
              return True
      while len(t) > 0:
        c = t.pop(0)
        trace.append(c)
        if __bfs(c[0], c[1], trace, visited):
          return True
      return False
    
    # Hàm tìm kiếm tọa độ đỉnh 0 gần nhất
    st = __bfs(self.current_pos[0], self.current_pos[1], trace, visited)
    print (st, trace)
    return trace, st
  
  def backward(self, target, prev_target):
    # Tính toán góc quay
    if prev_target == None:
        return [0, False]
    xa, ya = self.lng, self.lat
    xb, yb = target
    xc, yc = prev_target
    nab = np.array([ya - yb, xb - xa])
    nac = np.array([ya - yc, xc - xa])
    cos_vl = (nac * nab).sum() \
    / (np.sqrt((nab ** 2).sum()) * np.sqrt((nac ** 2).sum()))
    cos_vl = math.acos(cos_vl)
    deg = math.degrees(cos_vl)
    return deg, self.__calc_direction(nac, prev_target, target)
    
  def __calc_direction(self, nac, prev_target, target):
    xa, ya = self.lng, self.lat
    xc, yc = prev_target
    c = xa * yc - xc * ya
    ctarget = - (target[0] * nac[0] + target[1] * nac[1])
    return ctarget <= c