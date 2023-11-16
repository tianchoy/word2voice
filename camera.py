import cv2  
  
# 打开摄像头，0表示第一个摄像头  
cap = cv2.VideoCapture(0)  
  
while True:  
    # 从摄像头读取一帧图像  
    ret, frame = cap.read()  
  
    # 显示图像  
    cv2.imshow('Camera Feed', frame)  
  
    # 等待1毫秒，如果q被按下，那么退出循环  
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  
  
# 释放摄像头并销毁所有窗口  
cap.release()  
cv2.destroyAllWindows()