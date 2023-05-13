from bottle_photo import BottlePhoto
import cv2 as cv
import numpy as np

class ShapeMatching():

    def __init__(self, bottle: BottlePhoto) -> None:

        self.bottle = bottle
        self.problem_occurred = False

        self.get_bottle_shape()

    
    def get_bottle_shape(self) -> None:
        
        # creating array with image in grayscale
        img_gray: np.ndarray = cv.cvtColor(self.bottle.img, cv.COLOR_BGR2GRAY)
        # adding blur to img_gray 
        img_gray = cv.GaussianBlur(img_gray, (13, 13), cv.BORDER_DEFAULT)
        # thresholding img with experimentally determined threshold value
        _, thresh = cv.threshold(img_gray, 35, 255, cv.THRESH_BINARY)
        # finding contours on thresholded image
        cnt, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        # creating blank matrix that will be used to draw bottle shape - filled contour
        blank = np.zeros((img_gray.shape), dtype=np.uint8)
        # determining which one of found contours should be filled - last one is whole photo contour, second from the end is bottle contour
        x = len(cnt) - 1

        if (x < 0):
            # if this condition is met it means photo doesn't met requirements
            self.problem_occurred = True
        else:
            # filling contour
            shape = cv.fillPoly(blank, [cnt[x]], (255, 255, 255))
            kernel = np.ones((7, 7), np.uint8)
            # adding morphological transformation - closing
            shape = cv.morphologyEx(shape, cv.MORPH_CLOSE, kernel)
            # attributes assignment
            self.shape = shape
            self.bottle.shape = self.shape

    def prep_to_matching(self) -> None:
        x = 0