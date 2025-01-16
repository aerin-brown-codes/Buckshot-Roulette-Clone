import random

class Item:
    def __init__(self, name):
        self.name = name

    def use(self, game, user):
        user.items.remove(self)

    @staticmethod
    def open_box():
        selection = random.randint(1, 6)
        if selection == 1:
            return MagnifyingGlass()
        elif selection == 2:
            return Cigarettes()
        elif selection == 3:
            return Beer()
        elif selection == 4:
            return Inverter()
        elif selection == 5:
            return Handcuffs()
        elif selection == 6:
            return HandSaw()

class MagnifyingGlass(Item):
    def __init__(self):
        super().__init__("Magnifying Glass")

    def use(self, game, user):
        super().use(game, user)
        if game.gun[-1]:
            print("You see a live round in the chamber.")
        else:
            print("You see a blank round in the chamber.")
        return game.gun[-1]
    
class Cigarettes(Item):
    def __init__(self):
        super().__init__("Cigarettes")
    
    def use(self, game, user):
        super().use(game, user)
        if user.lives < game.lives:
            user.lives += 1
            return True
        else:
            return False
        
class Beer(Item):
    def __init__(self):
        super().__init__("Beer")
    
    def use(self, game, user):
        super().use(game, user)
        racked = game.gun.pop()
        print("SH-SHCK")
        if racked:
            print("A live shell falls out.")
            return True
        else:
            print("A blank shell falls out.")
            return False
        
class Inverter(Item):
    def __init__(self):
        super().__init__("Inverter")
    
    def use(self, game, user):
        super().use(game, user)
        game.gun[-1] = not game.gun[-1]
        if game.gun[-1]:
            game.live += 1
            game.blanks -= 1
            return True
        else:
            game.blanks += 1
            game.live -= 1
            return False
    
class Handcuffs(Item):
    def __init__(self):
        super().__init__("Handcuffs")
    
    def use(self, game, user):
        super().use(game, user)
        if user.name != "DEALER":
            targets = []
            i = 1
            for player in game.living_players:
                if player != self:
                    print (str(i) + ". " + player.name)
                    targets.append(player)
                    i += 1
            target_i = int(input("Cuff a player. (Enter a number) "))
            target = targets[target_i - 1]
            target.cuffed = True
            return True
        else:
            if game.living_players[-1] == self:
                opponents = [game.living_players[:-1]]
            else:
                dealer_i = game.living_players.index(self)
                opponents = game.living_players[dealer_i + 1:] + game.living_players[:dealer_i]
            for player in opponents:
                if not player.cuffed:
                    player.cuffed = True

class HandSaw(Item):
    def __init__(self):
        super().__init__("Hand Saw")
    
    def use(self, game, user):
        super().use(game, user)
        game.sawed = True
        return True