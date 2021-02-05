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

def evalueateEncounter(testCard, actionCard):
    if int(testCard.value) >= int(actionCard.value):
        return True
    return False

def getUserInput(jacks, treasure, isMonster=False, monster=cards.Card("0", "Blank")):
    validTreasure = [cardObj for cardObj in treasure if int(cardObj.value) > int(monster.value)]
    if len(jacks) == 1 and len(validTreasure) > 0 and isMonster:
        choice = pyip.inputInt("Would you like to (1) use a powerup, (2) use your treasure to escape, or (3) draw again? ", min=1, max=3)
        if choice == 1:
            choice = "powerup"
        elif choice == 2:
            choice = "treasure"
        else:
            choice = "draw"
    elif len(jacks) == 1:
        choice = pyip.inputInt("Would you like to (1) use a powerup or (2) draw again?", min=1, max=2)
        choice = "powerup" if choice == 1 else "draw"
    elif len(validTreasure) > 0:
        choice = pyip.inputInt("Would you like to (1) use treasure to escape or (2) draw again? ", min=1, max=2)
        choice = "treasure" if choice == 1 else "draw"
    else:
        print("You must draw again.")
        choice = "draw"
    return choice


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
            "burnt torches": [],
            "scroll": [],
            "kings": [],
            "berserk": [],
            "disarm": [],
            "lock pick": [],
            "dodge": [],
            "treasure": []
        }
        # loop of moves. Each cycle is one step further
        while True:
            # show player stats
            showStats()
            tempTreasure = {
                "queens": [],
                "treasure": [],
                "kings": [],
                "scroll": []
            }

            moveCards = []  # list of all cards played in one move / "step"

            if direction == "delve" and stepsOut > 1:
                turnAroundInput = pyip.inputInt("Would you like to (1) continue the delve or (2) begin to head back? ", min=1, max=2)
                if turnAroundInput == 2:
                    direction = "retreat"

            # will be populated with the designated action card. len == 0 if no action card yet
            actionCard = []

            # place cards on top of each other until a single move is over. ie battling a monster
            while True:

                # draw top card from deck
                drawnCard = deck[-1]
                moveCards.append(drawnCard)
                deck.remove(drawnCard)
                stepsOut = stepsOut + 1 if direction == "delve" else stepsOut - 1

                # do action depending on if deck is trap, monster, or door, and repeat until passed
                if drawnCard.value == "Jack":
                    # add to powerups
                    if drawnCard.suit == "Spades":
                        playerStats["berserk"].append(drawnCard)
                    elif drawnCard.suit == "Diamonds":
                        playerStats["disarm"].append(drawnCard)
                    elif drawnCard.suit == "Clubs":
                        playerStats["lock pick"].append(drawnCard)
                    else:
                        playerStats["dodge"].append(drawnCard)

                elif drawnCard.value == "Ace":
                    # add burnt torch
                    playerStats["burnt torches"].append(drawnCard)

                elif drawnCard.suit == "Joker":
                    # obtain scroll of light
                    tempTreasure["scroll"].append(drawnCard)

                elif drawnCard.value == "Queen":
                    # add divine favor if won
                    tempTreasure["queens"].append(drawnCard)

                elif drawnCard.value == "King":
                    # add king if won
                    tempTreasure["kings"].append(drawnCard)

                elif drawnCard.suit == "Spades":
                    # monster
                    if len(actionCard) == 0:
                        print("You've encountered a monster!")
                        actionCard.append(drawnCard)
                    else:
                        # do something with output of evaluate encounter and break statement
                        userChoice = getUserInput()
                        if userChoice == "draw":
                            evalueateEncounter(drawnCard, actionCard[0])

                elif drawnCard.suit == "Diamonds":
                    # trap / treasure
                    if len(actionCard) == 0:
                        print("You've encountered a trap!")
                        actionCard.append(drawnCard)
                    else:
                        evalueateEncounter(drawnCard, actionCard[0])

                else:
                    # clubs - sealed doors
                    if len(actionCard) == 0:
                        print("You've encountered a locked door!")
                        actionCard.append(drawnCard)
                    else:
                        evalueateEncounter(drawnCard, actionCard[0])

                playerHealth = getPlayerHealth()
                if checkIfLost(len(playerStats["burnt torches"]), len(deck), playerHealth):
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
            playerStats["scroll"].append(tempTreasure["scroll"])
            playerStats["kings"].append(tempTreasure["kings"])
            playerStats["treasure"].append(tempTreasure["treasure"])

            if stepsOut == 0 and direction == "retreat":
                # returned safely
                print("You returned safely! Let's count your treasure.")
                countScore()
 

        again = pyip.inputYesNo("Would you like to play again? (y/n) ")
        if again == "no":
            break
    print("Thanks for playing!")