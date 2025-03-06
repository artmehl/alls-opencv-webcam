import cv2
import time
import os

width = 1280
height = 720

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cap.grab()
start_time = time.time()
start_cap = time.time()
ret, frame = cap.read()
end_cap = time.time()
if not ret:
    print("Erro ao capturar o frame.")
start_save = time.time()
cv2.imwrite(f'frame.jpg', frame)
end_save = time.time()
print(f"Captura: {end_cap - start_cap} | Save: {end_save - start_save}")
end_time = time.time()
print(f"Levou: {end_time - start_time}")
cap.release()
