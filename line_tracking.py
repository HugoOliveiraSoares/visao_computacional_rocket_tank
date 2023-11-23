import cv2
import time
import numpy as np
import matplotlib.pyplot as plt


class LineTracking():
    def __init__(self,img_file):
        self.img = img_file
        self.img_inter = self.img
        self.img_final = self.img
        self.cendroids = []
        self.mean_centroids = [0,0]

    def processing(self):
        print(self.img.shape)
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) 
        blur = cv2.GaussianBlur(gray,(5,5),0) 
        ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

        self.img_inter=thresh
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) #on créé l'élement structurant de l'ouverture
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)) #on créé l'élement structurant de la fermeture

        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open) #on fait une ouverture suivant un motif
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close) #on fait une fermeturesuivant un motif

        connectivity = 8

        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S) #permet de délimiter une forme
        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        self.centroids = output[3] #donne les centres de la ou des formes de l'image

        for c in self.centroids :
            self.mean_centroids[0] += c[0]/len(self.centroids)
            self.mean_centroids[1] += c[1]/len(self.centroids)

        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        for c in self.centroids :
            self.img_final[int(c[1])-5 : int(c[1])+10, int(c[0])-5 : int(c[0])+10] = [0,255,0]
