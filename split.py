import cv2
import numpy as np
from matplotlib import pyplot as plt


def generateMask(image):
    lowRange = (30, 0, 200)
    highRange = (180, 255, 255)

    erodeKernel = np.ones((5, 5), np.uint8)
    gaussKernel = np.ones((5, 5), np.float32) / 25

    blurred = cv2.cvtColor(cv2.filter2D(
        image, -1, gaussKernel), cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(blurred, lowRange, highRange)
    mask = cv2.bitwise_not(mask)
    mask = cv2.erode(mask, erodeKernel, iterations=30)
    mask = cv2.dilate(mask, erodeKernel, iterations=20)

    return mask


def getBeansByColor(mask):
    _, beansContours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    beansByColor = []

    for beanContour in beansContours:
        beanMask = np.zeros(mask.shape, np.uint8)
        cv2.fillPoly(beanMask, [beanContour], (255, 255, 255))
        # cv2.imshow("test", beanMask)
        # cv2.waitKey(0)
        mean = cv2.mean(image, beanMask)
        beansByColor.append([mean, beanContour])

    return beansByColor


def drawBean(beanContours, rectangle=True):
    if rectangle:
        # DRAW RECTANGLE
        enlarge = 30
        x, y, w, h = cv2.boundingRect(beanContours)

        rectLeft = x - enlarge
        rectRight = rectLeft + w + (enlarge * 2)
        rectTop = y - enlarge
        rectBottom = rectTop + h + (enlarge * 2)
        cv2.rectangle(image, (rectLeft, rectTop),
                      (rectRight, rectBottom), (0, 0, 255), 8)
        cv2.rectangle(image, (rectLeft, rectTop),
                      (rectRight, rectBottom), (0, 255, 0), 6)
        cv2.rectangle(image, (rectLeft, rectTop),
                      (rectRight, rectBottom), (255, 0, 0), 4)
    else:
        # DRAW CONTOUR
        cv2.drawContours(image, [beanContours], -1, (0, 0, 255), 10)
        cv2.drawContours(image, [beanContours], -1, (255, 0, 0), 6)
        cv2.drawContours(image, [beanContours], -1, (0, 255, 0), 3)


def isCloseColor(colorA, colorB, leeway):
    redSimilar = abs(colorA[0] - colorB[0]) < leeway
    greenSimilar = abs(colorA[1] - colorB[1]) < leeway
    blueSimilar = abs(colorA[2] - colorB[2]) < leeway
    return redSimilar and greenSimilar and blueSimilar


def drawBeans(beansByColor):
    groups = 4
    beanGroups = []
    beans = []

    for i in range(len(beansByColor)):
        beanWithColor = beansByColor[i]
        color = beanWithColor[0]
        beanContours = beanWithColor[1]
        r = color[0]
        g = color[1]
        b = color[2]

        if i == 0:
            beanGroups.append([beanWithColor])
        else:
            for group in beanGroups:
                if isCloseColor(group[0][0], color, 20):
                    group[0].append(beanWithColor)
                else:
                    beanGroups.append([beanWithColor])

        beans.append(beanWithColor)
        drawBean(beanContours)

    return beans[0]


imageLocation1 = 'bonen/Image__2019-04-29__03-03-16.bmp'
imageLocation2 = 'bonen/Image__2019-04-29__02-58-28.bmp'
imageLocation3 = 'bonen/Image__2019-04-29__02-56-26.bmp'
imageLocation4 = 'bonen/Image__2019-04-29__02-54-56.bmp'
image = cv2.cvtColor(cv2.imread(imageLocation1), cv2.COLOR_BGR2RGB)

mask = generateMask(image)
beansByColor = getBeansByColor(mask)
beans = drawBeans(beansByColor)

# Visualize
plt.figure(figsize=(15, 6), frameon=False)

plt.subplot(121)
plt.imshow(mask, cmap='gray')
plt.title('Bean mask')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(image, cmap='gray')
plt.title(str(len(beans)) + ' beans')
plt.xticks([])
plt.yticks([])

plt.show()
