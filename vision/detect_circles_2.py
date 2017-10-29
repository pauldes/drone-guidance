##########################
#
#  FROM https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
#Usage:
#python detect_circles.py img.png

# import the necessary packages
import numpy as np
import cv2
import sys

if len(sys.argv) != 2:
    print("Error! Program usage:")
    print("python detect_circles_2.py <image_circles_path>")
    exit()

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(sys.argv[1])
output = image.copy()
img = image.copy()

#from https://pythonprogramming.net/color-filter-python-opencv-tutorial/
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#TODO: still need adjustments
lower_red = np.array([0,120,50])
upper_red = np.array([40,220,150])
# H: 0 - 180, S: 0 - 255, V: 0 - 255
mask = cv2.inRange(hsv, lower_red, upper_red)
img = cv2.bitwise_and(image,image, mask= mask)
#######################################
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50,param2=30,minRadius=50,maxRadius=200)

# ensure at least some circles were found
if circles is not None:
  # convert the (x, y) coordinates and radius of the circles to integers
  circles = np.round(circles[0, :]).astype("int")

  #Paul: find biggest r
  biggest_r  = 0
  biggest_circle = {0,0,0}

  for (x, y, r) in circles:
    if(r>biggest_r):
      biggest_circle = {x,y,r}
      biggest_r = r

  cv2.circle(output, (x, y), r, (0, 255, 0), 4)
  cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

  cv2.namedWindow("output", cv2.WINDOW_NORMAL)
  cv2.imshow("output", np.hstack([image, output]))

else:
  print('No circles were found!')
  cv2.namedWindow("img", cv2.WINDOW_NORMAL)
  cv2.imshow("img", img)

cv2.waitKey(0)
