'''
    先用delete_video.py篩選
    擷取人臉部分另存影片
'''
from shutil import copyfile
import cv2
import os

data_path = 'data/shock/'
file_list = os.listdir(data_path)
output_path = 'output/'

if not os.path.exists(output_path):
    os.makedirs(output_path)

# 載入分類器
face_cascade = cv2.CascadeClassifier('face_detect.xml')

# 讀影片
for file in file_list:
    cap = cv2.VideoCapture(os.path.join(data_path, file))
    outputCounter = 0
    position = True
    while True:
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break
        # 轉成灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 偵測臉部
        faces = face_cascade.detectMultiScale(
                                            gray,
                                            scaleFactor = 1.1,
                                            minNeighbors = 30,
                                            minSize=(25, 25))

        # 擷取人臉部份        
        for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            hasFace = True
            if position == True:
                px, py, pw, ph = x - 30, y - 30, w + 60, h + 60
                position = False
                file = file.replace('.mp4', '')
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter('%s/%s.mp4' % (output_path, file), fourcc, 20.0, (pw, ph))
        
            crop = frame[y:y + ph, x:x + pw]
            out.write(crop)

# Release the VideoCapture object
cap.release()     
out.release()
cv2.destroyAllWindows()