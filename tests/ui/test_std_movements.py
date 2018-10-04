from content.actives.std_movements import move_forward, move_back, move_diag, move_side
from mechanics.events import ActiveEvent, MovementEvent
from battlefield.Facing import Facing
from battlefield.Battlefield import Cell
import pytest

@pytest.fixture()
def collect_events(empty_game):
    events = []
    empty_game.events_platform.process_event = lambda x: events.append(x)
    yield events

facings = [Facing.NORTH, Facing.EAST, Facing.SOUTH, Facing.WEST]

def check_contains_right_action_and_cell(collect_events, action, cell):
    activated = False
    assert collect_events
    for e in collect_events:
        if isinstance(e, ActiveEvent):
            if e.active.name == action.name:
                activated = True
            assert e.targeting == cell

    assert activated

@pytest.mark.parametrize("facing", facings)
def test_can_move_forward(empty_game, hero, collect_events, facing):
    pos = empty_game.battlefield.unit_locations[empty_game.the_hero]
    empty_game.battlefield.unit_facings[empty_game.the_hero] = facing

    target_cell = Cell.from_complex(pos.complex + facing)

    empty_game.ui_order( target_cell.x, target_cell.y )
    check_contains_right_action_and_cell(collect_events, move_forward, target_cell)



@pytest.mark.parametrize("facing", facings)
def test_can_move_back(empty_game, hero, collect_events, facing):
    pos = empty_game.battlefield.unit_locations[empty_game.the_hero]
    empty_game.battlefield.unit_facings[empty_game.the_hero] = facing

    target_cell = Cell.from_complex(pos.complex - facing)

    empty_game.ui_order( target_cell.x, target_cell.y )

    check_contains_right_action_and_cell(collect_events, move_back, target_cell)



@pytest.mark.parametrize("facing", facings)
def test_can_move_left(empty_game, hero, collect_events, facing):
    pos = empty_game.battlefield.unit_locations[empty_game.the_hero]
    empty_game.battlefield.unit_facings[empty_game.the_hero] = facing

    target_cell = Cell.from_complex(pos.complex + facing * 1j)

    empty_game.ui_order( target_cell.x, target_cell.y )

    check_contains_right_action_and_cell(collect_events, move_side, target_cell)



@pytest.mark.parametrize("facing", facings)
def test_can_move_right(empty_game, hero, collect_events, facing):
    pos = empty_game.battlefield.unit_locations[empty_game.the_hero]
    empty_game.battlefield.unit_facings[empty_game.the_hero] = facing

    target_cell = Cell.from_complex(pos.complex + facing * -1j)

    empty_game.ui_order( target_cell.x, target_cell.y )

    check_contains_right_action_and_cell(collect_events, move_side, target_cell)


@pytest.mark.parametrize("facing", facings)
def test_can_move_diag_left(empty_game, hero, collect_events, facing):

    pos = empty_game.battlefield.unit_locations[empty_game.the_hero]
    empty_game.battlefield.unit_facings[empty_game.the_hero] = facing

    target_cell = Cell.from_complex(pos.complex + facing * (1+1j) )
    empty_game.ui_order( target_cell.x, target_cell.y )
    check_contains_right_action_and_cell(collect_events, move_diag, target_cell)


@pytest.mark.parametrize("facing", facings)
def test_can_move_diag_right(empty_game, hero, collect_events, facing):
    pos = empty_game.battlefield.unit_locations[empty_game.the_hero]
    empty_game.battlefield.unit_facings[empty_game.the_hero] = facing

    target_cell = Cell.from_complex(pos.complex + facing * (1 - 1j))
    empty_game.ui_order(target_cell.x, target_cell.y)
    check_contains_right_action_and_cell(collect_events, move_diag, target_cell)



