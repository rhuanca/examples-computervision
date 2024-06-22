import cv2
import cvzone 
from cvzone.HandTrackingModule import HandDetector
import time
import random


cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]

while True:
    imgBG = cv2.imread("resources/BG.png")
    
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]


    # find hands
    hands, img = detector.findHands(imgScaled) # with draw

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    playerMove = None
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1

                    if fingers == [1,1,1,1,1]:
                        playerMove = 2

                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randonNumber = random.randint(1,3)
                    imgAI = cv2.imread(f'resources/{randonNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # player wins
                    if (playerMove==1 and randonNumber==3) or \
                        (playerMove==2 and randonNumber==1) or \
                        (playerMove==3 and randonNumber==2):
                        scores[1] += 1

                    # AI wins
                    if (playerMove==3 and randonNumber==1) or \
                        (playerMove==1 and randonNumber==2) or \
                        (playerMove==2 and randonNumber==3):
                        scores[0] += 1



    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))


    cv2.putText(imgBG, str(int(scores[0])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)
    cv2.putText(imgBG, str(int(scores[1])), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False


