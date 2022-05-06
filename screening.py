from shutil import copyfile
import cv2
import os

data_path = 'data/shock/'
file_list = os.listdir(data_path)
#output_path = 'output/'

'''
if not os.path.exists(output_path):
    os.makedirs(output_path)
'''

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
    '''
    依人臉裁切存影片要求每一個frame的size要一致，目前想不到怎搞
    '''
    for (x, y, w, h) in faces:
        '''
        x_l, x_r = x - 50, x + w + 50
        y_u, y_d = y - 50, y + h + 50
        '''
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        '''
        if len(faces) == 1:

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('%s/output_%s.mp4' % (output_path, file), fourcc, 20.0, (w + 100, h + 100))
            
            crop = frame[y_u:y_d, x_l:x_r]
            out.write(crop)
        '''
    '''   
    if len(faces) == 1:
        copyfile(os.path.join(data_path, file), os.path.join(output_path, file))
    '''
    
    '''
    # 顯示成果
    cv2.imshow('img', frame)
    #計算找到幾張臉
    print("找到了 {0} 張臉.".format(len(faces)))
    '''
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
#out.release()
cv2.destroyAllWindows()