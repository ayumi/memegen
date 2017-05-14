#!/usr/bin/env python

#import cv
import cv2
import numpy as np
import re
import os

debug = False

# def findImages(root):
#     result = []
#     all = os.listdir(root)
#     return all
#     for filename in all:
#         path = os.path.join(root, filename)
#         if (os.path.isfile(path) and
#             valid.match(filename)):
#             result.append(os.path.splitext(filename)[0])
#     return result

def bound_image(imagePath):
    image = cv2.imread(imagePath)
    channels = cv2.split(image)
    white = channels[2]
    cv2.bitwise_and(white, channels[1], white)
    cv2.bitwise_and(white, channels[0], white)
    _, white = cv2.threshold(white, 200, 255, cv2.THRESH_BINARY)
    # if debug:
    #     cv2.imwrite('out/%s-white.png' % fn, white)

        #Mat morphKernel = getStructuringElement(MORPH_ELLIPSE, Size(3, 3));
        #morphologyEx(small, grad, MORPH_GRADIENT, morphKernel);
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    grad = cv2.morphologyEx(white, cv2.MORPH_GRADIENT, kernel)
    # if debug:
    #     cv2.imwrite('out/%s-grad.png' % fn, grad)

    _, thres = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # if debug:
    #     cv2.imwrite('out/%s-thres.png' % fn, thres)

     #morphKernel = getStructuringElement(MORPH_RECT, Size(9, 1));
         #morphologyEx(bw, connected, MORPH_CLOSE, morphKernel);
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(25,1))
    conn = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
    # if debug:
    #     cv2.imwrite('out/%s-conn.png' % fn, conn)

    kernel = np.ones((9,9),np.uint8)
    conn = cv2.erode(conn, kernel, iterations=1)
    conn = cv2.dilate(conn, kernel, iterations=1)
#edged = auto_canny(gray)
    # if debug:
    #     cv2.imwrite('out/%s-erode.png' % fn, conn)


    im2, contours, hierarchy = cv2.findContours(conn.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cmask = conn.copy()
    cmask.fill(0)
    cv2.drawContours(cmask, contours, -1, (255,255,255), -1)
    if debug:
        cv2.imwrite('out/%s-cmask.png' % fn, mask)

    mask = conn.copy()
    mask.fill(0)

    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        rect = cmask.copy()[y:y+h,x:x+w]
        height, width = rect.shape[:2]
        #r = ouble)countNonZero(maskROI)/(rect.width*rect.height);
        #r = cv2.CountNonZero(rect)/(w*h)
        r = float(np.count_nonzero(rect))/(w*h)
        if w > 30 and h > 30:
            print height, width, r
            if r > 0.45:
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.rectangle(mask, (x,y), (x+w,y+h), (255,255,255), -1)
    # if debug:
    #     cv2.imwrite('out/%s-bound.png' % fn, image)

    cv2.bitwise_and(white, mask, white)
    white = cv2.bitwise_not(white)
    fileName = os.path.basename(imagePath)
    filePath = 'out/%s.png' % fileName
    cv2.imwrite(filePath, white)
    return filePath

# directory = "../src"
# imageList = findImages(directory)
# for fn in imageList:

    # imagePath = os.path.join(directory, fn)
    # print 'Processing ' + imagePath


    # bound_image(imagePath)
