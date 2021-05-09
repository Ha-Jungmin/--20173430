!pip install opencv-python mediapipe

import mediapipe as mp
import cv2
import math

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

#영상을 불러오는 부분
cap = cv2.VideoCapture("C:/Users/jungm/Desktop/walk.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    distance = 0
    if ret:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
    
        if results.pose_landmarks:
            lmList = []
            results = pose.process(frame)
        
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        
            if any(26 in l for l in lmList):
                rightknee_x, rightknee_y = lmList[26][1], lmList[26][2]
                leftknee_x, leftknee_y = lmList[25][1], lmList[25][2]
    
                distance = math.sqrt(math.pow((rightknee_y - leftknee_y),2) + math.pow((rightknee_x - leftknee_x),2))
                print(lmList[25], lmList[26]) 
        if distance < 10:
            cv2.putText(frame,"Go", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
            
        if distance > 10:
            cv2.putText(frame,"STOP", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
            cv2.waitKey(10)
    
        cv2.imshow('detect_object', frame)
        
    else:
        break
            
cap.release()
cv2.destroyAllWindows()
