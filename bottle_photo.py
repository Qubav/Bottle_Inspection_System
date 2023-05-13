import cv2 as cv
import numpy as np

class BottlePhoto:

    def __init__(self, path: str) -> None:

        self.img = cv.imread(path)
        self.bottle_brand: str = None
        self.liquid_in_bottle: bool = False
        self.shape: np.ndarray = None

        self.img_scaling()
    
    def img_scaling(self, scale: float = 0.25) -> None:
        
        # setting up new width and height values by multiplying img width and height by scale
        width = int(self.img.shape[1] * scale)
        height = int(self.img.shape[0] * scale)
        size = (width, height)
        # changing img size to new values
        self.img = cv.resize(self.img, size, interpolation=cv.INTER_AREA)