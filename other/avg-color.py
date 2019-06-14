import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

image = cv2.imread('bonen/Image__2019-04-29__03-03-16.bmp')
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

lower_colors = np.array([180, 0, 0])
upper_colors = np.array([250, 250, 250])
mask = cv2.inRange(img, lower_colors, upper_colors)
edges = cv2.Canny(img, 50, 200)
kernel = np.ones((3, 3), np.uint8)
eroded = edges
eroded = cv2.morphologyEx(eroded, cv2.MORPH_CLOSE, kernel, iterations=8)
eroded = cv2.dilate(eroded, kernel, iterations=4)
newMask = cv2.subtract(mask, eroded)
newMask = cv2.morphologyEx(newMask, cv2.MORPH_OPEN, kernel, iterations=8)

color = np.zeros((300, 300, 3), np.uint8)
# Fill image with red color(set each pixel to red)
avgColor = cv2.mean(img, mask)
color[:] = avgColor[0:3]

gs = gridspec.GridSpec(2, 2)

plt.figure()
plt.subplot(gs[0, 0]), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.plot([0, 1])

plt.subplot(gs[0, 1]), plt.imshow(mask, cmap='gray')
plt.title('Mask:'), plt.xticks([]), plt.yticks([])
plt.plot([0, 1])

plt.subplot(gs[1, :]), plt.imshow(color, cmap='gray')
plt.title('Average color:'), plt.xticks([]), plt.yticks([])
plt.plot([0, 1])

plt.show()
