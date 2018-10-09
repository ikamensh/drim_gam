from cntent.items.materials.materials import Stones, Metals, Leathers
from cntent.items.blueprints.weapons import weapons as bp_weapons
from cntent.items.blueprints.armor import body_armor as bp_armor
from cntent.items.QualityLevels import QualityLevels

axe_ancient = bp_weapons.primordial_great_axe.to_item(Stones.flintstone, QualityLevels.SUPERIOR)

sword_cheap = bp_weapons.short_sword.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
axe_cheap = bp_weapons.axe.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
dagger_cheap = bp_weapons.dagger.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
spear_cheap = bp_weapons.spear.to_item(Metals.bronze, QualityLevels.PRIMITIVE)
hammer_cheap = bp_weapons.hammer.to_item(Metals.bronze, QualityLevels.PRIMITIVE)

sword_superior = bp_weapons.short_sword.to_item(Metals.iron, QualityLevels.SUPERIOR)
axe_superior = bp_weapons.axe.to_item(Metals.iron, QualityLevels.SUPERIOR)
spear_superior = bp_weapons.spear.to_item(Metals.iron, QualityLevels.SUPERIOR)
dagger_superior = bp_weapons.dagger.to_item(Metals.iron, QualityLevels.SUPERIOR)
hammer_superior = bp_weapons.hammer.to_item(Metals.iron, QualityLevels.SUPERIOR)


elven_skimitar = bp_weapons.scimitar.to_item(Metals.mithril, QualityLevels.MASTERPIECE)
smiths_hammer = bp_weapons.hammer.to_item(Metals.steel, QualityLevels.SUPERIOR)


jacket_cheap = bp_armor.pirate_jacket.to_item(Leathers.skin, QualityLevels.PRIMITIVE)
jacket_usual = bp_armor.leather_outfit.to_item(Leathers.thick_skin, QualityLevels.SUPERIOR)

jacket_trollhide = bp_armor.leather_outfit.to_item(Leathers.troll_skin, QualityLevels.USUAL)
scalemail_inferior = bp_armor.scalemail.to_item(Metals.iron, QualityLevels.PRIMITIVE)
cuirass_usual = bp_armor.cuirass.to_item(Metals.steel, QualityLevels.USUAL)

