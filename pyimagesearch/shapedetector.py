# import the necessary packages
import cv2


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        print len(approx)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 4:
            shape = "Carreau"
        elif len(approx) == 5:
            shape = "Coeur"
        elif len(approx) == 7:
            shape = "Trefle"

        elif len(approx) == 8:
            shape = "Pique"
        # otherwise, we assume the shape is a circle
        else:
            shape = "undefined"

        # return the name of the shape
        return shape
