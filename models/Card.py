# encoding: utf-8
REF_VALUE_STR = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
REF_COLOR_STR = ["♠", "♣", "♡", "♢"]
COLOR_BLACK = 0
COLOR_GREEN = 1
COLOR_RED = 2
COLOR_BLUE = 3
REF_COLOR_RGB_RED = [178, 7, 27]
REF_COLOR_RGB_BLUE = [12, 49, 131]
REF_COLOR_RGB_GREEN = [55, 187, 34]
REF_COLOR_RGB_BLACK = [0, 0, 0]


class Card:
    value = 0;
    color = 0;

    def __init__(self, value, color):
        self.color = color
        self.value = value

    def getColor(self):
        return self.color

    def getValue(self):
        return self.value

    def toString(self):
        return "[" + REF_VALUE_STR[self.value] + REF_COLOR_STR[self.color] + "]"
