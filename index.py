import socketio
import cv2
import serial
import threading
from src.Mode import Mode
from src.MatrixPoint import MatrixPoint

SERVER_ADDRESS = "http://boat-project.herokuapp.com"
NAMESPACE = "/device"
server = socketio.Client()

arduino = serial.Serial(
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

video = cv2.VideoCapture(0)
width = 500
height = 500
handle = Mode(arduino, gps, width, height)

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

def direction(left_right):
    handle.turnlr(left_right)
    
def socket():  
  server.on("speed", handler=set_speed, namespace=NAMESPACE)  
  server.on("direction", handler=direction, namespace=NAMESPACE)
  server.connect(SERVER_ADDRESS, namespaces=NAMESPACE)
  
c = 0
prev_target = None
target = None

threading.Thread(name="socket", target=socket, daemon=True).start()

while True:
  __, frame = video.read()
  if handle.is_target:
    handle.is_target = False
    
    if target == None:
      # Đổi mode thành tự động
      # handle.set_mode(2)
      pass
    else:
      handle.update_coordinates(target)
    
    coordinates = classify(frame)
    r = handle.calc_classify(coordinates)
    
    prev_target = target
    target = r.pop(0)
    handle.garbages += r
    handle.sort()
    
  if handle.is_ok and handle.run(target, prev_target):
    prev_target = target
    target = handle.garbages.pop(0)    