import socketio
import cv2
import serial
import threading
from src.Mode import Mode
from src.MatrixPoint import MatrixPoint

SERVER_ADDRESS = "http://boat-project.herokuapp.com"
NAMESPACE = "/device"

arduino = serial.Serial(
<<<<<<< HEAD
  port = "/dev/ttyACM0",
  baudrate=9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

gps = serial.Serial(
  port = "/dev/ttyACM1",
  baudrate=9600,
  timeout=0.5
)
=======
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)
>>>>>>> e546fad6b73ac41fd6f6f4dc519b74e7f8d1d2ff

client = socketio.Client()
video = cv2.VideoCapture(0)
width = 500
height = 500
<<<<<<< HEAD
handle = Mode(arduino, gps, width, height)
=======
>>>>>>> e546fad6b73ac41fd6f6f4dc519b74e7f8d1d2ff

def classify(img):
    cv2.imwrite("t.jpg", img)
    with open("t.jpg", mode="rb") as f:
        b = base64.b64encode(f.read())
    b = str(b)
    b = b[2:len(b)-1]
    
    state = requests.post(SERVER_ADDRESS, json={'base64': b})
    print(state)

def set_speed(speed):    
  handle.set_speed(speed)

<<<<<<< HEAD
def direction(left_right):
    handle.turnlr(left_right)
    
def socket():  
  server.on("speed", handler=set_speed, namespace=NAMESPACE)  
  server.on("direction", handler=direction, namespace=NAMESPACE)
  server.connect(SERVER_ADDRESS, namespaces=NAMESPACE)
  
=======
def run_socket():
    client.on("")
    client.connect(SERVER_ADDRESS, namespace=NAMESPACE)

>>>>>>> e546fad6b73ac41fd6f6f4dc519b74e7f8d1d2ff
c = 0
prev_target = None
target = None

threading.Thread(name="socket", target=run_socket, daemon=True).start()
handle = Mode(arduino, width, height)

while True:
  __, frame = video.read()
  if handle.is_target:
    handle.is_target = False
    
    if target == None:
<<<<<<< HEAD
      # Đổi mode thành tự động
      # handle.set_mode(2)
=======
      # Cần xử lí
      # Camera quay 360 tim rac
>>>>>>> e546fad6b73ac41fd6f6f4dc519b74e7f8d1d2ff
      pass
    else:
      handle.update_coordinates(target)
    
    coordinates = classify(frame)
    
<<<<<<< HEAD
    prev_target = target
    target = r.pop(0)
    handle.garbages += r
    handle.sort()
    
  if handle.is_ok and handle.run(target, prev_target):
    prev_target = target
    target = handle.garbages.pop(0)    
=======
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
>>>>>>> e546fad6b73ac41fd6f6f4dc519b74e7f8d1d2ff
