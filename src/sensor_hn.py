from typing import List
import RPi.GPIO as GPIO

# Quy định chân
# 0 --> trái
# 1 --> phải
# 2 --> thẳng

GPIO.setmode(GPIO.BCM)
PINS = [17, 27, 22]

for i in PINS:
  GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read() -> List[bool]:
  """Đọc cảm biến hồng ngoại

  Returns:
    List[bool]: _description_
  """
  r = []
  for pin in PINS:
    r.append(int(not GPIO.input(pin)))
  r.append(0)
  return r