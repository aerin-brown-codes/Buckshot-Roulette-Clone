class Player:
    def __init__(self, name):
        self.lives = 0
        self.items = []
        self.name = name
        self.next_player = None
    
    def set_next_player(self, next_player):
        self.next_player = next_player

    def new_round(self, lives, items):
        self.items = items
        self.lives = lives
    
    def display(self):
        print(self.name + ": " + "O" * self.lives)
        # Item display
    
    def take_turn(self, game):
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
