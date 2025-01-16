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
        bullet = False
        item_names = [item.name for item in self.items]
        while game.blanks != 0 and "Beer" in item_names:
            for item in self.items:
                if item.name == "Beer":
                    item.use(game, self)
                    item_names.remove("Beer")
                    break
        while self.lives < game.lives and "Cigarettes" in item_names:
            for item in self.items:
                if item.name == "Cigarettes":
                    item.use(game, self)
                    item_names.remove("Cigarettes")
                    break        
        if "Magnifying Glass" in item_names:
            known = True
            for item in self.items:
                if item.name == "Magnifying Glass":
                    bullet = item.use(game, self)
                    break
        if (game.blanks > game.live or (known and not bullet)) and "Inverter" in item_names:
            known = True # Technically, no this is not a guarantee. The dealer is making an assumption
            bullet = True
            for item in self.items:
                if item.name == "Inverter":
                    item.use(game, self)
                    break

        if "Hand Saw" in item_names and (bullet or game.live > game.blanks):
            for item in self.items:
                if item.name == "Hand Saw":
                    item.use(game, self)
                    break
        
        if game.living_players[-1] == self:
            opponents = [game.living_players[:-1]]
        else:
            dealer_i = game.living_players.index(self)
            opponents = game.living_players[dealer_i + 1:] + game.living_players[:dealer_i]
        for player in opponents:
            if "Handcuffs" in item_names and not player.cuffed:
                for item in self.items:
                    if item.name == "Handcuffs":
                        item.use(game, self)
                        item_names.remove("Handcuffs")
                        break
        
        if known:
            if bullet:
                print("The DEALER points the shotgun at you.")
                target = self
                while target == self:
                    target = random.choice(game.living_players)
                game.fire_gun(target)
                return True
            else:
                print("The DEALER turns the shotgun on himself.")
                result = game.fire_gun(self)
                return result
        else:
            if game.live > game.blanks:
                print("The DEALER points the shotgun at you.")
                target = self
                while target == self:
                    target = random.choice(game.living_players)
                game.fire_gun(target)
                return True
            else:
                print("The DEALER turns the shotgun on himself.")
                result = game.fire_gun(self)
                return result