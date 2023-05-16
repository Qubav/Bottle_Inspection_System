from bottle_photo import BottlePhoto
import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt


THRESHOLD_VALUE = 35
GAUS_BLUR_KERNEL = (13, 13)
MORPH_CLOSING_KERNEL = np.ones((7, 7), np.uint8)
PERCENT_LEFT_CROP = 3
BOTTLE_WIDTH_VAL = 160

class ShapeMatching():

    def __init__(self, bottle: BottlePhoto) -> None:

        self.bottle = bottle
        self.problem_occurred = False
        self.raw_shape: np.ndarray = None
        self.shape: np.ndarray = None
        self.cropped_img: np.ndarray = None
        self.cropped_adjusted: np.ndarray = None
        self.starting_bottle_width: int = None

        self.get_bottle_shape()
        self.crop_shape()
        self.adjust_bottle_width()

    
    def get_bottle_shape(self) -> None:
        
        # creating array with image in grayscale
        img_gray: np.ndarray = cv.cvtColor(self.bottle.img, cv.COLOR_BGR2GRAY)
        # adding blur to img_gray 
        img_gray = cv.GaussianBlur(img_gray, GAUS_BLUR_KERNEL, cv.BORDER_DEFAULT)
        # thresholding img with experimentally determined threshold value
        _, thresh = cv.threshold(img_gray, THRESHOLD_VALUE, 255, cv.THRESH_BINARY)
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
            # adding morphological transformation - closing
            shape = cv.morphologyEx(shape, cv.MORPH_CLOSE, MORPH_CLOSING_KERNEL)
            # attributes assignment
            self.raw_shape = shape

    def crop_shape(self) -> None:
        lat_hist_x = np.sum(self.raw_shape, 0)
        lat_hist_y = np.sum(self.raw_shape, 1)

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(lat_hist_x)
        plt.title("x")
        plt.subplot(2, 1, 2)
        plt.plot(lat_hist_y)
        plt.title("y")
        plt.show()

        first_occ_x = np.argmax(lat_hist_x >= 2550)
        last_occ_x = len(lat_hist_x) - np.argmax(lat_hist_x[::-1] >= 2550) - 1
        first_occ_y = np.argmax(lat_hist_y >= 2550)
        last_occ_y = len(lat_hist_y) - np.argmax(lat_hist_y[::-1] >= 2550) - 1

        bottle_width = last_occ_x - first_occ_x
        bottle_height = last_occ_y - first_occ_y

        if bottle_height > bottle_width:
            additional_val = int(bottle_height * PERCENT_LEFT_CROP / 100)
        else:
            additional_val = int(bottle_width * PERCENT_LEFT_CROP / 100)
        
        x_r = last_occ_x + additional_val
        x_l = first_occ_x - additional_val
        y_b = last_occ_y + additional_val
        y_t = first_occ_y - additional_val

        # protection in case this values would be negative or higher than shape value
        if y_b > self.raw_shape.shape[0]:
            y_b =  self.raw_shape.shape[0]
        if y_t < 0:
            y_t = 0
        if x_r > self.raw_shape.shape[1]:
            x_r = self.raw_shape.shape[1]
        if x_l < 0:
            x_l = 0

        self.cropped_img = self.raw_shape[y_t:y_b,x_l:x_r]
        self.starting_bottle_width = bottle_width

    def adjust_bottle_width(self):

        scale = BOTTLE_WIDTH_VAL / self.starting_bottle_width
        new_width = int(self.cropped_img.shape[1] * scale)
        new_height = int(self.cropped_img.shape[0] * scale)
        new_size = (new_width, new_height)
        new_img = cv.resize(self.cropped_img, new_size, interpolation = cv.INTER_AREA)
        self.cropped_adjusted = cv.morphologyEx(new_img, cv.MORPH_CLOSE, MORPH_CLOSING_KERNEL)      

    def prep_to_matching(self) -> None:
        x = 0