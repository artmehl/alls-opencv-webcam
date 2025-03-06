import cv2
import time
import os

duration = 60
fps = 10.0
width = 1920
height = 1080
filename = "output/teste_7.mp4"
limit_n_frames = (fps * duration)

if not os.path.exists('output'):
    os.makedirs('output')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

n_frames = 0
start_time = time.time()

while (n_frames < limit_n_frames):
    start_cap = time.time()
    ret, frame = cap.read()
    end_cap = time.time()
    if not ret:
        print("Erro ao capturar o frame.")
        break
    start_save = time.time()
    out.write(frame)
    end_save = time.time()
    print(f"Frame - {n_frames} | Captura: {end_cap - start_cap} | Save: {end_save - start_save}")
    n_frames+=1

cap.release()
out.release()

end_time = time.time()
print(f"Levou: {end_time - start_time}")
print(f"Video salvo em {filename}.")
