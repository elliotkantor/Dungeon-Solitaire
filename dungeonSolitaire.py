# dungeon solitaire - recreation of the solitaire game 
# instructions at: https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
import cards
import random

deck = [cards.Card(value, suit) for value in cards.values for suit in cards.suits]
deck.append(cards.Card("Black", "Joker"))
random.shuffle(deck)
healthCards = [card for card in deck if card.value in [str(num) for num in range(2, 11)] and card.suit == "Hearts"]
healthCards.sort(key=lambda x: int(x.value))
for card in healthCards:
    deck.remove(card)

def getPlayerHealth():
    playerHealth = int(healthCards[-1].value) - 1
    return playerHealth

def checkIfLost(numBurntTorches, numCardsLeft, health):
    """Returns true if lost, false if did not lose"""
    if numBurntTorches >= 4 or numCardsLeft <= 0 or playerHealth <= 0:
        return True
    return False

if __name__ == "__main__":
    # for card in healthCards:
    #     print(card.name)
    while True:
        # show player stats

        # draw top card from deck
        drawnCard = deck[-1]
        deck.remove(drawnCard)
        if drawnCard.value == "Jack":
            # add to powerups
            pass
        elif drawnCard.value == "Ace":
            # add burnt torch
            pass
        elif drawnCard.suit == "Joker":
            # obtain scroll of light
            pass
        elif drawnCard.value == "Queen":
            # add divine favor if won
            pass
        elif drawnCard.value == "King":
            # add king if won
            pass
        elif drawnCard.suit == "Spades":
            # monster
            pass
        elif drawnCard.suit == "Diamonds":
            # trap / treasure
            pass
        else:
            # clubs - sealed doors
            pass

        # do action depending on if deck is trap, monster, or door, and repeat until passed

        # save player stats
        playerHealth = getPlayerHealth()
        checkIfLost(burntTorches, len(deck), playerHealth)