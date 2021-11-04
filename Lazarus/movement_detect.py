from grab_screen import grab_screen
import cv2
import numpy as np


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def apply_roi(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    vertices = np.array([[0, 520], [0, 168], [1280, 168], [1280, 520]], np.int32)
    return roi(gray, [vertices])


prev = grab_screen(region=(0, 40, 1280, 1024))
prev = apply_roi(prev)

current = None

while True:
    screen = grab_screen(region=(0, 40, 1280, 1024))
    region = apply_roi(screen)

    delta_frame = cv2.absdiff(prev, region)   #Find the difference in two frames
    threshold = cv2.threshold(delta_frame, 120, 255, cv2.THRESH_BINARY)[1]   #Minimum threshold to determine movement, make things white
    contour, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #Find target and create contour lines

    for i in contour:
        if cv2.contourArea(i) < 50:
            continue
        else:
            x, y, w, h = cv2.boundingRect(i)
            cv2.rectangle(screen, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow('window', screen)

    prev = region

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break