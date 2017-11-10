def main(input_image_url):

  # Load the image
  bgr    = cv2.imread(input_image_url)
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

  #Invert black and white
  mask=cv2.bitwise_not(mask)
  # Now the target is black and background is white
  # Blur slightly
  mask = cv2.GaussianBlur(mask,(5,5),0)


  # Setup SimpleBlobDetector parameters.
  params = cv2.SimpleBlobDetector_Params()
  # params.minThreshold = 10;
  # params.maxThreshold = 200;
  # params.filterByArea = True
  # params.minArea = 1500
  # params.filterByCircularity = True
  # params.minCircularity = 0.1
  # params.filterByConvexity = True
  # params.minConvexity = 0.87
  # 0=bar, 1=circle
  params.filterByInertia = True
  params.minInertiaRatio = 0.3

  # Create a detector with the parameters
  ver = (cv2.__version__).split('.')
  if int(ver[0]) < 3 :
      detector = cv2.SimpleBlobDetector(params)
  else :
      detector = cv2.SimpleBlobDetector_create(params)

  # Find the blobs
  blobs = detector.detect(mask)

  MAX_BLOB_RADIUS = 140
  MIN_BLOB_RADIUS = 14

  if len(blobs) >0:
    #output = cv2.drawKeypoints(output, blobs, np.array([]),(0,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    print(str(len(blobs))+' blobs found')

    biggest_blob_r  = 0

    for blob in blobs:
          x = int(blob.pt[0])
          y = int(blob.pt[1])
          r = int(blob.size/2)

          #Look for the biggest circle
          if( r>biggest_blob_r and r>MIN_BLOB_RADIUS and r<MAX_BLOB_RADIUS):
            biggest_blob_r = r
            biggest_blob_x = x
            biggest_blob_y = y

          cv2.circle(output, (x, y), r, (255, 225, 255), 2)

    #Draw the biggest circle
    cv2.circle(output, (biggest_blob_x, biggest_blob_y), biggest_blob_r, (0, 255, 0), 2)

    # Compute distance to center
    vector_y = - output.shape[0]/2 + biggest_blob_y
    vector_x = - output.shape[1]/2 + biggest_blob_x

    if(biggest_blob_r>0):
      #Print as JSON
      print('{"vx":'+str(int(vector_x))+', "vy":'+str(int(vector_y))+' , "r": '+str(biggest_blob_r)+ '}')
      cv2.line(output,(int(output.shape[1]/2),int(output.shape[0]/2)),(biggest_blob_x,biggest_blob_y),(0,255,0),2)
    else:
      print('OUTRANGE_BLOB')

  else:
    print('NOTHING_FOUND')

  cv2.circle(output, (int(output.shape[1]/2),int(output.shape[0]/2)), MIN_BLOB_RADIUS, (100, 100, 100), 2)
  cv2.circle(output, (int(output.shape[1]/2),int(output.shape[0]/2)), MAX_BLOB_RADIUS, (100, 100, 100), 2)

  cv2.namedWindow("output", cv2.WINDOW_NORMAL)
  cv2.imshow("output", output)
  '''
  cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
  cv2.imshow("mask", mask)
  cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
  cv2.imshow("hsv", hsv)
  '''
  #cv2.waitKey(0)



if __name__ == "__main__":

    import numpy as np
    import cv2
    import sys

    if(len(sys.argv)!=3):
      print('Wrong number of parameters (detect_blobs.py)')
      print('Usage: python detect_blobs.py <input_image_url> <output_duration_milliseconds>')
      exit()

    else:
      main(sys.argv[1])
      cv2.waitKey(int(sys.argv[2]))

