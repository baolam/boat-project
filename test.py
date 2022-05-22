import threading
import serial
import time

##### Config arduino port
arduino = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


def recv():    
    time.sleep(3.0)
    checked = True
    print ("Arduino ui! Ban con song khong")
    arduino.write(bytes("Start arduino\n", "utf-8"))
    time.sleep(0.2)
    while True:
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').rstrip()
            print (received_data)
            
            
threading.Thread(name="arduino", target=recv, daemon=True).start()

while True:
    n=input()
    arduino.write(bytes(n, 'utf-8'))
        