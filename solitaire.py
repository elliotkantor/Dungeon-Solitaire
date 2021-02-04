import cards
import random

def setup():
    # deal cards
    deck = cards.availableCards[:]
    random.shuffle(deck)
    playCards = deck[:15]
    pickCards = deck[15:]
    discard = []

    # arrange cards
    prettyDeck = []
    for i in range(1,6):
        prettyDeck.append(playCards[:i])
        for item in playCards[:i]:
            playCards.remove(item)
    del playCards

    # make final stacks for winning
    finalStacks = {
        "hearts": [],
        "clubs": [],
        "diamonds": [],
        "spades": []
    }

# display board
def displayTable(inPlay, finalStacks, discard, available):
    # available and discard
    print(f"Next in available cards: {available[-1]}")
    print(f"There are {len(discard)} cards in discard and {len(available)} cards left to draw from.")
    # print final stacks
    for key, value in finalStacks.items():
        if len(value) > 0:
            print(f"{key.title()}: {len(value)} cards. Top is {value[-1]}.") 
    # print play area
    print()
    for index, column in enumerate(inPlay):
        print(*column, sep=", ")


# check if won
def checkIfWon(finalStacks):
    pass

if __name__ == "__main__":
    while True:
        displayTable(prettyDeck, finalStacks, discard, pickCards)
        moveCards(
            getInput()
        )
        checkIfWon(finalStacks)