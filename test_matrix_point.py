from src import MatrixPoint
import serial
import socketio

SERVER = "http://localhost:3000"
NAMESPACE = "/device"
gps = serial.Serial(
  port = "COM12",
  baudrate = 9600,
  timeout = 0.5
)

def journey(infor):
  global NAMESPACE
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
    # print(matrixpoint.matrix)
  else:
    socket.emit("cannot_update_journey", namespace=NAMESPACE)

socket = socketio.Client()
socket.on("journey", handler=journey, namespace=NAMESPACE)
matrixpoint = MatrixPoint(socket, NAMESPACE, gps, None)
socket.connect(SERVER, namespaces=NAMESPACE)