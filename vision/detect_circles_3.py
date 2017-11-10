'''
P.Désigaud
INSA Lyon
github.com/pauldes
A python algorithm using OpenCV's Hough Circles method to find a red circle in a picture
Optimized for a 720p cheap camera (webcam, Parrot AR Drone)
'''

# import the necessary packages
import numpy as np
import cv2
import sys

if len(sys.argv) != 2:
    print("Error! Program usage:")
    print("python detect_circles_2.py <image_circles_path>")
    exit()

# Load the image
bgr    = cv2.imread(sys.argv[1])
output = bgr.copy()



#Convert to HSV color space
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

# Red range 1 (hue from 0 to 40)
lower_red1 = np.array([0,120,50])
upper_red1 = np.array([40,220,150])
# Red range 2 (hue from 140 to 180)
lower_red2 = np.array([140,120,50])
upper_red2 = np.array([180,220,150])
# H: 0 - 180, S: 0 - 255, V: 0 - 255

#Creating the color masks
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1|mask2

mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)[1]

mask = cv2.GaussianBlur(mask,(5,5),0)

circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, minDist=5, param1=50,param2=30,minRadius=20,maxRadius=200)

if circles is not None:

    for i in circles[0]:
        x = i[0]
        y = i[1]
        r = i[2]
        cv2.circle(output, (x, y), r, (255, 0, 0), 2)

else:
  print('No circles were found!')

cv2.circle(output, (int(output.shape[1]/2),int(output.shape[0]/2)), 20, (255, 0, 0), 2)
cv2.circle(output, (int(output.shape[1]/2),int(output.shape[0]/2)), 200, (255, 255, 0), 2)

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.imshow("output", output)

cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
cv2.imshow("mask", mask)

cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
cv2.imshow("hsv", hsv)
cv2.waitKey(0)
