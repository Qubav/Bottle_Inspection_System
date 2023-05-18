import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui_main_window import Ui_MainWindow
from bottle_inspection_system import bottle_inspection_system
import cv2 as cv

class Main_Window(QtWidgets.QMainWindow, QtWidgets.QFileDialog):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.f_name = "Photos/w_z_e_11.jpg"
        self.is_browse_clicked()
        self.is_start_clicked()
    
    def is_start_clicked(self):
        self.ui.start_button.clicked.connect(self.start_inspection)
        
    def start_inspection(self):
        self.ui.log_box.clear()
        file_name = self.f_name
        try:
            input_img, processed_img = bottle_inspection_system(file_name, self.add_log)
            inp_img = self.convert_cv_qt(input_img)
            proc_img = self.convert_cv_qt(processed_img)
            self.ui.inp_img.setPixmap(inp_img)
            self.ui.proc_img.setPixmap(proc_img)
        except:
            self.add_log("A problem occurred.\nPlease pick other image!")
    
    def is_browse_clicked(self):
        self.ui.browse.clicked.connect(self.browse_files)
    
    def browse_files(self):
        f_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "Photos")
        self.ui.file_name.setText(str(f_name[0]))
        self.f_name = str(f_name[0])
        
    def add_log(self, log: str):
        self.ui.log_box.append(log)
    
    def convert_cv_qt(self, cv_img):
        rgb_img = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytse_per_line = ch * w
        p = QtGui.QImage(rgb_img.data, w, h, bytse_per_line, QtGui.QImage.Format_RGB888)

        return QtGui.QPixmap.fromImage(p)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Main_Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()




















# from bottle_photo import BottlePhoto
# from shape_matching import ShapeMatching
# from detecting_label import LabelDetection
# from liquid_level_detection import LiquidLevelDetection
# from matplotlib import pyplot as plt
# import cv2 as cv
# import numpy as np





# if __name__ == "__main__":

#     path = "Photos/r_e_4.jpg"
#     # path = "Photos/IMG_7550.jpg"
#     # path = "Photos/IMG_7551.jpg"


#     bottle1 = BottlePhoto(path=path)
#     shape_matching = ShapeMatching(bottle1)
#     label_detection = LabelDetection(bottle1)
#     liquid_level_detection = LiquidLevelDetection(bottle1)

#     # old_hist = lat_hist(bottle1.shape, 1)
#     cv.imshow("bottle", bottle1.img)
#     cv.imshow("shape", shape_matching.raw_shape)
#     cv.imshow("cropped img", shape_matching.cropped_img)
#     cv.imshow("to match", shape_matching.cropped_adjusted)
#     print(bottle1.bottle_brand)
#     cv.imshow("cap bb", label_detection.img_w_bounding_boxes)
#     cv.imshow("hsv masked", liquid_level_detection.img_hsv_masked)
#     cv.imshow("rectangle", liquid_level_detection.img_hsv_rectangle)
#     cv.imshow("whole", bottle1.img_with_bb_and_liquid_lvl)
#     print(label_detection.no_label_fits)
#     if liquid_level_detection.liquid_presence is True:
#         print(liquid_level_detection.liquid_color)
#     print(liquid_level_detection.liquid_presence)
#     if label_detection.no_label_fits is False:
#         cv.imshow("label", label_detection.label_img)
#     cv.waitKey(0)



