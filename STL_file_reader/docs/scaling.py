import cv2 as cv
import numpy as np

W, H = 1500, 1000

img: np.ndarray = cv.imread("img.png")
width = (img.shape[1] - W) // 2
height = (img.shape[0] - H) // 2
new = img[height:H + height, width:W + width]
print(new.shape)

cv.imshow("img", new)
cv.imwrite("img_.png", new)
cv.waitKey()

