import math

class Angle:
  def __init__(self, width, height):
    self.w = width // 2
    self.h = height // 2
    self.width = width
    self.height = height
  
  def get_angle(self, x : int, y : int, w : int, h : int) -> dict:
    """Lấy tọa độ và hướng quay trái phải

    Args:
      x (_type_): _description_
      y (_type_): _description_
      w (_type_): _description_
      h (_type_): _description_

    Returns:
      dict: Kết quả trả về
    """
    xb = x + 0.5 * w
    yb = y + 0.5 * h
    
    
    res = {
      "deg" : 0,
      "left" : False,
      "distance_img" : (xb - self.w) ** 2 + yb ** 2
    }
    
    cos_vl = 1 / res["distance_img"]
    cos_rad = math.acos(cos_vl)
    cos_deg = math.degrees(cos_rad)
    
    res["deg"] = cos_deg
    
    if xb >= self.w:
      res["left"] = True
      
    return res
  
  def get_relative(self, a : float, b : float, alpha_deg : float, beta_deg : float) -> tuple:
    """Trả về góc theo tọa độ và khoảng cách

    Args:
      a (float): Độ dài đoạn a
      b (float): Độ dài đoạn b
      alpha_deg (float): Góc tạo bởi điểm bắt đầu với đích
      beta_deg (float): Góc tạo bởi điểm bắt đầu với điểm đến

    Returns:
      tuple : kết quả
    """
    alpha_deg = math.radians(alpha_deg)
    beta_deg = math.radians(beta_deg)
    
    temp_cos = math.cos(alpha_deg + beta_deg)
    c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * temp_cos)
    
    off_cos = (b - a * temp_cos) / c
    off_cos = math.acos(off_cos)
    off_cos = math.degrees(off_cos)
    
    return 180 - off_cos, c
    