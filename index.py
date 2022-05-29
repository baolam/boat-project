import cv2
import time
import socketio
import serial
import threading
import math

from src import Read, MatrixPoint
from src import request_to_server
from src import bfs_get_x_nearest, goes_to_home
from src import depthmeasurement
from src import control
from src import change_depthmeausement_deg_into_ij, get_degree_depend_on_image

SERVER = "http://boat-project.herokuapp.com"
WIDTH = 416
HEIGHT = 416
NAMESPACE = "/device"

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

socket = socketio.Client()

video = cv2.VideoCapture(0)
infor = Read(socket, arduino, NAMESPACE)
matrixpoint = MatrixPoint(gps, arduino)

def speed(sp):
  matrixpoint.motor = sp

def is_full():
  matrixpoint.is_full = 0

def journey(infor):
  """Tạo hành trình sẵn cho thuyền. Công việc này được thực hiện đầu tiên, trước khi thực hiện việc khác, không sẽ bị lỗi

  Args:
    infor (_type_): _description_
  """
  wb = infor["wb"]
  hb = infor["hb"]
  
  if wb % matrixpoint.w == 0 and hb % matrixpoint.h == 0:
    matrixpoint.row_matrix = int(wb / matrixpoint.w)
    matrixpoint.col_matrix = int(hb / matrixpoint.h)
    matrixpoint(matrixpoint.lng_st, matrixpoint.lat_st)

def control(left):
  i, j = matrixpoint.current_pos
  if left and i >= 1 and matrixpoint.matrix[i-1][j] != MatrixPoint.WARNING_VC:
    control(arduino, 0, left)
  if not left and i <= matrixpoint.row_matrix - 1 \
    and matrixpoint.matrix[i-1][j] != MatrixPoint.WARNING_VC:
    control(arduino, 0, left)
  
def classify(resp):
  print (resp)
  
  matrixpoint.is_full += len(resp)
  # Vẽ vào ma trận điểm
  
  for x, y, w, h in resp:
    dis = depthmeasurement(w)
    deg, left_right = get_degree_depend_on_image(x, y, w, h, WIDTH)
    th1, th2 = change_depthmeausement_deg_into_ij(matrixpoint.prev, matrixpoint.current_pos, dis, deg)
    i, j = math.floor(th1[0]), math.floor(th2[0])
    if th2[2] == left_right:
      # Cập nhập theo trường hợp này
      i, j = math.floor(th2[0]), math.floor(th2[1])
    matrixpoint.matrix[i][j] = MatrixPoint.PRIORITY
    
def run_socket():
  socket.on("speed", handler=speed, namespace=NAMESPACE)
  socket.on("classify", handler=classify, namespace=NAMESPACE)
  socket.on("journey", handler=journey, namespace=NAMESPACE)
  socket.on("direction", handler=control, namespace=NAMESPACE)
  socket.connect(SERVER, namespaces=NAMESPACE)

threading.Thread(name="socket", target=run_socket, daemon=True).start()
c = 0

while True:
  __, frame = video.read()
  c += 1
  if c % 3 == 0:
    c = 0
    request_to_server(img, SERVER)
  if matrixpoint.is_trace == 0:
    i, j = matrixpoint.current_pos
    
    if matrixpoint.meet >= matrixpoint.is_full:
      st, trace = goes_to_home(matrixpoint.matrix, i, j)
      threading.Thread(name="tracing", target=matrixpoint.trace, args=(trace,), daemon=True).start()      
    else:
      st, trace = bfs_get_x_nearest(matrixpoint.matrix, MatrixPoint.PRIORITY, i, j)
      if st:
        threading.Thread(name="tracing", target=matrixpoint.trace, args=(trace,), daemon=True).start()
      else:
        st, trace = bfs_get_x_nearest(matrixpoint.matrix, MatrixPoint.NOT_VISITED, i, j)
        if st:
          threading.Thread(name="tracing", target=matrixpoint.trace, args=(trace,), daemon=True).start()
        else:
          st, trace = goes_to_home(matrixpoint.matrix, i, j)
          threading.Thread(name="tracing", target=matrixpoint.trace, args=(trace,), daemon=True).start()