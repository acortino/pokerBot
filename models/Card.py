# encoding: utf-8
REF_VALUE_STR = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
REF_COLOR_STR = ["♠", "♣", "♡", "♢"]


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
