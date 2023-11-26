import cv2
import time
import numpy as np
import matplotlib.pyplot as plt


class LineTracking():
    def __init__(self,img_file):
        self.img = img_file

    def processing(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,th = cv2.threshold(blur, 60,255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(self.img, contours, -1, (0,255,0), 3)
        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            return self.img, M 

        return self.img, 0
