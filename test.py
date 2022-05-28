import math

def running(A, B, dis, alpha):
  xa, ya = A
  xb, yb = B
  
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

print (running((1, 1), (4, 2), math.sqrt(25), 30)) 