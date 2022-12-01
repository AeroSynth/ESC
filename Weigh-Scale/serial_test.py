import sys,os
import serial
import serial.tools.list_ports

def open_ser():
    global comport, b, p,a
    baudrate = 115200#57600
    comport = 'COM1'
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print('p in ports',p)
        b=str(p)
        print('string',p)
    
        if b.find("USB") >=0:
            a=b.find("USB")
            print('a=',a)
            comport = b[a:a+4]
            comport='/dev/tty'+comport
            print("USB at ",comport)
            print('baudrate= ',baudrate)
            break

    print('final',comport)
    #comport = '/dev/ttyUSB0'
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = comport
    ser.timeout = 2
    try:
        ser.open()
    except:
        print("Error.  Incorrect COM port or baud rate")
        sys.exit()
    return ser

ser = open_ser()
