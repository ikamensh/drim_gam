from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame
from game_objects.battlefield_objects import Unit
from single_player.Shop import Shop


class Adventure:
    def __init__(self, base_type, first_mission):
        self.character = Character(base_type)
        self.first_mission = first_mission

    def start(self):
        Shop.enter_shop(self.character)
        for dungeon in self.first_mission:
            game = SimGame.start_dungeon(dungeon, Unit(self.character.base_type))
            result = game.loop()
            if result != "VICTORY":
                print("you have lost the game.")
                return "DEFEAT"
            else:
                Shop.enter_shop(self.character)

        return "VICTORY"




