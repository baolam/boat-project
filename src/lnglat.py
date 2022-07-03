from typing import Tuple
import math

earth_radius = 3960.0
miles_to_meter = 1609.344
radians_to_degrees = 180 / math.pi
degress_to_radians = math.pi / 180

def change_to_lat(metters):
  """Đổi mét sang độ dài lat

  Args:
    miles (_type_): _description_

  Returns:
    _type_: _description_
  """
  return (metters / miles_to_meter * earth_radius) / radians_to_degrees

def change_to_lng(lat, metters):
  """Đổi mét sang độ dài lat

  Args:
    lat (_type_): _description_
    miles (_type_): _description_

  Returns:
    _type_: _description_
  """
  r = earth_radius * math.cos(lat * degress_to_radians)
  return ((metters / miles_to_meter) / r) * radians_to_degrees

def latlng(lng, lat) -> Tuple:
  """Kinh độ vĩ độ dưới dạng tuple

Args:
    lng (_type_): _description_
    lat (_type_): _description_

Returns:
    Tuple: _description_
  """
  return lng, lat