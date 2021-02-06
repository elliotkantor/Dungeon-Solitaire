# dungeon solitaire - recreation of the solitaire game 
# instructions at: https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
import cards
import random
import pyinputplus as pyip
import banner
import logging
from os import system, name
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')
logging.disable(logging.CRITICAL) # to disable logs after this

# names of playing cards translated to game terms
CARD_ALIASES = {
    "Spades": "monster",
    "Clubs": "door",
    "Diamonds": "trap"
}

ENEMY_POWERUPS = {
    "Spades": "berserk",
    "Clubs": "lock pick",
    "Diamonds": "disarm"
}

def clearScreen():
	# windows
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

def getPlayerHealth():
    playerHealth = len(healthCards)
    return playerHealth

def checkIfLost(numBurntTorches, numCardsLeft, health):
    """Returns true if lost, false if did not lose"""
    global torchThreshhold
    torchThreshold = 4
    if (numBurntTorches >= torchThreshold and len(playerStats["scroll"]) == 0) or numCardsLeft <= 0 or health <= 0:
        return True
    if numBurntTorches == torchThreshold and len(playerStats["scroll"]) == 1:
        print("You've burnt four torches, so you use the Scroll of Light!")
        playerStats["scroll"] = []
        torchThreshold += 1
        # didn't lose yet so return False
    return False

def showStats():
    print(f"You have {getPlayerHealth()} health left.")
    print(f"You are {stepsOut} moves away from the start.")

def countScore():
    # write out points, breakdown, and final score (max possible is 100)
    kingsFound = playerStats["kings"]
    # 10 per king, face value of treasure, 6 for scroll
    try:
        # TODO: ensure there's no logic error here
        treasureValues = sum([int(item.value) for item in playerStats["treasure"]])
    except:
        treasureValues = 0
    totalScore = (len(playerStats["kings"]) * 10) + (len(playerStats["scroll"]) * 6) + treasureValues
    return kingsFound, totalScore

def evalueateEncounter(testCard, actionCard):
    """Returns true if you pass the encounter, false if you don't (and try again)"""
    if int(testCard.value) >= int(actionCard.value):
        return True
    return False


def getValidTreasure(actionCard):
    """Returns a list of valid treasure to be used on a given action card,
    based on treasure in playerStats
    Input: A single card object for filtering
    Return: list of card objects"""
    treasureVals = {
        # based on card.value
        "King": 10, "Joker": 6
    }
    for s, i in [(str(i), i) for i in range(2,11)]:
        treasureVals[s] = i

    treasure = []
    for king in playerStats["kings"]:
        treasure.append(king)
    for scroll in playerStats["scroll"]:
        treasure.append(scroll)
    for card in playerStats["treasure"]:
        treasure.append(card)
    # filter only available treasure
    availableTreasure = [card for card in treasure if treasureVals[card.value] >= int(actionCard.value)]
    return availableTreasure

def loseHealth(healthCards, amountLost):
    """Remove health cards. Does not implicitly update playerHealth"""
    healthCards = healthCards[:-amountLost]
    return healthCards

def showInstructions():
    # TODO: add detailed instructions
    print("Insert instructions here")

if __name__ == "__main__":
    # show intro title banner
    banner.intro()

    if pyip.inputYesNo("Would you like to read the instructions? (y/n) ") == "yes":
        showInstructions()

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
        discard = []

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


            if direction == "delve" and stepsOut > 1:
                turnAroundInput = pyip.inputInt("Would you like to (1) continue the delve or (2) begin to head back? ", min=1, max=2)
                if turnAroundInput == 2:
                    direction = "retreat"

            # list of all cards played in one move / "step"
            moveCards = []  
            # will be populated with the designated action card. len == 0 if no action card yet
            actionCard = []
            # list of cards used to attempt to beat a monster, door, or trap. Use len() to find num attempts
            actionAttempts = []

            input("Press enter to continue. ")
            clearScreen()
            # place cards on top of each other until a single move is over. ie battling a monster
            while True:
                endMove = False
                # if there's an action card already, ask if the player wants to use powerups etc instead of drawing
                if len(actionCard) > 0:
                    appropriatePowerup = ENEMY_POWERUPS[actionCard[0].suit]
                    userOptions = ["draw again"]
                    if len(playerStats[appropriatePowerup]) == 1:
                        userOptions.append(f"use {appropriatePowerup} powerup")
                    if len(getValidTreasure(actionCard[0])) > 0:
                        userOptions.append("use treasure drop")
                    if len(userOptions) > 1:
                        choice = pyip.inputMenu(userOptions, numbered=True)
                    else:
                        input("Press enter to draw again.")
                        choice = userOptions[0]
                    if choice == "use treasure drop":
                        # choose which treasure
                        treasureNames = [(card.name, card) for card in getValidTreasure(actionCard[0])]
                        treasureNames.append(("Go back", "Go back"))
                        discardTreasure = pyip.inputMenu([t[0] for t in treasureNames], numbered=True, prompt="Choose which card to remove: \n")
                        if discardTreasure == "Go back":
                            continue
                        else:
                            # find object where name matches
                            matchingName = []
                            for name, obj in treasureNames:
                                if name == discardTreasure:
                                    matchingName.append(obj)
                            assert len(matchingName) == 1, "Must find exactly one matching name"
                            # add treasure face down on stack
                            moveCards.append(matchingName[0])
                            logging.debug(f"Chose {discardTreasure} so removed {matchingName[0]}.")
                            # lose treasure
                            if matchingName[0].suit == "King":
                                playerStats["kings"].remove(matchingName[0])
                            elif matchingName[0].suit in ("Joker", "Black"):
                                playerStats["scroll"].remove(matchingName[0])
                            else:
                                playerStats["treasure"].remove(matchingName[0])

                        print(f"You used your treasure to get past the {CARD_ALIASES.get(actionCard[0].suit)}!")
                        # finish move
                        break
                    elif choice == f"use {appropriatePowerup} powerup":
                        # lose powerup but pass the level.
                        playerStats[appropriatePowerup] = []
                        print(f"You used a powerup and beat the {CARD_ALIASES.get(actionCard[0].suit)}!")
                        break
                    else:
                        # draw again
                        pass
                else:
                    input("Press enter to draw a card. ")

                # draw top card from deck
                drawnCard = deck[-1]
                moveCards.append(drawnCard)
                deck.remove(drawnCard)

                logging.debug(f"drew: {drawnCard.name}")

                # do action depending on if deck is trap, monster, or door, and repeat until passed
                if drawnCard.value == "Jack":
                    # add to powerups
                    if drawnCard.suit == "Spades":
                        playerStats["berserk"].append(drawnCard)
                        print("You gained a Go Berserk powerup!")
                    elif drawnCard.suit == "Diamonds":
                        playerStats["disarm"].append(drawnCard)
                        print("You gained a Disarm powerup!")
                    elif drawnCard.suit == "Clubs":
                        playerStats["lock pick"].append(drawnCard)
                        print("You gained a Lock Pick powerup!")
                    else:
                        playerStats["dodge"].append(drawnCard)
                        print("You gained a Dodge Blow powerup!")

                elif drawnCard.value == "Ace":
                    # add burnt torch
                    playerStats["burnt torches"].append(drawnCard)
                    print(f"A torch burnt out! You have burnt {len(playerStats['burnt torches'])} torches.")

                elif drawnCard.suit == "Joker":
                    # obtain scroll of light
                    tempTreasure["scroll"].append(drawnCard)
                    print("You gain the scroll of light!")

                elif drawnCard.value == "Queen":
                    # add divine favor if won
                    tempTreasure["queens"].append(drawnCard)
                    if len(tempTreasure["queens"]) == 1:
                        if len(actionCard) > 0:
                            # if the queen can be used on an action card, use it 
                            print("The divine intervention saved you!")
                            break
                        else:
                            print("The divine queen is with you! You will pass your next enemy.")
                    else:
                        # already have a queen
                        print("You are extra blessed! Another queen is with you.")

                elif drawnCard.value == "King":
                    # add king if won
                    tempTreasure["kings"].append(drawnCard)
                    print("You found a king! If you pass this move, you can keep it.")
                else:
                    # card must be either an action or encounter card
                    if len(actionCard) == 0:
                        # the card drawn is an action card
                        print(f"You've encountered a {CARD_ALIASES.get(drawnCard.suit)} of strength {drawnCard.value}!")
                        actionCard.append(drawnCard)

                        # if you have a divine intervention to use, use it immediately
                        if len(tempTreasure["queens"]) > 0:
                            print("The divine queen saves you!")
                            break
                    else:
                        # card must beat the action card
                        print(f"You draw a {drawnCard.name}!")
                        passesEncounter = evalueateEncounter(drawnCard, actionCard[0])
                        logging.debug(f"{passesEncounter = }")
                        if passesEncounter or len(tempTreasure["queens"]) > 0:
                            print(f"You beat the {CARD_ALIASES.get(actionCard[0].suit)}!")
                            break
                        else:
                            # TODO: drawn card does not pass. Depending on action card, lose health or cards, etc
                            if actionCard[0].suit == "Spades":
                                # monster
                                damageTaken = int(actionCard[0].value) - int(drawnCard.value)
                                healthCards = loseHealth(healthCards, damageTaken)
                                print(f"You take {damageTaken} damage!")
                                healthCards = loseHealth(healthCards, damageTaken)

                            elif actionCard[0].suit == "Diamonds":
                                # trap
                                damageTaken = int(actionCard[0].value) - int(drawnCard.value)
                                print(f"You take {damageTaken} damage and your turn is over. You do not get treasure.")
                                healthCards = loseHealth(healthCards, damageTaken)
                                # don't get treasure
                                tempTreasure = {
                                    "queens": [],
                                    "treasure": [],
                                    "kings": [],
                                    "scroll": []
                                }
                                # end the move after checking health
                                endMove = True
                            else:
                                # door
                                numDiscarded = int(actionCard[0].value) - int(drawnCard.value)
                                if len(getValidTreasure(actionCard[0])) > 0:
                                    useTreasure = pyip.inputYesNo(f"You must discard {numDiscarded} cards. Would you like to use a treasure drop instead? (y/n) ")
                                    if useTreasure == "yes":
                                        # TODO: choose and use treasure
                                        pass
                                print(f"You lose {numDiscarded} cards to the discard pile.")
                                for card in range(numDiscarded):
                                    drawnCard = deck[-1]
                                    if drawnCard.suit == "Ace":
                                        playerStats["burnt torches"].append(drawnCard)
                                        print(f"A discarded card is a burnt torch. You now have burnt {len(playerStats['burnt torch'])} torches.")
                                    discard.append(drawnCard)
                                    deck.remove(drawnCard)
                                # no treasure
                                tempTreasure = {
                                    "queens": [],
                                    "treasure": [],
                                    "kings": [],
                                    "scroll": []
                                }
                                endMove = True

                
                playerHealth = getPlayerHealth()
                if checkIfLost(len(playerStats["burnt torches"]), len(deck), playerHealth):
                    # banner.die()
                    print("Game over!")
                    lost = True
                    break
                elif endMove:
                    break
    
            # change number of steps from start each move (not each card, though)
            if direction == "delve":
                stepsOut += 1
            else:
                stepsOut -= 1
            playedCards.append(moveCards)

            if lost:
                break

            # if they don't lose within the turn, they get their treasure
            playerStats["scroll"].extend(tempTreasure["scroll"])
            playerStats["kings"].extend(tempTreasure["kings"])
            playerStats["treasure"].extend(tempTreasure["treasure"])

            if stepsOut <= 0 and direction == "retreat":
                # returned safely
                print("You returned safely! Let's count your treasure.")
                kingsFound, score = countScore()
                print(f"Your score is {len(kingsFound)} / {score}. (Kings / Total Score).")
                break
 
        again = pyip.inputYesNo("Would you like to play again? (y/n) ")
        if again == "no":
            break
        else:
            clearScreen()
    print("Thanks for playing!")