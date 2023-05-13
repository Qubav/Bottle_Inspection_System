from bottle_photo import BottlePhoto
from shape_matching import ShapeMatching
import cv2 as cv
import numpy as np


def lat_hist(img, type):  
        x = img.shape[type]
        lh = np.zeros(x, dtype = int)
        for i in range(0, x, 1):
            if type == 1:
                lh[i] = sum(img[::1, i])
            elif type == 0:
                lh[i] = sum(img[i,::1])
        
        return lh







if __name__ == "__main__":

    path = "Zdjecia/IMG_7551.jpg"
    bottle1 = BottlePhoto(path=path)
    shape_matching = ShapeMatching(bottle1)
    cv.imshow("bottle", bottle1.img)
    cv.imshow("shape", shape_matching.shape)
    cv.waitKey(0)

    
