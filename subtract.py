import cv2
import numpy as np

img1 = cv2.imread('C:/Users/jyj98/Desktop/Realsense/Mashroom/non_mash0.jpg', cv2.IMREAD_COLOR)
img2 = cv2.imread('C:/Users/jyj98/Desktop/Realsense/Mashroom/three_mash0.jpg', cv2.IMREAD_COLOR)

# img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
# img2 =cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)
cv_abs = cv2.subtract(img2, img1)
# cv_abs = cv2.absdiff(img2, img1)

# cv_abs = cv2.bitwise_not(cv_abs)
# cv_canny = cv2.Canny(cv_ash, 0, 200)
# mask = np.zeros(cv_abs.shape,np.uint8)
# cv2.drawContours(mask,[cnt])
# cv_mean = cv2.mean(cv_sub,mask=mask)
# k = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
cv_ash = cv2.cvtColor(cv_abs,cv2.COLOR_RGB2GRAY)
# cv_img1_ash = cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
# cv_img2_ash = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)


# erode = cv2.bitwise_not(cv_abs)
# cv_abs1 =cv2.convertScaleAbs(cv_abs)
# edge = cv2.Laplacian(cv_abs, -1)
# ret ,cv_thresh = cv2.threshold(cv_ash,0,255,cv2.THRESH_OTSU)
cv_thresh = cv2.adaptiveThreshold(cv_ash,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,4)
# # edge = cv2.Scharr(cv_thresh,-1,0,1)
# gx_kernel = np.array([[1,0],[0,-1]])
# gy_kernel = np.array([[0,1],[-1,0]])
# edge = cv2.filter2D(cv_abs,-1,gx_kernel)
# edge_1 = cv2.filter2D(cv_abs,-1,gy_kernel)
# edge_gray = cv2.cvtColor(edge,cv2.COLOR_RGB2GRAY)

# contours,ret = cv2.findContours(cv_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# cv2.drawContours(cv_abs, contours, 1, (255, 0, 0), 3)
edge = cv2.Canny(cv_thresh,0,200)
kernel = np.ones((7,7),np.uint8)
result = cv2.dilate(edge,cv_thresh,iterations=1)
# def noting(pos):
#     pass
# cv2.namedWindow("Canny Edge")
# cv2.createTrackbar('low threshold', 'Canny Edge', 0, 1000, noting)
# cv2.createTrackbar('high threshold', 'Canny Edge', 0, 1000, lambda x : x)
#
# cv2.setTrackbarPos('low threshold', 'Canny Edge', 50)
# cv2.setTrackbarPos('high threshold', 'Canny Edge', 150)
# cv_abs = np.hstack([cv_abs,cv_abs_copy])
# cv_abs = np.hstack([cv_abs,cv_sub])
result= np.dstack([result,result,result])
result = cv2.bitwise_not(result)

cv_sub =cv2.subtract(cv_abs,result)

# img_hsv = cv2.cvtColor(cv_sub,cv2.COLOR_RGB2HSV)
# h,s,v = cv2.split(img_hsv)
# equal = cv2.equalizeHist(v)
# hsv2 = cv2.merge([h,s,equal])
# yCrCb = cv2.cvtColor(hsv2,cv2.COLOR_HSV2BGR)
# y,Cr,Cb = cv2.split(yCrCb)
# equalize = cv2.equalizeHist(y)
# yCrCb2 = cv2.merge([equalize,Cr,Cb])
# yCrCb2 = cv2.cvtColor(yCrCb2,cv2.COLOR_YCrCb2RGB)

while True:

    cv2.imshow('cv_Gaussian',cv_sub)
    # cv2.imshow('cv_sub',cv_sub)
    # cv2.imshow('canny', cv_canny)
    # cv2.imshow('contour',contours)
    # cv2.imshow('cv_erode',erode)
    # cv2.imshow('thresh', cv_thresh)
    # cv2.imshow('la', edge)
    # cv2.imshow('hsv',hsv2)
    # cv2.imshow('laa',edge_1)
    # cv2.imshow('aa',img1)
    # cv2.imshow('bb',img2)
    # low = cv2.getTrackbarPos('low threshold', 'Canny Edge')
    # high = cv2.getTrackbarPos('high threshold', 'Canny Edge')
    #
    # img_canny = cv2.Canny(cv_ash, low, high)
    # cv2.imshow("Canny Edge", img_canny)

    key = cv2.waitKey(1) & 0xff
    if key == 27:  # Esc
        # cv2.imwrite('C:/Users/jyj98/Desktop/Realsense/subtract_canny_left.jpg', cv_canny)
        # cv2.imwrite('C:/Users/jyj98/Desktop/Realsense/subtract_abs_left.jpg', cv_abs)

        break

cv2.destroyAllWindows()
