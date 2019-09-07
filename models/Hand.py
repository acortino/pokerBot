# encoding: utf-8

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
        self.score = 0.32
