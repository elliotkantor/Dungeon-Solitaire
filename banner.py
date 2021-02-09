def intro():
    print("""
▓█████▄  █    ██  ███▄    █   ▄████ ▓█████  ▒█████   ███▄    █       
▒██▀ ██▌ ██  ▓██▒ ██ ▀█   █  ██▒ ▀█▒▓█   ▀ ▒██▒  ██▒ ██ ▀█   █       
░██   █▌▓██  ▒██░▓██  ▀█ ██▒▒██░▄▄▄░▒███   ▒██░  ██▒▓██  ▀█ ██▒      
░▓█▄   ▌▓▓█  ░██░▓██▒  ▐▌██▒░▓█  ██▓▒▓█  ▄ ▒██   ██░▓██▒  ▐▌██▒      
░▒████▓ ▒▒█████▓ ▒██░   ▓██░░▒▓███▀▒░▒████▒░ ████▓▒░▒██░   ▓██░      
 ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ░▒   ▒ ░░ ▒░ ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒       
 ░ ▒  ▒ ░░▒░ ░ ░ ░ ░░   ░ ▒░  ░   ░  ░ ░  ░  ░ ▒ ▒░ ░ ░░   ░ ▒░      
 ░ ░  ░  ░░░ ░ ░    ░   ░ ░ ░ ░   ░    ░   ░ ░ ░ ▒     ░   ░ ░       
   ░       ░              ░       ░    ░  ░    ░ ░           ░       
 ░                                                                   
  ██████  ▒█████   ██▓     ██▓▄▄▄█████▓ ▄▄▄       ██▓ ██▀███  ▓█████ 
▒██    ▒ ▒██▒  ██▒▓██▒    ▓██▒▓  ██▒ ▓▒▒████▄    ▓██▒▓██ ▒ ██▒▓█   ▀ 
░ ▓██▄   ▒██░  ██▒▒██░    ▒██▒▒ ▓██░ ▒░▒██  ▀█▄  ▒██▒▓██ ░▄█ ▒▒███   
  ▒   ██▒▒██   ██░▒██░    ░██░░ ▓██▓ ░ ░██▄▄▄▄██ ░██░▒██▀▀█▄  ▒▓█  ▄ 
▒██████▒▒░ ████▓▒░░██████▒░██░  ▒██▒ ░  ▓█   ▓██▒░██░░██▓ ▒██▒░▒████▒
▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒░▓  ░░▓    ▒ ░░    ▒▒   ▓▒█░░▓  ░ ▒▓ ░▒▓░░░ ▒░ ░
░ ░▒  ░ ░  ░ ▒ ▒░ ░ ░ ▒  ░ ▒ ░    ░      ▒   ▒▒ ░ ▒ ░  ░▒ ░ ▒░ ░ ░  ░
░  ░  ░  ░ ░ ░ ▒    ░ ░    ▒ ░  ░        ░   ▒    ▒ ░  ░░   ░    ░   
      ░      ░ ░      ░  ░ ░                 ░  ░ ░     ░        ░  ░
    """)
def gameOver():
  print("""
    ▄████  ▄▄▄       ███▄ ▄███▓▓█████ 
 ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀ 
▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███   
░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄ 
░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒
 ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░
  ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░
░ ░   ░   ░   ▒   ░      ░      ░   
      ░       ░  ░       ░      ░  ░
                                    
 ▒█████   ██▒   █▓▓█████  ██▀███    
▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒  
▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒  
▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄    
░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒  
░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░  
  ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░  
░ ░ ░ ▒       ░░     ░     ░░   ░   
    ░ ░        ░     ░  ░   ░       
              ░                     """)

def showInstructions():
  print("""Welcome to dungeon solitaire! The goal of the game is to
journey into the dungeon, collect treasure, and escape alive. The 
maximum possible score is 100 points and collecting all four kings.
The game is based on the card game by Matthew Lowes, which uses one
player and a deck of standard playing cards.

In the dungeon, you'll encounter monsters, traps, and doors.
To pass an encounter, you must draw a card equal to or higher than
the encounter card. You must somehow beat monsters, but traps and doors
only give you one chance. If you run out of health or playable cards, 
you lose.

If you encounter a trap and beat it, you may collect its treasure.
Any treasure found on a move can be collected after passing a move.
To pass some encounters, you may drop a treasure to escape.

All aces are torches, so if you burn all four, you will die.
However, if you collected the Scroll of Light as treasure, you
should use that to survive after you've burnt four torches.

You may collect powerups (Jacks) immediately after playing them.
To use it, you can choose to use a powerup instead of drawing
another card. You will discard the powerup and beat the encounter.

Once you have returned safely, you may count up your treasure and
view your past moves. Much of the game relies on luck, but if
you play your cards right, you will have better odds!
""")
  

def showCredits():
  # give credit to creator of game
  print("""This game was based entirely on Matthew Lowes' game
Dungeon Solitaire: Tomb of Four Kings. To read instructions for the 
original card game, visit: 
https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
  """)

def youWin():
  print("""
▓██   ██▓ ▒█████   █    ██    
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒   
  ▒██ ██░▒██░  ██▒▓██  ▒██░   
  ░ ▐██▓░▒██   ██░▓▓█  ░██░   
  ░ ██▒▓░░ ████▓▒░▒▒█████▓    
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒    
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░    
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░    
 ░ ░         ░ ░     ░        
 ░ ░                          
 █     █░ ██▓ ███▄    █  ▐██▌ 
▓█░ █ ░█░▓██▒ ██ ▀█   █  ▐██▌ 
▒█░ █ ░█ ▒██▒▓██  ▀█ ██▒ ▐██▌ 
░█░ █ ░█ ░██░▓██▒  ▐▌██▒ ▓██▒ 
░░██▒██▓ ░██░▒██░   ▓██░ ▒▄▄  
░ ▓░▒ ▒  ░▓  ░ ▒░   ▒ ▒  ░▀▀▒ 
  ▒ ░ ░   ▒ ░░ ░░   ░ ▒░ ░  ░ 
  ░   ░   ▒ ░   ░   ░ ░     ░ 
    ░     ░           ░  ░    
                              
  """)