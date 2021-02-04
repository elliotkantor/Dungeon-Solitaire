# dungeon solitaire - recreation of the solitaire game 
# instructions at: https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
import cards
import random
import pyinputplus as pyip


def getPlayerHealth():
    playerHealth = int(healthCards[-1].value) - 1
    return playerHealth

def checkIfLost(numBurntTorches, numCardsLeft, health):
    """Returns true if lost, false if did not lose"""
    if (numBurntTorches >= 4 and playerStats["scroll"] == 0) or numCardsLeft <= 0 or playerHealth <= 0:
        return True
    if numBurntTorches == 4 and playerStats["scroll"] == 1:
        print("You've burnt four torches, so you use the Scroll of Light!")
        playerStats["scroll"] = 0
    return False

def showStats():
    # print(f"You have {getPlayerHealth()} health left.")
    pass

if __name__ == "__main__":

    while True:
                
        deck = [cards.Card(value, suit) for value in cards.values for suit in cards.suits]
        deck.append(cards.Card("Black", "Joker"))
        random.shuffle(deck)
        healthCards = [card for card in deck if card.value in [str(num) for num in range(2, 11)] and card.suit == "Hearts"]
        healthCards.sort(key=lambda x: int(x.value))
        for card in healthCards:
            deck.remove(card)
            
        direction = "delve"
        stepsOut = 0

        playerStats = {
            "burnt torches": 0,
            "scroll": 0,
            "kings": 0,
            "berserk": 0,
            "disarm": 0,
            "lock pick": 0,
            "dodge": 0
        }

        while True:
            # show player stats
            showStats()

            # draw top card from deck
            drawnCard = deck[-1]
            deck.remove(drawnCard)

            # do action depending on if deck is trap, monster, or door, and repeat until passed
            if drawnCard.value == "Jack":
                # add to powerups
                if drawnCard.suit == "Spades":
                    playerStats["berserk"] += 1
                elif drawnCard.suit == "Diamonds":
                    playerStats["disarm"] += 1
                elif drawnCard.suit == "Clubs":
                    playerStats["lock pick"] += 1
                else:
                    playerStats["dodge"] += 1

            elif drawnCard.value == "Ace":
                # add burnt torch
                playerStats["burnt torches"] += 1

            elif drawnCard.suit == "Joker":
                # obtain scroll of light
                playerStats["scroll"] += 1

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

            stepsOut += 1
            # save player stats
            playerHealth = getPlayerHealth()
            if checkIfLost(playerStats["burnt torches"], len(deck), playerHealth):
                print("You lost!")
                break
        again = pyip.inputYesNo("Would you like to play again? (y/n) ")
        if again == "no":
            break
    print("Thanks for playing!")