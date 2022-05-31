import serial
import time

arduino = serial.Serial(
  port = "/dev/ttyACM1",
 #  port = "COM6",
  baudrate=9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1  
)

from src import control

time.sleep(3.5)
arduino.write(bytes("Arduino ưi! Bạn còn sống không?", "utf-8"))
time.sleep(5)
control(arduino, 0, 45, True)