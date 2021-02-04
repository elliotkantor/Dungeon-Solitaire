import random

# decide whether deck has 2 jokers
hasJokers = True

# all possible values and suits
values = "King Queen Jack 10 9 8 7 6 5 4 3 2 1".split()
suits = "Diamonds Spades Hearts Clubs".split()

# class for a singular card
class Card:
    """Card object to add card functionality"""

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        if not "Joker" in (self.value, self.suit):
            self.name = self.value + " of " + self.suit
        else:
            self.name = self.value + " " + self.suit


def reshuffle():
    """Shuffle all cards and remove cards from the discard"""
    global availableCards
    availableCards = allCards[:]
    random.shuffle(availableCards)
    discard = []


def drawCard():
    """Return one random card from the deck and move the card to the discard pile"""
    chosenCard = random.choice(availableCards)
    availableCards.remove(chosenCard)
    discard.append(chosenCard)
    return chosenCard


def dealCards(cardsPerPlayer, numPlayers, numDecks=1):
    assert (
        cardsPerPlayer * numPlayers <= len(availableCards) * numDecks
    ), f"There are only {len(availableCards) * numDecks} cards but you need {cardsPerPlayer * numPlayers} cards."
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


# if __name__ == "__main__":
#     hands = dealCards(5, 3)
#     for hand in hands:
#         print(hand)

# make a list of all cards, in a sorted order
if __name__ == "__main__":
    allCards = [Card(value, suit) for suit in suits for value in values]

    if hasJokers:
        allCards.append(Card("Black", "Joker"))
        allCards.append(Card("Red", "Joker"))

    reshuffle()