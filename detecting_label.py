from bottle_photo import BottlePhoto
import cv2 as cv
import numpy as np

WIT_LABEL_TEMPLATES = ["Label_Templates/wit1.png", "Label_Templates/wit2.png", "Label_Templates/wit3.png", "Label_Templates/wit4.png", "Label_Templates/wit5.png", "Label_Templates/wit6.png", "Label_Templates/wit7.png", "Label_Templates/wit8.png", "Label_Templates/wit9.png"]
WIT_CAP_TEMPLATE = ["Label_Templates/wit_cap.png"]
RIVIVA_LABEL_TEMPLATE = ["Label_Templates/riviva_labe.png"]
RIVIVA_CAP_TEMPLATE = ["Label_Templates/riviva_cap.png"]
SOMERSBY_LABEL_TEMPLATES = ["Label_Templates/somer1.png", "Label_Templates/somer2.png", "Label_Templates/somer3.png"]
RIVIVA_CAP_TEMPLATE = ["Label_Templates/riviva_cap.png"]

GOOD_MATCHES_MIN_NUMBER = 12

class LabelDetection:

    def __init__(self, bottle: BottlePhoto) -> None:
        
        self.bottle = bottle
        self.label_img: np.ndarray = None
        self.no_label_fits: bool = None

        self.detect_label()

    def label_comparison(self, template: np.ndarray) -> int:

        orb = cv.ORB_create()
        kp_img, des_img = orb.detectAndCompute(self.bottle.img, None)
        kp_label, des_label = orb.detectAndCompute(template, None)
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des_img, des_label, k = 2)

        good_matches_count = 0
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches_count += 1
        
        return good_matches_count


    def detect_label(self):

        if self.bottle.bottle_brand == "DrWit":

            best_match_val = 0
            templates: list [np.ndarray] = []

            for single_template in WIT_LABEL_TEMPLATES:
                new_img = cv.imread(single_template)
                new_img = cv.resize(new_img, (int(0.25 * new_img.shape[1]), int(0.25 * new_img.shape[0])))
                templates.append(new_img)
            
            # for template in templates:
            #     good_matches_count = self.label_comparison(template = template)
            #     if good_matches_count > best_match_val:
            #         best_match_val = good_matches_count
            
            for index, template in enumerate(templates):
                good_matches_count = self.label_comparison(template = template)
                if good_matches_count > best_match_val:
                    best_match_val = good_matches_count
                    best_match_index = index

            if best_match_val > GOOD_MATCHES_MIN_NUMBER:
                self.label_img = templates[best_match_index]
                self.no_label_fits = False
            
            else:
                self.no_label_fits = True
