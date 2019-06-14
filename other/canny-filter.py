import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('bonen/Image__2019-04-29__03-03-16.bmp')
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

edges = cv2.Canny(img, 50, 200)
kernel = np.ones((3, 3), np.uint8)
eroded = edges
eroded = cv2.morphologyEx(eroded, cv2.MORPH_CLOSE, kernel, iterations=8)
eroded = cv2.dilate(eroded, kernel, iterations=2)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(eroded, cmap='gray')
plt.title('Eroded'), plt.xticks([]), plt.yticks([])

plt.show()
