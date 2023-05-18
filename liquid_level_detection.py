from bottle_photo import BottlePhoto
import cv2 as cv
import numpy as np

YELLOW_UPPER_HSV_VALUES = np.array([36, 255, 255])
YELLOW_LOWER_HSV_VALUES = np.array([18, 160, 85])
GREEN_UPPER_HSV_VALUES = np.array([70, 255, 255])
GREEN_LOWER_HSV_VALUES = np.array([35, 50, 50])

RECTANGLE_WIDTH_PERCENTAGE = 15

class LiquidLevelDetection:

    def __init__(self, bottle: BottlePhoto) -> None:
        
        self.bottle = bottle
        self.liquid_presence: bool = None
        self.img_hsv_masked: np.ndarray = None
        self.liquid_color: str = None
        self.img_hsv_rectangle: np.ndarray = None

        self.get_hsv_masked_img()
        self.get_liquid_color()
        self.get_hsv_rectangle_masked_img()

    def get_hsv_masked_img(self):
        """Method creates hsv image of bottle photo and adds mask to it, then assigns it as attribute."""

        img_hsv = cv.cvtColor(self.bottle.img , cv.COLOR_BGR2HSV)
        self.img_hsv_masked = cv.bitwise_and(img_hsv, img_hsv, mask = self.bottle.shape_img)
    
    def get_hsv_rectangle_masked_img(self):

        blank = np.zeros((self.bottle.shape_img.shape), dtype=np.uint8)

        # getting lateral histogram to determine the object's location
        lat_hist_x = np.sum(self.bottle.shape_img, 0)
        lat_hist_y = np.sum(self.bottle.shape_img, 1)

        # getting object's coordinates from lateral histogram
        left = np.argmax(lat_hist_x >= 2550)
        right = len(lat_hist_x) - np.argmax(lat_hist_x[::-1] >= 2550) - 1
        top = np.argmax(lat_hist_y >= 2550)
        bottom = len(lat_hist_y) - np.argmax(lat_hist_y[::-1] >= 2550) - 1

        bottle_width = right - left
        rectangle_width = int(bottle_width * RECTANGLE_WIDTH_PERCENTAGE /100)

        new_left = left + bottle_width // 2 - rectangle_width // 2
        new_right = right - bottle_width // 2 + rectangle_width // 2

        mask = cv.rectangle(blank, [new_left, top], [new_right, bottom], (255, 255, 255), -1)

        self.img_hsv_rectangle = cv.bitwise_and(self.img_hsv_masked, self.img_hsv_masked, mask = mask,)


    def get_liquid_color(self):
        
        yellow_color_pixels_img = cv.inRange(self.img_hsv_masked, YELLOW_LOWER_HSV_VALUES, YELLOW_UPPER_HSV_VALUES)
        green_color_pixels_img = cv.inRange(self.img_hsv_masked, GREEN_LOWER_HSV_VALUES, GREEN_UPPER_HSV_VALUES)

        shape_pixels_count = cv.countNonZero(self.bottle.shape_img)
        yellow_pixels_count = cv.countNonZero(yellow_color_pixels_img)
        green_pixels_count = cv.countNonZero(green_color_pixels_img)

        # based on bottle brand and number of pixels representing possible colors and pixels representing bottle shape determining liquid presence and its color
        if self.bottle.bottle_brand == "DrWit":
            if green_pixels_count < 0.02 * shape_pixels_count and yellow_pixels_count < 0.02 * shape_pixels_count:
                self.liquid_presence = False
            elif green_pixels_count > yellow_pixels_count:
                self.liquid_color = "green"
                self.liquid_presence = True
            else:
                self.liquid_color = "yellow"
                self.liquid_presence = True

        elif self.bottle.bottle_brand == "Riviva":
            if yellow_pixels_count < 0.02 * shape_pixels_count:
                self.liquid_presence = False
            else:
                self.liquid_color = "yellow"
                self.liquid_presence = True

        else:
            if green_pixels_count < 0.02 * shape_pixels_count:
                self.liquid_presence = False
            else:
                self.liquid_color = "green"
                self.liquid_presence = True
            
    def get_liquid_level(self):

        x = 2

