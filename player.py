import random
class Player:
    def __init__(self, name):
        self.lives = 0
        self.items = []
        self.name = name
        self.next_player = None
        self.cuffed = False
    
    def set_next_player(self, next_player):
        self.next_player = next_player

    def new_round(self, lives):
        self.items = []
        self.lives = lives

    def add_items(self, items):
        self.items.extend(items)
    
    def display(self):
        print(self.name + ": " + "O" * self.lives)
        if len(self.items) > 0:
            print(", ".join([item.name for item in self.items]))
    
    def take_turn(self, game):
        while len(self.items) > 0:
            i = 1
            items = []
            for item in self.items:
                print(str(i) + ". " + item.name)
                items.append(item)
                i += 1
            print(str(i) + ". Shotgun")
            target_i = int(input("Select an item. (Enter a number) "))
            if target_i == len(items) + 1:
                break
            else:
                items[target_i - 1].use(game, self)
        if len(game.gun) == 0:
            return False
        targets = []
        i = 1
        for player in game.living_players:
            if player != self:
                print (str(i) + ". " + player.name)
                targets.append(player)
                i += 1
        print(str(i) + ". Yourself")
        target_i = int(input("Aim the shotgun. (Enter a number) "))
        if target_i == len(game.living_players): #targeted self
            result = game.fire_gun(self)
            if result:
                return True
            else:
                return False
        else:
            target = targets[target_i - 1]
            game.fire_gun(target)
            return True

class Dealer(Player):
    def __init__(self):
        super().__init__("DEALER")

    def take_turn(self, game):
        if game.live > game.blanks:
            target = self
            while target == self:
                target = random.choice(game.living_players)
            game.fire_gun(target)
            return True
        else:
            result = game.fire_gun(self)
            return result