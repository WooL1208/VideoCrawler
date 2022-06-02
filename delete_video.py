from shutil import copyfile
import cv2
import os

data_path = 'data/shock/'
file_list = os.listdir(data_path)

# 載入分類器
face_cascade = cv2.CascadeClassifier('face_detect.xml')

# 讀影片
for file in file_list:
    cap = cv2.VideoCapture(os.path.join(data_path, file))

    # Read the frame
    ret, frame = cap.read()

    # 轉成灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 偵測臉部
    faces = face_cascade.detectMultiScale(
                                        gray,
                                        scaleFactor = 1.1,
                                        minNeighbors = 10,
                                        minSize=(25, 25))

    # 繪製人臉部份的方框
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    # 按下ESC結束程式執行
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
    cap.release()
    #沒人臉刪除
    if len(faces) != 1:
        try:
            os.remove(os.path.join(data_path, file))
        except OSError as e:
            print(f"Error:{ e.strerror}")

# Release the VideoCapture object     
cv2.destroyAllWindows()