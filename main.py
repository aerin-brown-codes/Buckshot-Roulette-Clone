import player as p
from round import Round
import random

dealer = p.Dealer()

name = input("Please sign the general release form: ")
player = p.Player(name.upper())

while True:
    # Setup
    game = Round([player, dealer])
    game.run_game()
    again = input("Double or nothing? Y/N: ")
    if again.upper() == "N":
        break
    

