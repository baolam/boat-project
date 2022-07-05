from typing import List
import serial

def control(ser : serial.Serial, motors : int, deg : int, left_right : bool):
  """Điều khiển thiết bị

  Args:
    ser (serial.Serial): _description_
    motors (int): _description_
    deg (int): _description_
    left_right (bool): _description_
  """
  if not left_right:
    deg = - deg
  n = str(motors) + ';' + str(motors) + ';' + str(deg) + ';#'
  print ("Lệnh điều khiển Arduino", n)
  ser.write(bytes(n, "utf-8"))