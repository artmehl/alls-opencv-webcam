import cv2
import time
import os
import serial
import pynmea2

duration = 10
fps = 10.0
width = 1280
height = 720
filename = "output/teste.mp4"
output_folder = 'photo_teste/'
limit_n_frames = (fps * duration)
#port = '/dev/ttyACM0'
#last_lat = "0.0"
#last_long = "0.0"

#serial_gps = serial.Serial(port)

if not os.path.exists('output'):
    os.makedirs('output')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
cap.grab()
n_frames = 0
start_time = time.time()
while n_frames < limit_n_frames:
    #line = serial_gps.readline().decode()
    #if (line.find('GGA') > 0):
        #msg = pynmea2.parse(line)
        #lat = msg.latitude
        #long = msg.longitude
        #print(f"Lat: {lat} | Long: {long}")
        #if (last_lat != lat) and (last_long != long):
            #last_lat = lat
            #last_long = long
    start_cap = time.time()
    ret, frame = cap.read()
    end_cap = time.time()
    if not ret:
        print("Erro ao capturar o frame.")
    start_save = time.time()
    #out.imwrite(frame)
    #cv2.imwrite(f'{output_folder}frame{n_frames}_{last_lat}_{last_long}.png', frame)
    cv2.imwrite(f'{output_folder}frame{n_frames}.jpg', frame)
    end_save = time.time()
    print(f"Frame - {n_frames} | Captura: {end_cap - start_cap} | Save: {end_save - start_save} | Total: {(end_cap - start_cap) + (end_save - start_save)}")
    n_frames+=1

cap.release()
#out.release()

end_time = time.time()
print(f"Levou: {end_time - start_time}")
