from mechanics.actives import ActiveTags


def test_unit_util_positive(hero, pirate):
    assert hero.utility > 0
    assert pirate.utility > 0

def test_more_hp_is_better(game, hero):

    utility_initial = game.utility(game.fractions[hero])
    hero.max_health += 100
    assert utility_initial < game.utility(game.fractions[hero])

def test_invertion(game, hero):
    pirate = [unit for unit in game.battlefield.unit_locations if unit is not hero][0]

    utility_initial = game.utility(game.fractions[pirate])
    hero.max_health += 100
    assert utility_initial > game.utility(game.fractions[pirate])

def test_less_hp_is_worse(game, hero):

    utility_initial = game.utility(game.fractions[hero])
    hero.max_health -= 100
    assert utility_initial > game.utility(game.fractions[hero])

def test_double_inversion(game, hero):

    pirate = [unit for unit in game.battlefield.unit_locations if unit is not hero][0]
    utility_initial = game.utility(game.fractions[pirate])
    hero.max_health -= 100
    assert utility_initial < game.utility(game.fractions[pirate])

def test_more_mana_is_better(game, hero):
    utility_initial = game.utility(game.fractions[hero])
    hero.max_mana += 100
    assert utility_initial < game.utility(game.fractions[hero])


def test_more_stamina_is_better(game, hero):
    utility_initial = game.utility(game.fractions[hero])
    hero.max_stamina += 100
    assert utility_initial < game.utility(game.fractions[hero])


def test_more_readiness_is_better(game, hero):
    utility_initial = game.utility(game.fractions[hero])
    hero.readiness += 100
    assert utility_initial < game.utility(game.fractions[hero])




def test_hurt_negative_delta(game, hero, no_chances, imba_ability):

    old_abilities = set(hero.actives)

    hero.give_active(imba_ability)
    hero.readiness += 10

    ability = list(set(hero.actives)-old_abilities)[0]

    delta = game.delta_util(ability, hero)

    assert delta < 0

def test_small_hurt_negative_delta(game, hero, no_chances, tiny_imba_ability):

    old_abilities = set(hero.actives)

    hero.give_active(tiny_imba_ability)
    hero.readiness += 10

    ability = list(set(hero.actives)-old_abilities)[0]

    delta = game.delta_util(ability, hero)

    assert delta < 0


def test_pirates_cry_too(minigame, pirate, no_chances, imba_ability):

    old_abilities = set(pirate.actives)

    pirate.give_active(imba_ability)
    pirate.readiness += 10

    ability = list(set(pirate.actives) - old_abilities)[0]

    delta = minigame.delta_util(ability, pirate)

    assert delta < 0

def test_pirates_cry_too_a_little(minigame, pirate, no_chances, tiny_imba_ability):

    old_abilities = set(pirate.actives)

    pirate.give_active(tiny_imba_ability)
    pirate.readiness += 10

    ability = list(set(pirate.actives) - old_abilities)[0]

    delta = minigame.delta_util(ability, pirate)

    assert delta < 0


def test_positions_can_go_out_of_utility(game):
    n_checked = 0

    for unit in game.battlefield.unit_locations:
        # fraction = game.fractions[unit]
        choices = game.get_all_choices(unit)

        for c in choices:
            active, target = c
            if ActiveTags.MOVEMENT in active.tags:
                n_checked += 1

                delta = game.delta_util(active, target, use_positions=False)
                assert delta == 0


    assert n_checked > 0
