import cv2
import time
import os
import serial
import pynmea2
import csv

def create_csv(csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

def write_csv(csv_file, data):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    

duration = 10
fps = 10.0
width = 1280
height = 720
port = "/dev/ttyACM0"
#filename = "output/teste.mp4"
filename = 'teste'
limit_n_frames = (fps * duration)
last_lat = "0.0"
last_long = "0.0"

header = ['n_frame', 'Latitude', 'Longitude']
create_csv(f'output/{filename}.csv')

serial_gps = serial.Serial(port)

if not os.path.exists('output'):
    os.makedirs('output')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f'output/{filename}.mp4', fourcc, fps, (width, height))

n_frames = 0
start_time = time.time()

while (n_frames < limit_n_frames):
    if not serial_gps.isOpen():
        serial_gps.open()
    line = serial_gps.readline().decode()
    if (line.find('GGA') > 0):
        msg = pynmea2.parse(line)
        lat = msg.latitude
        long = msg.longitude
        print(f"Lat: {lat} | Long: {long}")
        if (last_lat != lat) and (last_long != long):
            last_lat = lat
            last_long = long
    serial_gps.close()
    print(f"Frame - {n_frames}")
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o frame.")
        break
    out.write(frame)
    data = [n_frames, last_lat, last_long]
    write_csv(f'output/{filename}.csv', data)
    n_frames+=1

cap.release()
out.release()

end_time = time.time()
print(f"Levou: {end_time - start_time}")
print(f"Video salvo em {filename}.")
