# dungeon solitaire - recreation of the solitaire game 
# instructions at: https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
import cards
import random

deck = [cards.Card(value, suit) for value in cards.values for suit in cards.suits]
deck.append(cards.Card("Black", "Joker"))
random.shuffle(deck)
healthCards = [card for card in deck if card.value in [str(num) for num in range(2, 11)] and card.suit == "Hearts"]
healthCards.sort(key=lambda x: int(x.value))

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
        playerHealth = getPlayerHealth()
        checkIfLost(burntTorches, len(deck), playerHealth)