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
  return math.degrees(cos_phi)