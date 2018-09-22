# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from imutils import contours
from pyimagesearch.colorlabeler import ColorLabeler
import argparse
import imutils
import cv2
import numpy as np

cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def selectMyHand(image):
    return image[700:740, 893:1000]


def selectRegion(image):
    # Select ROI
    r = cv2.selectROI(image)
    print r
    # Crop image
    # [y:y+h, x:x+w]
    imCrop = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    # Display cropped image
    cv2.imshow("Cropped", imCrop)
    cv2.waitKey(0)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-r", "--reference", required=True,
                help="path to reference OCR-A image")
args = vars(ap.parse_args())

# load the reference OCR-A image from disk, convert it to grayscale,
# and threshold it, such that the digits appear as *white* on a
# *black* background
# and invert it, such that the digits appear as *white* on a *black*
ref = cv2.imread(args["reference"])
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
refThresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image, then initialize the
# list of digit locations
im2, refCnts, hierarchy = cv2.findContours(refThresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}

# loop over the OCR-A reference contours
for (i, c) in enumerate(refCnts):
    # compute the bounding box for the digit, extract it, and resize
    # it to a fixed size
    (x, y, w, h) = cv2.boundingRect(c)
    if 60 < h < 110:
        roi = refThresh[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))
        cv2.rectangle(refThresh, (x, y), (x + w, y + h), (0, 0, 0), 1);
        # cv2.imshow("ref" + str(i), refThresh)
        # update the digits dictionary, mapping the digit name to the ROI
        digits[i] = roi

# load the input image, resize it, and convert it to grayscale
imageOriginal = cv2.imread(args["image"])
image = selectMyHand(imageOriginal)

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image, then initialize the
# list of digit locations
im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = contours.sort_contours(cnts, method="left-to-right")[0]
locs = []

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    if 20 <= h < 40:
        # if height is enough
        # create rectangle for bounding
        rect = (x, y, w, h)
        locs.append(rect)
        cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 255, 0), 1);

cv2.imshow("thresh", thresh)
output = []

for (i, (x, y, w, h)) in enumerate(locs):
    roi = thresh[y:y + h, x:x + w]
    roi = cv2.resize(roi, (57, 88))

    # initialize a list of template matching scores
    scores = []

    # loop over the reference digit name and digit ROI
    for (digit, digitROI) in digits.items():
        # apply correlation-based template matching, take the
        # score, and update the scores list
        result = cv2.matchTemplate(roi, digitROI,
                                   cv2.TM_CCOEFF)
        (_, score, _, _) = cv2.minMaxLoc(result)
        scores.append(score)

    # the classification for the digit ROI will be the reference
    # digit name with the *largest* template matching score
    output.append(cards[int(np.argmax(scores))])

print('Your Cards: ' + ''.join(str(e) for e in output))
cv2.imshow("thresh", imageOriginal)
cv2.waitKey(0)
