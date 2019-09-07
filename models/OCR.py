from imutils import contours
import cv2
import numpy as np
from models.Card import Card
import inspect


class OCR:
    image = None
    reference = None
    ocrRef = {}

    def __init__(self, image, reference):
        self.image = image
        self.reference = reference
        self.setOCRReference()

    def selectMyHand(self):
        # Return an image of your cards based on capture 1920x1080
        return self.image[700:740, 893:1000]

    def selectRegion(self):
        # Allow you to select a region on a picture and print the coordinate
        r = cv2.selectROI(self.image)
        print r
        # Crop image
        # [y:y+h, x:x+w]
        imCrop = self.image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    def setOCRReference(self):
        gray = cv2.cvtColor(self.reference, cv2.COLOR_BGR2GRAY)
        refThresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
        im2, refCnts, hierarchy = cv2.findContours(refThresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
        for (i, c) in enumerate(refCnts):
            (x, y, w, h) = cv2.boundingRect(c)
            if 60 < h < 110:
                roi = refThresh[y:y + h, x:x + w]
                roi = cv2.resize(roi, (57, 88))
                cv2.rectangle(refThresh, (x, y), (x + w, y + h), (0, 0, 0), 1);
                self.ocrRef[i] = roi

    def getMyHand(self):
        img = self.selectMyHand()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
        im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = contours.sort_contours(cnts, method="left-to-right")[0]
        locs = []

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            if 20 <= h < 40:
                rect = (x, y, w, h)
                locs.append(rect)
                cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 255, 0), 1);

        cv2.imshow("thresh", thresh)
        output = []

        for (i, (x, y, w, h)) in enumerate(locs):
            roi = thresh[y:y + h, x:x + w]
            roi = cv2.resize(roi, (57, 88))

            scores = []

            for (digit, digitROI) in self.ocrRef.items():
                result = cv2.matchTemplate(roi, digitROI,
                                           cv2.TM_CCOEFF)
                (_, score, _, _) = cv2.minMaxLoc(result)
                scores.append(score)
            output.append(Card(int(np.argmax(scores)), 0))
        return output
