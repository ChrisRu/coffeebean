import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('./bonen/Image__2019-04-29__03-03-16.bmp')
img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret,img = cv2.threshold(img2, 240, 255, cv2.THRESH_TOZERO)

plt.subplot(121),plt.imshow(img2,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

plt.subplot(122),plt.imshow(img,cmap = 'gray')
plt.title('New Image'), plt.xticks([]), plt.yticks([])

color = ('b','g','r')
for i,col in enumerate(color):
 histr = cv2.calcHist([img],[i],None,[256],[0,256])
 plt.plot(histr,color = col)
 plt.xlim([0,256])
plt.show()
