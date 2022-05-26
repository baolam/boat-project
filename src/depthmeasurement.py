# w --> w của trọng tâm điểm ảnh
def depthmeasurement(w, focal_length = 30, W = 2, espilon = 2.5) -> float:
  """Ước lượng khoảng cách

  Args:
    w (_type_): _description_
    focal_length (int, optional): _description_. Defaults to 30.
    W (int, optional): _description_. Defaults to 2.
    espilon (float, optional): _description_. Defaults to 2.5.

  Returns:
    float: Khoảng cách ước tính được
  """
  return (focal_length * w) \
    / (W + espilon)