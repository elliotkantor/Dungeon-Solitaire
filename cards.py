import random

hasJokers = True

values = "King Queen Jack 10 9 8 7 6 5 4 3 2 1".split()
suits = "Diamonds Spades Hearts Clubs".split()

allCards = [value + " of " + suit 
    for suit in suits 
    for value in values]

if hasJokers:
    allCards.append("Black Joker")
    allCards.append("Red Joker")

def reshuffle():
    global availableCards
    availableCards = allCards[:]
    random.shuffle(availableCards)
    discard = []

reshuffle()

def drawCard():
    chosenCard = random.choice(availableCards)
    availableCards.remove(chosenCard)
    return chosenCard

def dealCards(cardsPerPlayer, numPlayers, numDecks=1):
    assert cardsPerPlayer * numPlayers <= len(availableCards) * numDecks, f"There are only {len(availableCards) * numDecks} cards but you need {cardsPerPlayer * numPlayers} cards."
    playerHands = []
    for player in range(numPlayers):
        singleHand = []
        for card in range(cardsPerPlayer):
            singleHand.append(drawCard())
        playerHands.append(singleHand)
    return playerHands
    
def discard(card):
    discard.append(card)
    availableCards.remove(card)

if __name__ == "__main__":
    hands = dealCards(5, 3)
    for hand in hands:
        print(hand)