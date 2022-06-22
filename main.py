import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import socket
import time

def mode(fingers1, fingers2):
    if fingers_left==[1,1,1,1,1] and fingers_right==[1,1,1,1,1] :
        send_data("s")
        return "stop_mode"
    elif fingers_left==[0,1,1,0,0] and fingers_right==[0,1,1,0,0] :
        return "drive_mode"
    else :
        return "no_mode_detected"
def direction_drive_mode(yb,ya,xb,xa):
    try:
        a= float((yb - ya)/(xb - xa))
    except:
        a = 9999
    atan = np.arctan(a)
    # print(atan)
    # print(lmList_right[4][0]-lmList_right[2][0])
    if xb - xa <= 0 and yb - ya < 0:
        if atan >= 0.8:
            return 'up'
    elif xb - xa >= 0 and yb - ya < 0:
        if -0.8 > atan:
            return 'up'
    if xb - xa < 0 and yb - ya < 0:
        if -0.4 < atan < 0.8:
            return 'right'
    elif xb - xa > 0 and yb - ya < 0:
        if -0.8 < atan < 0.3:
            return 'left'
def for_back_drive_mode(yb,ya,xb,xa):
    try:
        a= float((yb - ya)/(xb - xa))
    except:
        a = 9999
    atan = np.arctan(a)
    #print(atan)
    # print(lmList_right[4][0]-lmList_right[2][0])
    if xb - xa <= 0 and yb - ya < 0:
        if atan >= 0.5:
            return 'up'
    elif xb - xa >= 0 and yb - ya < 0:
        if -0.8 > atan:
            return 'up'
    if xb - xa >= 0 and yb - ya > 0:
        if atan >= 0.5:
            return 'down'
    elif xb - xa <= 0 and yb - ya > 0:
        if -0.8 > atan:
            return 'down'

def send_data(command) :
    command_to_call = command
    s.sendto(command_to_call.encode(), (HOST, PORT))

def command_valid_send_data(command) :
    if command == vol_var.last_command :
        vol_var.count+=1
    else :
        vol_var.count=0
        vol_var.last_command=command
    if vol_var.count>=2 :
        vol_var.count=0
        send_data(command)

class vol_var:
    pass
vol_var.count=0
vol_var.last_command=""


HOST = "192.168.178.28"
PORT = 2740

command_count = 0
command_to_call = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

working_mode="stop_mode"
temp="stop_mode"
mode_count=0

print("connecting...")
s.connect((HOST, PORT))
print("done!")
s.sendto(command_to_call.encode(), (HOST, PORT))
#while True:
#    command_to_call= input('letter')
#    s.sendto(command_to_call.encode(), (HOST, PORT))
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw

    if hands:
        # Hand 1
        hand = hands[0]
        if hand["type"] == "Right" :
            hand_right=hand
            lmList_right = hand["lmList"]  # List of 21 Landmarks points
            bbox_right = hand["bbox"]  # Bounding Box info x,y,w,h
            centerPoint_right = hand["center"]  # center of the hand cx,cy
            handType_right = hand["type"]  # Hand Type Left or Right
            fingers_right = detector.fingersUp(hand)
        else :
            hand_left=hand
            lmList_left = hand["lmList"]  # List of 21 Landmarks points
            bbox_left = hand["bbox"]  # Bounding Box info x,y,w,h
            centerPoint_left = hand["center"]  # center of the hand cx,cy
            handType_left = hand["type"]  # Hand Type Left or Right
            fingers_left = detector.fingersUp(hand)
    #    print(fingers1)
        #print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        #fingers1 = detector.fingersUp(hand1)
        # length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
        # length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw

        if len(hands) == 2:
            hand = hands[1]
            if hand["type"] == "Right":
                hand_right = hand
                lmList_right = hand["lmList"]  # List of 21 Landmarks points
                bbox_right = hand["bbox"]  # Bounding Box info x,y,w,h
                centerPoint_right = hand["center"]  # center of the hand cx,cy
                handType_right = hand["type"]  # Hand Type Left or Right
                fingers_right = detector.fingersUp(hand)
            else:
                hand_left = hand
                lmList_left = hand["lmList"]  # List of 21 Landmarks points
                bbox_left = hand["bbox"]  # Bounding Box info x,y,w,h
                centerPoint_left = hand["center"]  # center of the hand cx,cy
                handType_left = hand["type"]  # Hand Type Left or Right
                fingers_left = detector.fingersUp(hand)

            #finding working mode :
            current_mode=mode(fingers_left, fingers_right)
            if current_mode != "no_mode_detected" :
                if current_mode==temp:
                    mode_count+=1
                    temp=current_mode
                else :
                    mode_count = 0
                    temp = current_mode
                if  mode_count>10 :
                    working_mode=current_mode
                    mode_count=0

            if working_mode =="stop_mode" :
                if fingers_left == [1, 1, 1, 1, 1] and fingers_right == [0, 0, 0, 0, 0]  :
                   print('right')
                   command_valid_send_data("r")
                elif fingers_left == [0, 0, 0, 0, 0] and fingers_right == [1, 1, 1, 1, 1]  :
                   print('left')
                   command_valid_send_data("l")
            elif working_mode == "drive_mode":
                dirr = direction_drive_mode(lmList_right[4][1], lmList_right[2][1], lmList_right[4][0],
                                            lmList_right[2][0])
                for_back = for_back_drive_mode(lmList_left[4][1], lmList_left[2][1], lmList_left[4][0],
                                               lmList_left[2][0])
                print(for_back ," ", dirr)
                if for_back=="up" and dirr=="up":
                    command_valid_send_data("f")
                elif for_back=="down" and dirr=="up":
                    command_valid_send_data("b")
                elif for_back=="up" and dirr=="right":
                    command_valid_send_data("t")
                elif for_back=="up" and dirr=="left":
                    command_valid_send_data("u")
                elif for_back=="down" and dirr=="right":
                    command_valid_send_data("o")
                elif for_back=="down" and dirr=="left":
                    command_valid_send_data("p")
                else :
                    command_valid_send_data("s")
                #print(dirr)

            #print(fingers_left, fingers_right)
            #print(handType2)
            #print(working_mode)
            # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
            #length, info, img = detector.findDistance(centerPoint_left, centerPoint_right, img)  # with draw



    #print(working_mode)

    #cTime = time.time()
    #fps = 1 / (cTime)
    #pTime = cTime
    #flipped = cv2.flip(img, 1)
    #cv2.putText(flipped, "FPS: " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,
    #            (100, 150, 100), 2)
    #cv2.putText(flipped, "Last Mode " + working_mode, (200, 20), cv2.FONT_HERSHEY_PLAIN, 1,
    #            (100, 150, 100), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)