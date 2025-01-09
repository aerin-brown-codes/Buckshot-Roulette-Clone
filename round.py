import random

class Round:
    def __init__(self, players):
        self.load_gun()

        lives = random.randint(2, 6)
        self.living_players = players
        for i in range(len(players) - 1):
            players[i].set_next_player(players[i + 1])
            players[i].new_round(lives, [])
        players[-1].set_next_player(players[0])
        players[-1].new_round(lives, [])

    def load_gun(self):
        self.live = random.randint(1, 4)
        self.blanks = random.randint(1, 4)
        print(f"{str(self.live)} live, {str(self.blanks)} blanks.")
        self.gun = [True] * self.live + [False] * self.blanks
        random.shuffle(self.gun)

    def fire_gun(self, target):
        bullet = self.gun.pop()
        if bullet:
            print("BANG!")
            self.live -= 1
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
            return True
        else:
            print("Click.")
            self.blanks -= 1
            return False
    
    def run_game(self):
        cur_player = self.living_players[0]
        while len(self.living_players) > 1:
            if len(self.gun) == 0:
                self.load_gun()
            print()
            for player in self.living_players:
                player.display()
            print(cur_player.name + "'S TURN")
            move_on = cur_player.take_turn(self)
            if move_on:
                cur_player = cur_player.next_player
        print(self.living_players[0].name + " WINS")

    
    def display_state(self):
        for player in self.living_players:
            player.display()
            print()
    