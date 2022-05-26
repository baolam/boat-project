from typing import List

# Quy định chân
# 0 --> trái
# 1 --> phải
# 2 --> thẳng
PINS = []

def read() -> List[bool]:
  """Đọc cảm biến hồng ngoại

  Returns:
    List[bool]: _description_
  """
  r = []
  for pin in PINS:
    r.append(0)
  r.append(0)
  return r