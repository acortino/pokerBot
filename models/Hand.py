# encoding: utf-8
from models.Card import REF_VALUE_PERCENT, REF_WIN_PERCENT_PREFLOP, REF_VALUE_STR


class Hand:
    cards = []
    score = 0

    def __init__(self, cards):
        self.cards = cards

    def getCards(self):
        return self.cards

    def getScore(self):
        return self.score

    def getScorePercent(self):
        return self.score * 100

    def toString(self):
        handStr = "Cards: "
        for card in self.cards:
            handStr += card.toString()
        handStr += " \nScore : " + str(self.getScorePercent()) + "%"
        return handStr

    def evaluateScore(self):
        if self.suited():
            lin = REF_VALUE_PERCENT.index(REF_VALUE_STR[self.cards[0].value])
            col = REF_VALUE_PERCENT.index(REF_VALUE_STR[self.cards[1].value])
        else:
            lin = REF_VALUE_PERCENT.index(REF_VALUE_STR[self.cards[1].value])
            col = REF_VALUE_PERCENT.index(REF_VALUE_STR[self.cards[0].value])

        self.score = REF_WIN_PERCENT_PREFLOP[lin][col]

    def suited(self):
        return self.cards[0].color == self.cards[1].color
