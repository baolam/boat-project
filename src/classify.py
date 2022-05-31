import requests
import cv2
import base64

def request_to_server(img, url : str) -> int:
  """Gửi ảnh lên server

  Args:
    img (_type_): _description_
    url (str): _description_

  Returns:
    int: mã thành công hay chưa
  """
  cv2.imwrite("temp.png", img)
  with open("temp.png", mode="rb") as fin:
    b = str(base64.b64encode(fin.read()))
  b = b[2:len(b) - 1]
  r = requests.get(url, json = { "base64" : b })
  return r.status_code