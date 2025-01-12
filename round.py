import random
from time import sleep
import item

class Round:
    def __init__(self, players):
        self.lives = random.randint(2, 6)
        self.items_per_load = random.randint(1, 4)
        print(str(self.items_per_load) + " items. " + str(self.items_per_load) + " more every reload.")

        self.living_players = players
        for i in range(len(players) - 1):
            players[i].set_next_player(players[i + 1])
            players[i].new_round(self.lives)
        players[-1].set_next_player(players[0])
        players[-1].new_round(self.lives)

        self.load_gun()

        self.sawed = False

    def load_gun(self):
        self.live = random.randint(1, 4)
        self.blanks = random.randint(1, 4)
        print(f"{str(self.live)} live, {str(self.blanks)} blank.")
        self.gun = [True] * self.live + [False] * self.blanks
        random.shuffle(self.gun)
        
        for player in self.living_players:
            player.add_items([item.Item.open_box() for i in range(self.items_per_load)])

    def fire_gun(self, target):
        bullet = self.gun.pop()
        if bullet:
            print("\nBANG!")
            self.live -= 1
            target.lives -= 1
            if self.sawed and target.lives != 0:
                target.lives -= 1
            if target.lives == 0:
                if target == self.living_players[-1]:
                    self.living_players[-2].set_next_player(self.living_players[0])
                elif target == self.living_players[0]:
                    self.living_players[-1].set_next_player(self.living_players[1])
                else:
                    index = self.living_players.index(target)
                    self.living_players[index - 1].set_next_player(self.living_players[index + 1])   
                self.living_players.remove(target)      
            self.sawed = False      
            return True
        else:
            print("\nClick.")
            self.blanks -= 1
            self.sawed = False
            return False
    
    def run_game(self):
        cur_player = self.living_players[0]
        while len(self.living_players) > 1:
            if len(self.gun) == 0:
                print()
                self.load_gun()
                sleep(1)
            print()
            for player in self.living_players:
                player.display()
            print(cur_player.name + "'S TURN")
            move_on = cur_player.take_turn(self)
            if move_on:
                cur_player = cur_player.next_player
                if cur_player.cuffed:
                    cur_player.cuffed = False
                    cur_player = cur_player.next_player
            sleep(1)
        print(self.living_players[0].name + " WINS")

    
    def display_state(self):
        for player in self.living_players:
            player.display()
            print()
    