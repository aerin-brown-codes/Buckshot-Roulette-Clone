import player as p
from round import Round
import random

players = []
num_players = int(input("How many high rollers at the table? "))
for i in range(num_players):
    name = input("Player " + str(i + 1) + ", please sign the general release form: ")
    players.append(p.Player(name.upper()))

if len(players) == 1:
    print("The DEALER will play with you.")
    players.append(p.Dealer())

while True:
    # Setup
    game = Round(players.copy())
    game.run_game()
    again = input("Double or nothing? Y/N: ")
    if again.upper() == "N":
        break
    

