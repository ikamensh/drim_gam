from game_objects.battlefield_objects import BattlefieldObject
from mechanics.damage import Resistances, Armor
from game_objects.attributes import DynamicParameter
from mechanics.events import ObstacleDestroyedEvent
from ui.sounds import sound_maps


class Obstacle(BattlefieldObject):

    last_uid = 0
    sound_map = sound_maps.std_sound_map #TODO specific obstacle sound maps

    health = DynamicParameter("max_health", [ObstacleDestroyedEvent])

    def __init__(self, name, max_health, armor, resists, icon):
        Obstacle.last_uid += 1
        self.uid = Obstacle.last_uid

        self.name = name
        self.max_health = max_health
        self.armor = armor if isinstance(armor,Armor) else Armor(base_value=armor)
        self.resists = resists or Resistances()
        self.melee_evasion = 0
        self.icon = icon
        self.alive = True
        self.last_damaged_by = None
        self.is_obstacle = True


    def lose_health(self, dmg_amount, source=None):
        assert dmg_amount >= 0
        if source:
            self.last_damaged_by = source
        self.health -= dmg_amount