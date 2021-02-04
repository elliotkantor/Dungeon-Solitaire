# dungeon solitaire - recreation of the solitaire game 
# instructions at: https://matthewlowes.files.wordpress.com/2015/06/dungeon-solitaire.pdf
import cards

deck = [cards.Card(value, suit) for value in cards.values for suit in cards.suits]
deck.append(cards.Card("Black", "Joker"))

for card in deck:
    print(card.name)