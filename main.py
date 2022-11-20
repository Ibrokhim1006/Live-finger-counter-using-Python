import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_Hands = mp.solutions.hands

hands = mp_Hands.Hands()

mpDraw = mp.solutions.drawing_utils

finger_Coor = [(8, 6), (12, 10), (16, 14), (20, 18)]

thumb_Coor = (4,2)

while True:
    
    success,image = cap.read()

    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = hands.process(RGB_image)

    multiLandMarks = result.multi_hand_landmarks

    if multiLandMarks:
        
        handList = []
        
        for handLms in multiLandMarks:
            
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            
            for idx, lm in enumerate(handLms.landmark):
                
                h, w, c = image.shape
                
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                handList.append((cx, cy))
                for point in handList:
                    cv2.circle(image, point, 10,  (255, 255, 0), cv2.FILLED)
                upCount = 0
        for coordinate in finger_Coor:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        if handList[thumb_Coor[0]][0] > handList[thumb_Coor[1]][0]:
                upCount += 1
        cv2.putText(image, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)

    cv2.imshow("Counting number of fingers", image)
    cv2.waitKey(1)