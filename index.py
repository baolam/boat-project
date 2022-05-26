import cv2
import time
import socketio
import serial
import threading

from src import Read, MatrixPoint
from src import request_to_server
from src import bfs_get_x_nearest, goes_to_home
from src import depthmeasurement

SERVER = "http://boat-project.herokuapp.com"
NAMESPACE = ""
arduino = serial.Serial(
  
)

gps = serial.Serial(
  
)

socket = socketio.Client()

video = cv2.VideoCapture(0)
infor = Read(socket, arduino, NAMESPACE)
matrixpoint = MatrixPoint(gps, arduino)

def speed(sp):
  matrixpoint.motor = sp

def classify(resp):
  print (resp)

def run_socket():
  socket.on("speed", handler=speed, namespace=NAMESPACE)
  socket.on("classify", handler=classify, namespace=NAMESPACE)
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