import cv2
import numpy as np
import sys
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
    mask = cv2.erode(mask, erodeKernel, iterations=15)
    mask = cv2.dilate(mask, erodeKernel, iterations=5)

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


def isCloseColor(colorA, colorB, leeway):
    redSimilar = abs(colorA[0] - colorB[0]) < leeway
    greenSimilar = abs(colorA[1] - colorB[1]) < leeway
    blueSimilar = abs(colorA[2] - colorB[2]) < leeway
    return redSimilar and greenSimilar and blueSimilar


def isCloseSize(contourA, contourB, leeway):
    aX, aY, aW, aH = cv2.boundingRect(contourA)
    bX, bY, bW, bH = cv2.boundingRect(contourB)
    sameSize = abs((bW * bH) - (aH * aW)) < leeway
    return sameSize


def filterCoffeeBeans(beansByColor):
    groups = 4
    coffeeBeanGroup = 1
    beanGroups = []
    beans = []

    # minRed = min(beansByColor, key=lambda x: x[0][0])[0][0]
    # minGreen = min(beansByColor, key=lambda x: x[0][1])[0][1]
    # minBlue = min(beansByColor, key=lambda x: x[0][2])[0][2]
    # maxRed = min(beansByColor, key=lambda x: x[0][0])[0][0]
    # maxGreen = min(beansByColor, key=lambda x: x[0][1])[0][1]
    # maxBlue = min(beansByColor, key=lambda x: x[0][2])[0][2]

    # maxDiff = max(maxRed, maxGreen, maxBlue)
    # minDiff = min(minRed, minGreen, minBlue)
    # diff = maxDiff - minDiff
    # print(diff)

    for i in range(len(beansByColor)):
        beanWithColor = beansByColor[i]
        color = beanWithColor[0]
        beanContours = beanWithColor[1]

        if i == 0:
            beanGroups.append([beanWithColor])
        else:
            assigned = False
            for group in beanGroups:
                if isCloseColor(group[0][0], color, 18):
                    group.append(beanWithColor)
                    assigned = True
                    break
            if assigned == False:
                beanGroups.append([beanWithColor])

    beanGroups = sorted(beanGroups, key=lambda x: x[0][0])

    return beanGroups[coffeeBeanGroup]


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


def drawBeans(beans):
    for bean in beans:
        drawBean(bean[1])


if len(sys.argv) < 2:
    print("No image location supplied")
    exit()

imageLocation = sys.argv[1]

image = cv2.cvtColor(cv2.imread(imageLocation), cv2.COLOR_BGR2RGB)

mask = generateMask(image)
beansByColor = getBeansByColor(mask)
beans = filterCoffeeBeans(beansByColor)
drawBeans(beans)

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
