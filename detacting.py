import cv2
import numpy as np

img1 = cv2.imread('C:/Users/jyj98/Desktop/Realsense/Mashroom_right.jpg',cv2.IMREAD_COLOR)


# cv_img =

while True:

    key = cv2.waitKey(1) & 0xff
    if key == 27:  # Esc


        break

cv2.destroyAllWindows()