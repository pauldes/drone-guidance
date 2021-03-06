def main(input_image_url):

  # Load the image
  bgr    = cv2.imread(input_image_url)
  output = bgr.copy()

  #Convert to HSV color space
  hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

  # Red range 1 (hue from 0 to 40)
  lower_red1 = np.array([0,120,50])
  upper_red1 = np.array([40,220,200])
  # Red range 2 (hue from 140 to 180)
  lower_red2 = np.array([140,120,50])
  upper_red2 = np.array([180,220,200])
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
  mask = cv2.GaussianBlur(mask,(5,5),100,100)


  # Setup SimpleBlobDetector parameters.
  params = cv2.SimpleBlobDetector_Params()
  # params.minThreshold = 10;
  # params.maxThreshold = 200;
  params.filterByArea = False
  # params.minArea = 1500
  params.filterByCircularity = False
  # params.minCircularity = 0.1
  params.filterByConvexity = False
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

  MAX_BLOB_RADIUS = 720
  MIN_BLOB_RADIUS = 14

  if len(blobs) >0:
    #print(str(len(blobs))+' blobs found')

    biggest_blob_r  = 0
    biggest_blob_x  = 0
    biggest_blob_y  = 0

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
          cv2.circle(mask, (x, y), r, (0, 225, 0), 2)

    if(biggest_blob_r>0):
      # Compute distance to center
      vector_y = - output.shape[0]/2 + biggest_blob_y
      vector_x = - output.shape[1]/2 + biggest_blob_x
      #Print as JSON
      print('{"vx":'+str(int(vector_x))+', "vy":'+str(int(vector_y))+' , "r": '+str(biggest_blob_r)+ '}')
      #Draw the biggest circle
      cv2.circle(output, (biggest_blob_x, biggest_blob_y), biggest_blob_r, (0, 255, 0), 2)
      #Draw line from image center to biggest cercle center
      cv2.line(output,(int(output.shape[1]/2),int(output.shape[0]/2)),(biggest_blob_x,biggest_blob_y),(0,255,0),2)


      #Treshold print for presentation

      # TRESHOLD_X = 100
      # TRESHOLD_RADIUS = 40
      # EPSILON_RADIUS = 10
      # cv2.circle(output, (biggest_blob_x, biggest_blob_y), TRESHOLD_RADIUS - EPSILON_RADIUS, (255, 255, 0), 2)
      # cv2.circle(output, (biggest_blob_x, biggest_blob_y), TRESHOLD_RADIUS + EPSILON_RADIUS, (255, 255, 0), 2)
      # cv2.line(output,(int(output.shape[1]/2) + TRESHOLD_X, 0),(int(output.shape[1]/2) + TRESHOLD_X, output.shape[0]),(0,255,255),2)
      # cv2.line(output,(int(output.shape[1]/2) - TRESHOLD_X, 0),(int(output.shape[1]/2) - TRESHOLD_X, output.shape[0]),(0,255,255),2)

    else:
      print('OUTRANGE_BLOB')

  else:
    print('NOTHING_FOUND')

  cv2.namedWindow("output", cv2.WINDOW_NORMAL)
  cv2.imshow("output", output)

  # Intermadiate images show and save
  
  # cv2.imwrite('output.png',output)
  # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
  # cv2.imshow("mask", mask)
  # cv2.imwrite('mask.png',mask)
  # cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
  # cv2.imshow("hsv", hsv)
  # cv2.imwrite('hsv.png',hsv)


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
      sys.stdout.flush()
      cv2.waitKey(int(sys.argv[2]))
