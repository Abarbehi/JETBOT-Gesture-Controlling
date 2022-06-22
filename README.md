# JETBOT-Gesture-Controlling

This project aims to control a jetBot robot with hand gestures remotely and the video feed of the Jetson Nano. The robot will go forward, backward, left and right by detecting different hand gestures . Hand gestures are an aspect of body language that can be conveyed through the center of the palm, the finger position and the shape constructed by the hand. Hand gestures can be classified into static and dynamic. As its name implies, the static gesture refers to the stable shape of the hand, whereas the dynamic gesture comprises a series of hand movements such as waving. In this project we will only deal with static gestures to move the robot .
Using a computer connected to the same network as the Jetson, the JETBOT interface can be connected to through its IP-adress. Jupyter there displays Notebooks possible to run and where the one of this project can be added.
The notebook in this project uses a TCP socket hosted on the Jetson, making it possible for a client to connect and send command on how to steer the robot. Camera feed from the Jetson is also shown through the Notebook using a widget display.

you can watch the video here :
https://youtu.be/7WTCdcV6jAg

# Table of Contents
- Setup / Software Requirements
- Usage Instructions
- Maintainers

#  Setup / Software Requirements
After setting up the jetbot which is completely explained in waveshare website, upload the file JetBot.ipynb into the JetBot and run all the Cells. On the client side in computer run the main.py file. if you come up with errors, The istruction of how to deal with cvzone is completely explained in this video:
https://www.youtube.com/watch?v=3xfOa4yeOb0

https://www.computervision.zone/

# Usage Instructions

The JetBot works in 2 modes, STOPMODE and DRIVEMODE .if you raise both of your hand and show your palm with your fingers open, it goes into  STOPMODE ; if you show "V sign" with both of your hands, it will get into Drive mode. In STOPMODE if you close all of one hand's fingers and the other hand wide open Jetbot will turn in the direction of the closed hand in its place. In DRIVEMODE left hand is used for acceleration and right hand is used for changing direction, if left had thumb is up the robot will go forward and if the thumb is down it will go downward. If the left-hand's thumb points to other directions (left or right) it won't move. While the left hand is used for acceleration the right hand is used for direction, if the right hand's thumb is up it will go straight and if the thumb is left or right it will go into that direction.
