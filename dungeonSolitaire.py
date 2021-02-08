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
    "Diamonds": "disarm",
    "Hearts": "dodge blow"
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
    print(f"You are {stepsOut} moves away from the start.")
    print(f"Health: {getPlayerHealth()}")
    for key, value in playerStats.items():
        if len(value) != 0:
            print(f"{key.title()}: {len(value)}")

def countScore():
    # write out points, breakdown, and final score (max possible is 100)
    kingsFound = playerStats["kings"]
    # 10 per king, face value of treasure, 6 for scroll
    try:
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
        "King": 10, "Black": 6, "Jack": 0, "Joker": 6, "Queen":0
    }
    # add values for other card.values -> "1":1, "2": 2, etc
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

def chooseCard(cardList, goBack=True):
    """Prints a list of card names and allows user
    to choose a card based on number.
    Returns corresponding card object
    goBack determines if you want the option to go back"""

    assert len(cardList) > 1, "List of cards must have more than 1 item"

    print("Choose a card: ")
    for index, cardObj in enumerate(cardList):
        print(f"{index + 1}. {cardObj.name}")
    if goBack:
        print(f"{len(cardList) + 1}. Go Back")
        numChoice = pyip.inputInt("Enter a number: ", min=1, max=len(cardList) + 1)
    else:
        numChoice = pyip.inputInt("Enter a number: ", min=1, max=len(cardList))

    if numChoice <= len(cardList):
        chosenObj = cardList[numChoice - 1]
    else:
        chosenObj = "Go Back"
    return chosenObj

def showPastPlays():
    for index, moveCards in enumerate(playedCards):
        print(f"Move {index + 1}:")
        for card in moveCards:
            print(card.name)
        print()

    if len(discard) > 0:
        print("Discard pile: ")
        for card in discard:
            print(card.name)
        print()

    if hasItemsInHand():
        print("The hand: ")
        for cardList in playerStats.values():
            for card in cardList:
                print(card.name)

def hasItemsInHand():
    """Returns true if there are items in the player's hand"""
    for cardList in playerStats.values():
        if len(cardList) > 0:
            return True
    return False

def damageOrDodge(damageTaken):
    global healthCards
    if len(playerStats["dodge"]) > 0:
        # TODO: no damage or one less damage?
        useDodge = pyip.inputYesNo(f"Would you like to use your dodge blow skill to avoid \ntaking {damageTaken} damage? (y/n) ") == "yes"
        if useDodge:
            print("You avoided taking damage!")
            moveCards.append(playerStats["dodge"][0])
            playerStats["dodge"] = []
        else:
            healthCards = loseHealth(healthCards, damageTaken)
            print(f"You take {damageTaken} damage! You have {getPlayerHealth()} health left.")
    else:
        healthCards = loseHealth(healthCards, damageTaken)
        print(f"You take {damageTaken} damage! You have {getPlayerHealth()} health left.")
    return healthCards

if __name__ == "__main__":
    # show intro title banner
    banner.intro()

    if pyip.inputYesNo("Would you like to read the instructions? (y/n) ") == "yes":
        print()
        banner.showInstructions()

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
                    stepsOut -= 1

            # list of all cards played in one move / "step"
            moveCards = []  
            # will be populated with the designated action card. len == 0 if no action card yet
            actionCard = []
            # list of cards used to attempt to beat a monster, door, or trap. Use len() to find num attempts
            actionAttempts = []

            input("Press enter to continue. ")
            clearScreen()
            showStats()
            print()
            # place cards on top of each other until a single move is over. ie battling a monster
            while True:
                endMove = False
                # if there's an action card already, ask if the player wants to use powerups etc instead of drawing
                if len(actionCard) > 0:
                    appropriatePowerup = ENEMY_POWERUPS[actionCard[0].suit]
                    userOptions = ["draw again"]
                    if len(playerStats[appropriatePowerup]) == 1:
                        userOptions.append(f"use {appropriatePowerup} powerup")
                    if len(getValidTreasure(actionCard[0])) > 0 and actionCard[0].suit == "Spades":
                        userOptions.append("use treasure drop")
                    if len(userOptions) > 1:
                        choice = pyip.inputMenu(userOptions, numbered=True)
                    else:
                        input("Press enter to draw again.")
                        choice = userOptions[0]
                    if choice == "use treasure drop":
                        # choose which treasure
                        treasureNames = getValidTreasure(actionCard[0])
                        if len(treasureNames) > 1:
                            discardTreasure = chooseCard(treasureNames)
                        else:
                            discardTreasure = treasureNames[0]
                        if discardTreasure == "Go Back":
                            continue
                        else:
                            # add treasure face down on stack
                            moveCards.append(discardTreasure)
                            # lose treasure
                            logging.debug(f"{discardTreasure.name = }")
                            if discardTreasure.value == "King":
                                playerStats["kings"].remove(discardTreasure)
                            elif discardTreasure.suit in ("Joker", "Black"):
                                playerStats["scroll"].remove(discardTreasure)
                            else:
                                playerStats["treasure"].remove(discardTreasure)
                            tempTreasure = {
                                "queens": [],
                                "treasure": [],
                                "kings": [],
                                "scroll": []
                            }

                        print(f"You used your treasure to get past the {CARD_ALIASES.get(actionCard[0].suit)}!")
                        # finish move
                        break
                    elif choice == f"use {appropriatePowerup} powerup":
                        # lose powerup but pass the level.
                        moveCards.append(playerStats[appropriatePowerup][0])
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
                    # jack is not automatically played
                    moveCards.remove(drawnCard)

                elif drawnCard.value == "Ace":
                    # add burnt torch
                    playerStats["burnt torches"].append(drawnCard)
                    print(f"A torch burnt out! You have burnt {len(playerStats['burnt torches'])} torches.")
                    moveCards.remove(drawnCard)

                elif drawnCard.suit == "Joker":
                    # obtain scroll of light
                    tempTreasure["scroll"].append(drawnCard)
                    print("You found the scroll of light!")
                    moveCards.remove(drawnCard)

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
                            # gain treasure from all moveCards
                            treasureGained = []
                            for treasureCard in moveCards:
                                if treasureCard.suit == "Diamonds":
                                    treasureGained.append(treasureCard)
                            if len(treasureGained) == len(moveCards):
                                # if all are treasure cards, leave one behind (choose)
                                print("\nYou must choose one treasure card to leave behind to mark your turn.")
                                # choose card to leave behind
                                treasureLeft = chooseCard(moveCards, goBack=False)
                                treasureGained.remove(treasureLeft)
                                print(f"You left behind the {treasureLeft.name}!\n")
                            tempTreasure["treasure"].extend(treasureGained)
                            moveCards2 = [card for card in moveCards if card not in treasureGained]
                            moveCards = moveCards2
                            # end turn
                            break
                        else:
                            if actionCard[0].suit == "Spades":
                                # monster
                                damageTaken = int(actionCard[0].value) - int(drawnCard.value)
                                healthCards = damageOrDodge(damageTaken)


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
                                if len(playerStats["lock pick"]) > 0:
                                    useSkill = pyip.inputYesNo(f"You must discard {numDiscarded} cards. Would you like to use a lock pick skill instead? (y/n) ") == "yes"

                                    if useSkill:
                                        moveCards.append(playerStats["lock pick"][0])
                                        playerStats["lock pick"] = []
                                        break

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
                    banner.gameOver()
                    # print("Game over!")
                    lost = True
                    break
                elif endMove:
                    break
                print()
    
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
                print("\nYou returned safely! Let's count your treasure.")
                kingsFound, score = countScore()
                print(f"\nYour score is {len(kingsFound)} / {score}. (Kings / Total Score).")
                break
 
        showPast = pyip.inputYesNo("\nWould you like to see your moves from this game? (y/n) ")
        if showPast == "yes":
            print()
            showPastPlays()

        again = pyip.inputYesNo("\nWould you like to play again? (y/n) ")
        if again == "no":
            break
        else:
            clearScreen()
    print("\nThanks for playing!\n")
    banner.showCredits()