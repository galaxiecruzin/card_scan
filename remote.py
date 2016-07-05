import os
import sys
from PySide import QtCore, QtGui
from mainwindow import Ui_MainWindow
from decimal import *
import numpy as np
import cv
import cv2
import imghdr
from detect_card import detect_card, longest_lines
from scan_card import get_card
# Get entrypoint through which we control underlying Qt framework
TEMPFILE = '/tmp/mytempfile.jpg'
WINDOW = 'The Card'
# CARD_IMAGES = '/Users/abarger/Cockatrice/pics/downloadedPics'
# CARD_IMAGES = '/Users/abarger/card_scan/phototest/'
CARD_IMAGES = '/Users/abarger/Downloads/card-scans'
BACKGROUND = '/Users/abarger/card_scan/phototest/greenscreen.jpg'


class App():

    def __init__(self):
        self.qapp = QtGui.QApplication(sys.argv)
        self.main = MainWindow()

    def show(self):
        self.main.show()

    def shutdown(self):
        sys.exit(self.qapp.exec_())


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set Image
        myPixmap = QtGui.QPixmap('./phototest/ancient-stirrings.jpg')
        myScaledPixmap = myPixmap.scaled(self.ui.preview.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.preview.setPixmap(myScaledPixmap)

        # Set Status
        self.ui.status.setText("Identified")

        # Set Card Name
        self.ui.card_name.setText("Ancient Stirrings")

        # Load combo options for expansion
        # self.ui.expansion

        # Load combo options for conditions
        # self.ui.condition


class CvImage:
    size = None
    original = None
    current = None
    greyscale = None
    img_ndarray = None
    img2 = None

    def __init__(self):
        self.size = (0, 0)

    def __str__(self):
        return "Image (%s, %s)" % (self.get_height(), self.get_width())

    def load_image(self, path):
        print ("Image type:%s" % imghdr.what(path))
        if imghdr.what(path) == 'jpeg':
            print ("Loading image: %s" % path)
            self.original = cv.LoadImage(path) # returns -> iplimage
            self.img_ndarray = cv2.imread(path) # returns -> numpy.ndarray
            self.img2 = cv2.imread(path, 0) # returns -> numpy.ndarray
            self.size = cv.GetSize(self.original)
            self.current = cv.CloneImage(self.original)
            self.save_temp_file()
        # cv.CvtColor(self.current, self.greyscale, cv.CV_RGB2GRAY)

    def flip_horizontal(self):
        new = cv.CloneImage(self.current)
        cv.Flip(self.current, new, flipMode=0)
        new2 = cv.CloneImage(self.current)
        cv.Flip(new, new2, flipMode=1)
        self.current = cv.CloneImage(new2)
        self.save_temp_file()

    def save_temp_file(self):
        cv.SaveImage(TEMPFILE, self.current)

    def get_height(self):
        return self.size[1]

    def get_width(self):
        return self.size[0]

    def get_area(self):
        return Decimal(self.get_height()) * Decimal(self.get_width())

    def get_original(self):
        return self.original

    def get_current(self):
        return self.current

    def get_greyscale(self):
        self.greyscale = cv.CreateImage(cv.GetSize(self.current), 8, 1)
        cv.CvtColor(self.current, self.greyscale, cv.CV_RGB2GRAY)
        return self.greyscale

    def is_rightside_up(self):
        try:
            img_gray = cv2.cvtColor(self.img_ndarray, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            # print ('Error converting image to grayscale with cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)')
            return True
        ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        features = {'top': 0, 'bottom': 0}
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if approx.size == 8:
                # Ignore micro boxes
                cnt_area = box_area(approx)
                area_diff = cnt_area / self.get_area()
                if Decimal(0.34) > area_diff > Decimal(0.05):
                    # Determine if contour is in the top half or bottom half
                    cnt_y = box_y(cnt)
                    if cnt_y < (self.get_height()/2):
                        features['top'] += 1
                    else:
                        features['bottom'] += 1
                    cv2.drawContours(self.img_ndarray, [cnt], 0, (0, 255, 0), 5)
        show_image(self.img_ndarray)
        print ("features top: %s \ bottom %s" % (features['top'], features['bottom']))
        if features['top'] > features['bottom']:
            return False
        return True


def box_area(contour):
    x,y,w,h = cv2.boundingRect(contour)
    return Decimal(w) * Decimal(h)


def box_y(contour):
    x,y,w,h = cv2.boundingRect(contour)
    return y


def template_match(cv_image):
    template = cv2.imread('./phototest/expansion.jpg', 0)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
               'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    for meth in methods:
        img = cv_image.img2.copy()
        method = eval(meth)

        # Apply template Matching
        match = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        demo = cv.CloneImage(cv_image.original)
        cv.Rectangle(demo, top_left, bottom_right, (0, 255, 0), 10)
        print ("Show template match. method = %s, TL=%s BR=%s" % (meth, top_left, bottom_right))
        show_image(demo)

# class MyDialog(QDialog):
#     def __init__(self, parent=None):
#         super(MyDialog, self).__init__(parent)


def init():
    APP = QtGui.QApplication(sys.argv)
    main = MainWindow()
    return main
    # cv.NamedWindow(WINDOW, flags=cv.CV_WINDOW_NORMAL)
    # cv.MoveWindow(WINDOW, 0, 0)
    # cv.ResizeWindow(WINDOW, 350, 500)


def list_images():
    local_files = []
    for path, subdirs, files in os.walk(CARD_IMAGES):
        for name in files:
            local_files.append(os.path.join(path, name))
    return local_files


def show_image(img):
    if isinstance(img, np.ndarray):
        cv2.imshow(WINDOW, img)
    elif isinstance(img, cv2.cv.iplimage):
        cv.ShowImage(WINDOW, img)

    key = cv.WaitKey(1000)
    if key == 27:
        shutdown()


def shutdown():
    print ("Exiting...")
    cv.DestroyAllWindows()


def card_from_image(img):
    greyscale = img.get_greyscale()
    current = img.get_current()
    background = cv.LoadImage(BACKGROUND, iscolor=False)
    if greyscale.height == background.height and greyscale.width == background.width:
        corners = detect_card(greyscale, background)
        if corners is not None:
            card = get_card(current, corners)
            show_image(card)
            return card
    return False


if __name__ == "__main__":
    # initialize windows
    app = App()
    app.show()

    # samples = ['./phototest/ancient-stirrings.jpg', './phototest/ancient-stirrings-copy.jpg']
    # samples = list_images()
    #
    # for sample in samples:
    #     img = CvImage()
    #     img.load_image(sample)
    #     if img.current is not None:
    #         show_image(img.current)
    #         if not img.is_rightside_up():
    #             print ("flipping %s" % sample)
    #             img.flip_horizontal()
    #             show_image(img.current)
    #         greyscale_card = card_from_image(img)
    #         show_image(greyscale_card)
            # template_match(img)
    '''
    # prompt for next card or quit
    answer = ''
    while answer != 'q':
        print "Enter 'n' for next image or 'q' to quit:"
        answer = raw_input()
        if answer == 'n':
            # load an image
            # get('http://192.168.0.111/current.jpg')
            pass
    '''
    app.shutdown()

'''
flipping /Users/abarger/Cockatrice/pics/downloadedPics/ARC/A Display of My Dark Power.jpg
flipping /Users/abarger/Cockatrice/pics/downloadedPics/ARC/The Iron Guardian Stirs.jpg
flipping /Users/abarger/Cockatrice/pics/downloadedPics/ME4/Acid Rain.jpg
flipping /Users/abarger/Cockatrice/pics/downloadedPics/NPH/Chancellor of the Tangle.jpg
flipping /Users/abarger/Cockatrice/pics/downloadedPics/SOK/Adamaro, First to Desire.jpg
'''
