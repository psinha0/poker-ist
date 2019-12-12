from random import shuffle
from collections import Counter
import math
import re

class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit

  def cardName(self):
    royalCards = {1: "Ace", 11: "Jack", 12: "Queen", 13:"King"}
    cardValue = royalCards[self.value] if self.value in royalCards else self.value
    return '%s of %s'%(cardValue, self.suit)

  def cardReveal(self):
      print(self.cardName())

  def cardSuit(self):
      return self.suit

  def cardValue(self):
      return self.value

class Deck:
    def __init__(self):
        self.suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
        self.cardDeck = [Card(value, suit) for suit in self.suits for value in range(1,14)]

    def deckShuffle(self):
        for i in range(10):
            shuffle(self.cardDeck)

    def drawCard(self):
        randomCard = self.cardDeck.pop()
        return randomCard

    def drawExchange(self, placement):
        self.cardHand.pop(placement)
        self.cardHand.insert(placement, self.drawCard())
        return self.cardHand

    def drawReveal(self):
        randomCard = self.cardDeck.pop()
        randomCard.cardReveal()
        return randomCard

    def drawHand(self, size):
        self.cardHand = [self.drawCard() for i in range(size)]
        return self.cardHand

    def handReveal(self):
        self.tempHand = len(self.cardHand)
        for i in range(self.tempHand):
            self.cardHand[i].cardReveal()

    def setupHand(self, size):
        self.size = size
        self.deckShuffle()
        self.drawHand(size)
        self.handReveal()

    def checkStraight(self):
        self.handValues = []
        for i in range(self.tempHand):
            self.handValues.append(self.cardHand[i].cardValue())
        self.handValues.sort()
        self.highestCard = self.handValues[-1]
        self.lowestCard = self.handValues[0]
        tempNum = 1
        for i in self.handValues: tempNum *= i
        if (math.factorial(self.handValues[-1])/(math.factorial(self.handValues[0]-1))) == tempNum:
          return (18, "You have a straight!", self.highestCard)
        else:
          return (0, 0, 0)

    def checkFlush(self):
      self.handSuits = []
      flushCheck = False
      for i in range(self.tempHand):
        self.handSuits.append(self.cardHand[i].cardSuit())
      '''for i in range(self.tempHand-1):
        if self.handSuits[0] == self.handSuits[i+1]:
          flushCheck = True
        else:
          flushCheck = False
          break'''
      if len(set(self.handSuits)) == 1:
        return (19, "You have a flush!", self.highestCard)
      else:
        return (0, 0, 0)

    def checkStraightFlush(self):
      if (self.checkStraight() == 18) and (self.checkFlush() == 19):
        return (22, "You have a straight flush!", self.highestCard)
      else:
        return (0, 0, 0)

    def checkOfAKind(self):
      self.handValues = []
      for i in range(self.tempHand):
          self.handValues.append(self.cardHand[i].cardValue())
      self.handValues.sort()
      for i in range(6):
        cardDuplicate = [value for value, count in Counter(self.handValues).items() if count > i]
        if not cardDuplicate:
          cardDuplicate = [value for value, count in Counter(self.handValues).items() if count == i]
          typeOfKind = i
          break
      if len(cardDuplicate) == 2:
        return (16, "You have two pairs!", 0)
      elif len(cardDuplicate) == 1:
        if typeOfKind == 3:
          cardDuplicate = [value for value, count in Counter(self.handValues).items() if count == 2]
          if cardDuplicate:
            return (20, "You have a full house!", self.highestCard)
          else:
            cardDuplicate = [value for value, count in Counter(self.handValues).items() if count == 3]
            return (17, "You have three of a kind!", cardDuplicate[0])
        if typeOfKind == 4:
          return (21, "You have four of a kind!", cardDuplicate[0])
        else:
          return (15, "You have one pair!", cardDuplicate[0])
      else:
        return (0, 0, 0)

    def checkHighestValue(self):
      if self.lowestCard == 1:
        self.highestCard = 14
      return (self.highestCard, 0, 0)

    def checkAllCards(self):
     if self.checkStraightFlush()[0] == 22:
      return (22, "You have a straight flush!", self.checkStraightFlush()[2])
     elif self.checkFlush()[0] != 19 and self.checkStraight()[0] != 18:
      if self.checkOfAKind()[0] > 0:
        return (self.checkOfAKind()[0], self.checkOfAKind()[1], self.checkOfAKind()[2])
      else:
        return self.checkHighestValue()
     else:
      return (self.checkStraight()[0], self.checkStraight()[1], self.checkStraight()[2])
      return (self.checkFlush()[0], self.checkFlush()[1], self.checkFlush()[2])

def runGame():
    playerName = input("Play Poker! Enter Name: \n")
    print(playerName + ", are you ready to play poker? Your hands is:\n")
    deck = Deck()
    deck.setupHand(5)
    numberOfPlayers = 2
    while True:
      try:
        inputCardReplace = input("Which card would you like to exchange? (Enter the card position number, seperated by spaces)\n")
        cardReplace = [int(i) for i in re.split('[ |, |]+', inputCardReplace.strip('[]'))]
        for i in range(len(cardReplace)):
          replacePlacement = cardReplace[i]
          if replacePlacement in range(1, 6):
            deck.drawExchange(replacePlacement-1)
            cardsExchanged = True
          else:
            print("A number between 1 and 5 please!")
            cardsExchanged = False
        deck.handReveal()
        if cardsExchanged:
          break
      except ValueError:
        print("Enter a number please!")
    print(deck.checkAllCards()[1])
    playerScores = {}
    duplicateScores = {}
    duplicateScores[0] = deck.checkAllCards()[2]
    playerScores[0] = deck.checkAllCards()[0]
    for i in range(numberOfPlayers):
      print()
      deck.setupHand(5)
      playerScores[i+1] = deck.checkAllCards()[0]
      duplicateScores[i+1] = deck.checkAllCards()[2]
    scoreNumbers = {sortedScores: i for sortedScores, i in sorted(playerScores.items(), key=lambda item: item[1])}
    playerDuplicatesTemp = [(i,j) for i in scoreNumbers for j in scoreNumbers if (scoreNumbers[i]==scoreNumbers[j]) and i != j and scoreNumbers[i] > 14 and scoreNumbers[j] > 14]
    if playerDuplicatesTemp:
      playerDuplicates = playerDuplicatesTemp[0]
      scoreDuplicates = []
      inv_duplicateScores = {v: k for k, v in duplicateScores.items()}
      for i in playerDuplicates:
        scoreDuplicates.append(duplicateScores[i])
      scoreDuplicates.sort()
      winnerScore = scoreDuplicates[-1]
      winnerPlayer = (inv_duplicateScores[winnerScore])+1
    else:
      winnerPlayer = (list(scoreNumbers.keys())[-1])+1
    print("Player " + str(winnerPlayer) + " wins!")
    
   
if __name__ == "__main__":
    runGame()
