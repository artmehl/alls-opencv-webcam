import cv2
import time
import os
import serial
import pynmea2
import multiprocessing

def get_gps_data(queue):
    ser = serial.Serial('/dev/ttyACM0')
    last_lat = None
    last_long = None

    while True:
        line = ser.readline().decode()
        if 'GGA' in line:
            msg = pynmea2.parse(line)
            lat = msg.latitude
            long = msg.longitude
            queue.put((lat, long))
        time.sleep(0.1)
                
def main():
    width = 1280
    height = 720
    duration = 10
    fps = 10.0
    limit_n_frames = (fps * duration)
    output_folder = 'photo_teste/'
    lat = '0.0'
    long = '0.0'
    n_frames = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=get_gps_data, args=(queue,))
    process.start()
    time.sleep(3)
    print('Started Capturing')
    
    if not os.path.exists('output'):
        os.makedirs('output')

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        exit()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.grab()

    start_time = time.time()
    while n_frames < limit_n_frames:
        if not queue.empty():
            lat, long = queue.get()
        start_cap = time.time()
        ret, frame = cap.read()
        end_cap = time.time()
        if not ret:
            print("Erro ao capturar o frame.")
        start_save = time.time()
        cv2.imwrite(f'{output_folder}frame{n_frames}_{lat}_{long}.jpg', frame)
        end_save = time.time()
        print(f"Frame - {n_frames} | Captura: {end_cap - start_cap} | Save: {end_save - start_save} | Total: {(end_cap - start_cap) + (end_save - start_save)}")
        n_frames+=1

    cap.release()
    end_time = time.time()
    process.terminate()
    print(f"Levou: {end_time - start_time}")

if __name__ == "__main__":
    main()
