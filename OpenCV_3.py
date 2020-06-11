# -*- conding: utf-8 -*-

import numpy as np
import os
import cv2

img_dir = os.getcwd()+"/images/"
img_color = cv2.imread(img_dir+"dog.3.jpg")
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

ret, img_binary = cv2.threshold(img_gray, 127, 255, 0)

# For removing the noises
kernel = np.ones((10,10), np.uint8)
img_binary = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)
img_binary = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours :
    cv2.drawContours(img_color, [contour], 0, (255,0,0), 2)
    print(cv2.contourArea(contour))
    
    # x, y, w, h = cv2.boundingRect(contour)
    # cv2.rectangle(img_color, (x,y), (x+w, y+h), (0,255,0), 2)

    """
    Drawing the bounding box
    """
    # rect = cv2.minAreaRect(contour)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(img_color, [box], 0, (0,0,255), 2)

    """
    Getting the center of gravity
    """
    # M = cv2.moments(contour)
    # cx = int(M['m10']/M['m00'])
    # cy = int(M['m01']/M['m00'])
    # cv2.circle(img_color, (cx,cy), 5, (0,0,255), -1)

    """
    Approximating as threshold(curve to straight)
    """
    # threshold = 0.01
    # ep = threshold*cv2.arcLength(contour, True)
    # approx = cv2.approxPolyDP(contour, ep, True)
    # cv2.drawContours(img_color, [approx], 0, (0,0,255), 2)

    # for p in contour :
    #     cv2.circle(img_color, (p[0][0], p[0][1]), 1, (255,0,0), -1)

    """
    Drawing a convex hull and finding the concave points
    """
    # hull = cv2.convexHull(contour)
    # cv2.drawContours(img_color, [hull], 0, (255,0,255), 2)

    # hull = cv2.convexHull(contour, returnPoints=False)
    # defects = cv2.convexityDefects(contour, hull)

    # for i in range(defects.shape[0]) :
    #     s,e,f,d = defects[i, 0]
    #     start = tuple(contour[s][0])
    #     end = tuple(contour[e][0])
    #     far = tuple(contour[f][0])

    #     print(f"d: {d}")

    #     if d > 500 :
    #         cv2.line(img_color, start, end, [0,255,0], 2)
    #         cv2.circle(img_color, far, 3, [0,0,255], -1)

"""
Drawing all of contours
"""
# cv2.drawContours(img_color, contours, -1, (0, 255, 0), 2)

cv2.imshow('result', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()