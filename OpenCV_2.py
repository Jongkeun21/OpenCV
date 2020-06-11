import numpy as np
import cv2

hsv = 0

lower_blue1 = 0
lower_blue2 = 0
lower_blue3 = 0

upper_blue1 = 0
upper_blue2 = 0
upper_blue3 = 0

threshold = 0

def mouse_callback(event, x, y, flags, param) :
    global hsv, lower_blue1, lower_blue2, lower_blue3, upper_blue1, upper_blue2, upper_blue3, threshold
    
    if event == cv2.EVENT_LBUTTONDOWN :
        print(img_color[y,x])
        color = img_color[y,x]
        
        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]
        
        threshold = cv2.getTrackbarPos('threshold', 'img_result')
        
        if hsv[0] < 10 :
            print("case 1")
            
            lower_blue1 = np.array([hsv[0]-10+180, threshold, threshold])
            lower_blue2 = np.array([0, threshold, threshold])
            lower_blue3 = np.array([hsv[0], threshold, threshold])
            
            upper_blue1 = np.array([180, 255, 255])
            upper_blue2 = np.array([hsv[0], 255, 255])
            upper_blue3 = np.array([hsv[0]+10, 255, 255])
            
        elif hsv[0] > 170 :
            print("case 2")
            
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            lower_blue2 = np.array([0, threshold, threshold])
            lower_blue3 = np.array([hsv[0]-10, threshold, threshold])
            
            upper_blue1 = np.array([hsv[0]+10-180, 255, 255])
            upper_blue2 = np.array([hsv[0]-10, 255, 255])
            upper_blue3 = np.array([hsv[0]+10, 255, 255])
            
        else :
            print("case 3")
            
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            lower_blue2 = np.array([hsv[0]-10, threshold, threshold])
            lower_blue3 = np.array([hsv[0]-10, threshold, threshold])
            
            upper_blue1 = np.array([hsv[0]+10, 255, 255])
            upper_blue2 = np.array([hsv[0], 255, 255])
            upper_blue3 = np.array([hsv[0], 255, 255])
            
        print("hsv: ", hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)

def trackbarCallback(_) :
    pass

cv2.namedWindow('img_color')
cv2.setMouseCallback('img_color', mouse_callback)

cv2.namedWindow('img_result')
cv2.createTrackbar('threshold', 'img_result', 0, 255, trackbarCallback)
cv2.setTrackbarPos('threshold', 'img_result', 30)

cap = cv2.VideoCapture(0)

while True :
    ret, img_color = cap.read()
    height, width = img_color.shape[:2]
    img_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_AREA)
    
    img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    
    img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)
    img_mask = img_mask1 | img_mask2 | img_mask3
    
    kernel = np.ones((3,3), np.uint8)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)
    
    img_result = cv2.bitwise_and(img_color, img_color, mask=img_mask)
    
    numOfLabels, img_label, stats, centroids = cv2.connectedComponentsWithStats(img_mask)
    
    for idx, centroid in enumerate(centroids) :
        if stats[idx][0] == 0 and stats[idx][1] == 0 :
            continue
            
        if np.any(np.isnan(centroid)) :
            continue
            
        x, y, width, height, area = stats[idx]
        centerX, centerY = int(centroid[0]), int(centroid[1])
        
        if area > 75 :
            cv2.circle(img_color, (centerX,centerY), 10, (0,0,255), 10)
            cv2.rectangle(img_color, (x,y), (x+width,y+height), (0,0,255))
    
    cv2.imshow('img_color', img_color)
    cv2.imshow('img_mask', img_mask)
    cv2.imshow('img_result', img_result)
    
    if cv2.waitKey(1) & 0xFF == 27 :
        break
        
cv2.destroyAllWindows()