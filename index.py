import socketio
import cv2
import serial
import threading
from src.Mode import Mode

SERVER_ADDRESS = "http://boat-project.herokuapp.com"
NAMESPACE = "/device"

arduino = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

client = socketio.Client()
video = cv2.VideoCapture(0)
width = 500
height = 500

def classify(img):
  # Tạo kết quả nhận dạng :>>
  pass

def run_socket():
    client.on("")
    client.connect(SERVER_ADDRESS, namespace=NAMESPACE)

c = 0
target = None

threading.Thread(name="socket", target=run_socket, daemon=True).start()
handle = Mode(arduino, width, height)

while True:
  __, frame = video.read()
  if handle.is_target:
    handle.is_target = False
    
    if target == None:
      # Cần xử lí
      # Camera quay 360 tim rac
      pass
    
    handle.update_coordinates(target)
    
    coordinates = classify(frame)
    
    if len(coordinates) == 0:
      # No garbage
      pass
    else:
    
        r = handle.calc_classify(coordinates)
        
        target = r.pop(0)
        handle.garbages += r
        handle.sort()
    
        # Phẩn xử lí tọa độ mới
        pass
        
  handle.run()    