# dungeon solitaire - recreation of the solitaire game 
# instructions at: https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
import cards
import random
import pyinputplus as pyip
import banner


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
    print(f"You have {getPlayerHealth()} health left.")
    print(f"You are {stepsOut} moves away from the start.")
    pass

def countScore():
    # write out points, breakdown, and final score (max possible is 100)
    kingsFound = playerStats["kings"]
    # 10 per king, face value of treasure, 6 for scroll
    totalScore = (playerStats["kings"] * 10) + (playerStats["scroll"] * 6) + sum([int(item.value) for item in playerStats["treasure"]])
    return kingsFound, totalScore

if __name__ == "__main__":
    banner.title1()

    # game loop. Replay after you lose
    while True:
                
        # initial setup each new game
        deck = [cards.Card(value, suit) for value in cards.values for suit in cards.suits]
        deck.append(cards.Card("Black", "Joker"))
        random.shuffle(deck)
        healthCards = [card for card in deck if card.value in [str(num) for num in range(2, 11)] and card.suit == "Hearts"]
        healthCards.sort(key=lambda x: int(x.value))
        for card in healthCards:
            deck.remove(card)
            
        direction = "delve"
        stepsOut = 0
        lost = False
        playedCards = []  # store a multi-dimensional list of lists, with inner lists representing one "step"

        playerStats = {
            "burnt torches": 0,
            "scroll": 0,
            "kings": 0,
            "berserk": 0,
            "disarm": 0,
            "lock pick": 0,
            "dodge": 0,
            "treasure": []
        }
        # loop of moves. Each cycle is one step further
        while True:
            # show player stats
            showStats()
            tempTreasure = {
                "queens": 0,
                "treasure": 0,
                "kings": 0,
                "scroll": 0
            }

            moveCards = []  # list of all cards played in one move / "step"

            if direction == "delve" and stepsOut > 1:
                turnAroundInput = pyip.inputInt("Would you like to (1) continue the delve or (2) begin to head back? ", min=1, max=2)
                if turnAroundInput == 2:
                    direction = "retreat"

            # place cards on top of each other until a single move is over. ie battling a monster
            while True:

                # draw top card from deck
                drawnCard = deck[-1]
                moveCards.append(drawnCard)
                deck.remove(drawnCard)
                stepsOut = stepsOut + 1 if direction == "delve" else stepsOut - 1

                # determine if card is action card or not
                actionCard = True

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
                    tempTreasure["scroll"] += 1

                elif drawnCard.value == "Queen":
                    # add divine favor if won
                    tempTreasure["queens"] += 1

                elif drawnCard.value == "King":
                    # add king if won
                    tempTreasure["kings"] += 1

                elif drawnCard.suit == "Spades":
                    # monster
                    if actionCard:
                        print("You've encountered a monster!")

                elif drawnCard.suit == "Diamonds":
                    # trap / treasure

                    if actionCard:
                        print("You've encountered a trap!")
                else:
                    # clubs - sealed doors
                    if actionCard:
                        print("You've encountered a sealed door!")

                playerHealth = getPlayerHealth()
                if checkIfLost(playerStats["burnt torches"], len(deck), playerHealth):
                    # banner.die()
                    print("Game over!")
                    lost = True
                    break
                # break  # for testing
    
            playedCards.append(moveCards)

            if lost:
                break
            playerHealth = getPlayerHealth()

            # if they don't lose within the turn, they get their treasure
            playerStats["scroll"] += tempTreasure["scroll"]
            playerStats["kings"] += tempTreasure["kings"]
            playerStats["treasure"] += tempTreasure["treasure"]

            if stepsOut == 0 and direction == "retreat":
                # returned safely
                print("You returned safely! Let's count your treasure.")
                countScore()
 

        again = pyip.inputYesNo("Would you like to play again? (y/n) ")
        if again == "no":
            break
    print("Thanks for playing!")