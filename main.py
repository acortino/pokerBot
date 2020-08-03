#!/usr/bin/env python
# encoding: utf-8
import argparse
import cv2
from models.OCR import OCR
from models.Hand import Hand

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-r", "--reference", required=True,
                help="path to reference OCR-A image")
args = vars(ap.parse_args())

print("Loading the image...")
image = cv2.imread(args["image"])
print("Loading the reference...")
reference = cv2.imread(args["reference"])
print("Init OCR...")
ocr = OCR(image, reference)
print("Retrieving your hand...")
myHand = Hand(ocr.getMyHand())
print("Evaluating the score...")
myHand.evaluateScore()
print(myHand.toString())
