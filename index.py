import socketio
import cv2
import serial
import threading
from src.Mode import Mode
from src.MatrixPoint import MatrixPoint

SERVER_ADDRESS = "http://boat-project.herokuapp.com"
NAMESPACE = "/device"
server = socketio.Client()

arduino = serial.Serial()
mp = MatrixPoint(1.5, 0.8)

video = cv2.VideoCapture(0)
width = 500
height = 500
handle = Mode(arduino, width, height)

def classify(img):
  # Tạo kết quả nhận dạng :>>
  pass

def socket():
  server.connect(SERVER_ADDRESS, namespaces=NAMESPACE)
  
c = 0
target = None

threading.Thread(name="socket", target=socket, daemon=True).start()

while True:
  __, frame = video.read()
  if handle.is_target:
    handle.is_target = False
    
    if target == None:
      # Cần xử lí
      pass
    
    handle.update_coordinates(target)
    
    coordinates = classify(frame)
    r = handle.calc_classify(coordinates)
    
    target = r.pop(0)
    handle.garbages += r
    handle.sort()
    
    # Phẩn xử lí tọa độ mới
    
  handle.run()    