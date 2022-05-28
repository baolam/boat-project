from typing import List
import math
import numpy as np

# lng, lat
def create_linear_equation(a : List, c):
  """Tạo phương trình đường thẳng dựa trên ma trận điểm

  Args:
    a (List): _description_
    c (_type_): _description_

  Returns:
    _type_: _description_
  """
  xa, ya = a
  xc, yc = c
  alinear = ya - yc
  blinear = xc - xa
  clinear = xa * yc - xc * ya
  return alinear, blinear, clinear

# a, b là tuple gồm 3 giá trị...
def angle_between_two_linears(a, b):
  """Tính góc giữa 2 đường thẳng

  Args:
    a (_type_): _description_
    b (_type_): _description_

  Returns:
    _type_: _description_
  """
  na = np.array([a[0], a[1]])
  nb = np.array([b[0], b[1]])
  cos_phi = math.abs((na * nb).sum()) / (math.sqrt((na ** 2).sum()) * math.sqrt((nb ** 2).sum()))
  cos_phi = math.acos(cos_phi)
  cos_phi = math.degrees(cos_phi)
  return math.floor(cos_phi)

def change_depthmeausement_deg_into_ij(prev, curr, dis, alpha):
  """Công thức chuyển đổi khoảng cách ước tính và góc quay thành tọa độ i, j trong ma trận điểm

  Args:
    prev (_type_): _description_
    curr (_type_): _description_
    dis (_type_): _description_
    alpha (_type_): _description_

  Returns:
    _type_: _description_
  """
  xa, ya = prev
  xb, yb = curr
  
  wx = xb - xa
  wy = yb - ya
  
  d1 = math.sqrt(wx ** 2 + wy ** 2)
  d2 = dis / 100
  
  beta = d1 * d2 * math.cos(math.radians(alpha)) + wx * xb + wy * yb
  a = wy ** 2 + wx ** 2
  b = beta * wx + (wy ** 2) * xb - wy * yb * wx
  b = 2 * b
  c = beta ** 2 - 2 * wy * yb * beta + ((xb ** 2) + (yb ** 2) - (d2 ** 2)) * (wy ** 2)
  
  x1 = (b + math.sqrt((b ** 2) - 4 * a * c)) / (2 * a)
  x2 = (b - math.sqrt((b ** 2) - 4 * a * c)) / (2 * a)
  
  y1 = (beta - wx * x1) / wy
  y2 = (beta - wx * x2) / wy
  
  return [x1, y1, y1 >= yb], [x2, y2, y2 >= yb]

def get_degree_depend_on_image(x, y, w, h, wid):
  """Tính toán góc quay dựa vào ảnh

  Args:
    x (_type_): _description_
    y (_type_): _description_
    w (_type_): _description_
    h (_type_): _description_
    wid (_type_): _description_

  Returns:
    _type_: _description_
  """
  xb = x + w // 2
  yb = y + h // 2
  cos_alpha = yb / (math.sqrt((xb - wid / 2) ** 2 + yb ** 2))
  cos_alpha = math.acos(cos_alpha)
  cos_alpha = math.degrees(cos_alpha)
  return math.floor(cos_alpha), xb <= wid / 2