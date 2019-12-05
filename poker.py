from random import shuffle
from random import randint as rand
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
        tempNum = 1
        for i in self.handValues: tempNum *= i
        if (math.factorial(self.handValues[-1])/(math.factorial(self.handValues[0]-1))) == tempNum:
          print("You have a straight!")
        else:
          print("You do not have a straight!")

def runGame():
    playerName = input("Play Poker! Enter Name: \n")
    print(playerName + ", are you ready to play poker? Your hands is:\n")
    deck = Deck()
    deck.setupHand(5)
    deck.checkStraight()
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
