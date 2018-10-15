from game_objects.items import Blueprint
from game_objects.items import BodyArmor, ArmorTypes
from game_objects.items.blueprints.types.ArmorTypes import material_type_from_armor_type
from mechanics.damage import Armor


class ArmorBlueprint(Blueprint):
    armor_per_rarity = 30


    def __init__(self, name, target_item_type, rarity, armor=None, durability=None, material_count = 8):
        assert target_item_type in ArmorTypes
        assert armor is None or isinstance(armor, Armor)
        super().__init__(name, target_item_type, rarity, durability, material_type=material_type_from_armor_type[target_item_type], material_count=material_count)
        self.armor = armor or Armor(rarity * ArmorBlueprint.armor_per_rarity)

    def to_item(self, material, quality, *, game=None):
        assert material.material_type is self.material_type
        total_rarity = material.rarity * quality.rarity *self.rarity
        armor = Armor(armor_dict={t: v*total_rarity for t, v in self.armor.items()} )
        durability = self.item_durability(total_rarity)
        full_name = f"{quality.name} {self.name} of {material}"
        return BodyArmor(full_name, armor, durability, blueprint=self,
                         material=material, quality=quality, game=game)

    def __repr__(self):
        return f"{self.name} blueprint"


