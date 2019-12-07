from random import shuffle
from random import randint as rand
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
          return 18
        else:
          return 0

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
        return 19
      else:
        return 0

    def checkStraightFlush(self):
      if (self.checkStraight() == 18) and (self.checkFlush() == 19):
        return 22

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
        print("You have two pairs!")
        return 16
      elif len(cardDuplicate) == 1:
        if typeOfKind == 3:
          cardDuplicate = [value for value, count in Counter(self.handValues).items() if count == 2]
          if cardDuplicate:
            print("You have a full house!")
            return 20
          else:
            print("You have three of a kind!")
            return 17
        if typeOfKind == 4:
          print("You have four of a kind!")
          return 21
        else:
          print("You have one pair!")
          return 15
      else:
        return 0

    def checkHighestValue(self):
      if self.lowestCard == 1:
        self.highestCard = 14
      return self.highestCard

def runGame():
    playerName = input("Play Poker! Enter Name: \n")
    print(playerName + ", are you ready to play poker? Your hands is:\n")
    deck = Deck()
    deck.setupHand(5)
    while True:
      try:
        inputCardReplace = input("Which card would you like to exchange? (Enter the card position number)\n")
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
     

   
if __name__ == "__main__":
    runGame()
