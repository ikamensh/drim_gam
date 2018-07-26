from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from content.actives.callbacks import move_on_target_cell, turn_ccw_callback, turn_cw_callback
from battlefield import Cell
from content.actives.conditions import proximity_condition, within_angle, between_angles, target_cell_empty
from content.actives.temp_simulation import sim_move_on_target_cell, sim_turn_ccw, sim_turn_cw




std_attack_cost = Cost(stamina=1)

move_forward = Active(Cell,
                        [proximity_condition(1), within_angle(0), target_cell_empty],
                        Cost(stamina=1, readiness=0.3),
                        [move_on_target_cell],
                        [ActiveTags.MOVEMENT],
                        "move forward",
                      simulate=sim_move_on_target_cell)

move_diag = Active(Cell,
                    [proximity_condition(1.5), between_angles(1,89), target_cell_empty],
                    Cost(stamina=2, readiness=0.6),
                    [move_on_target_cell],
                    [ActiveTags.MOVEMENT],
                    "move forward diagonally",
                      simulate=sim_move_on_target_cell)

move_side = Active(Cell,
                    [proximity_condition(1), between_angles(89,91), target_cell_empty],
                    Cost(stamina=1, readiness=0.5),
                    [move_on_target_cell],
                    [ActiveTags.MOVEMENT],
                    "move to the side",
                      simulate=sim_move_on_target_cell)

move_back = Active(Cell,
                    [proximity_condition(1), between_angles(180,180), target_cell_empty],
                    Cost(stamina=1, readiness=0.6),
                    [move_on_target_cell],
                    [ActiveTags.MOVEMENT],
                    "move back",
                      simulate=sim_move_on_target_cell)

turn_cw = Active(None,
                 None,
                 Cost(readiness=0.1),
                 [turn_cw_callback],
                 [ActiveTags.TURNING],
                 "turn CW",
                      simulate=sim_turn_cw)

turn_ccw = Active(None,
                 None,
                 Cost(readiness=0.1),
                 [turn_ccw_callback],
                 [ActiveTags.TURNING],
                  "turn CCW",
                    simulate=sim_turn_ccw)


std_movements = [move_back, move_diag, move_forward, move_side]