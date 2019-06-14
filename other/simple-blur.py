import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('bonen/Image__2019-04-29__03-03-16.bmp')
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

kernel = np.ones((3,3), np.float32)*-1
kernel[1][1] = 12
dst = cv2.filter2D(img, -1, kernel)

print(kernel)

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()
