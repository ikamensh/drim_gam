from mechanics.actives import Active, CellTargeting, SingleUnitTargeting
from mechanics.actives import Costs
from mechanics.combat import Attack
from content.actives.conditions import proximity_condition

import my_globals


std_attack_cost = Costs(stamina=1)


def attack_direct_callback(active  :Active, targeting  :SingleUnitTargeting):
    Attack.attack(source=active.owner, target=targeting.unit)

def attack_on_cell_callback(active  :Active, targeting  :CellTargeting):
    unit_on_target_cell = my_globals.the_game.get_unit_at(targeting.cell)
    Attack.attack(source=active.owner, target=unit_on_target_cell)

attack_unit_active = Active(SingleUnitTargeting, proximity_condition(1), std_attack_cost, [attack_direct_callback])
attack_cell_active = Active(CellTargeting, proximity_condition(1), std_attack_cost, [attack_on_cell_callback])



