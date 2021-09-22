import cv2
import time
import numpy as np

#To save output in a file (output.avi)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

# Starting the camera
cap = cv2.VideoCapture(0)
# Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

# Capturing the background for 60 frames
for i in range(60):
    ret, bg = cap.read()

# Flipping the background
bg = np.flip(bg, axis = 1)

# Reading the captured frame until the camera is open
while(cap.isOpened()):
    ret, img = cap.read()
    if(not ret):
        break
    #Flipping the image
    img = np.flip(img, axis = 1)

    # Converting the color from RBG to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Generating mask to detect red color
    # Values can be changed as per the color choice

    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])

    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])

    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    # Open and expand image where there is mask 1

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    # Selecting the part without mask 1 and saving that in mask 2

    mask_2 = cv2.bitwise_not(mask_1)

    # Keeping only the part of the image without the red color
    res_1 = cv2.bitwise_and(img, img, mask = mask_2)

    # Keeping i=only the part of the image WITH the red color
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)

    # Generating Final output by merging Res 1 and Res 2
    final_ouput = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_ouput)

    # Displaying output to the user
    cv2.imshow("Magic!", final_ouput)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
