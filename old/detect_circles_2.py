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
image = cv2.imread(sys.argv[1])
output = image.copy()

#Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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

#Apply the mask to the image
img = cv2.bitwise_and(image,image, mask= mask)
#Surprisingly it works when using only one mask:
#img = cv2.bitwise_and(image,image, mask= mask1)

#Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the circles
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50,param2=30,minRadius=50,maxRadius=200)

# Ensure at least 1 circle was found
if circles is not None:

  # Convert the (x, y) coordinates and radius of the circles to integers
  circles = np.round(circles[0, :]).astype("int")

  biggest_circle_r  = 0
  biggest_circle_x = 0
  biggest_circle_y = 0

  #Iterating through the circles found
  for (x, y, r) in circles:

    #Look for the biggest circle
    if(r>biggest_circle_r):
      biggest_circle_r = r
      biggest_circle_x = x
      biggest_circle_y = y
    # Draw the circle
    cv2.circle(output, (x, y), r, (255, 0, 0), 2)
    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

  #Draw the biggest circle
  cv2.circle(output, (biggest_circle_x, biggest_circle_y), biggest_circle_r, (0, 255, 0), 4)
  cv2.rectangle(output, (biggest_circle_x - 5, biggest_circle_y - 5), (biggest_circle_x + 5, biggest_circle_y + 5), (0, 128, 255), -1)

  #Draw input and output image
  cv2.namedWindow("output", cv2.WINDOW_NORMAL)
  cv2.imshow("output", np.hstack([image, output]))

else:
  print('No circles were found!')

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow("img", img)
cv2.namedWindow("gray", cv2.WINDOW_NORMAL)
cv2.imshow("gray", gray)

cv2.waitKey(0)
