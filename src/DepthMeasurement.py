class DepthMeasureMent:
  def __init__(self, focal_length=30, espilon=2.5, W=2):
    self.focal_length = focal_length
    self.espilon = espilon
    self.W = W
    
  def get_distance(self, w) -> float:
    """Lấy khoảng cách của đối tượng trong ảnh

    Args:
      w (_type_): Ảnh trải dài theo chiều dài

    Returns:
      float: Kết quả khoảng cách
    """
    return (self.focal_length * w) \
    / (self.W + self.espilon)