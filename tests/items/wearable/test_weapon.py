

def test_weapon_gives_damage(hero, weapon):
    damage_before = hero.get_melee_weapon().damage

    hero.equipment["hands"] = weapon

    damage_after = hero.get_melee_weapon().damage

    assert damage_before is not damage_after


