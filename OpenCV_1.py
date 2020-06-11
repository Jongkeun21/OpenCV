import numpy as np
import cv2
import os

image_dir = os.getcwd() + "/images/"

def mouse_callback(event, x, y, flags, param) :
    if event == cv2.EVENT_LBUTTONDOWN :
        print("LBUTTON CLICKED: ", x, ", ", y)

cv2.namedWindow('img_color')
cv2.setMouseCallback('img_color', mouse_callback)

while True :
    img_color = cv2.imread(image_dir+"dog.3.jpg")
    height, width = img_color.shape[:2]
    img_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_AREA)
    
    img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    
    cv2.imshow('img_color', img_color)
    
    if cv2.waitKey(1) & 0xFF == 27 :
        break

cv2.destroyAllWindows()