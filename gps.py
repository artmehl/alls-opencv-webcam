import serial
import pynmea2

ser = serial.Serial('/dev/ttyACM0')  # open serial port
arrayChar = []

while True:
    line = ser.readline().decode()
    if (line.find('GGA') > 0):
        msg = pynmea2.parse(line)
        print(msg) # print message
        print(f't:{msg.timestamp} - Lat: {msg.latitude} - Lon: {msg.longitude}')
