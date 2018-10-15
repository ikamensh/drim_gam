from mechanics.events import AttackEvent
from battlefield.Cell import Cell
from battlefield.Facing import Facing

def test_backstab(empty_game, hero, pirate):

    bf = empty_game.battlefield
    empty_game.add_unit(hero, Cell(1,1))
    empty_game.add_unit(pirate, Cell(1,2))


    bf.unit_facings[hero] = Facing.SOUTH
    bf.unit_facings[pirate] = Facing.SOUTH

    ae = AttackEvent(pirate, hero)

    assert not ae.is_backstab
    assert ae.is_blind

    bf.unit_facings[pirate] = Facing.NORTH
    ae = AttackEvent(pirate, hero)
    assert not ae.is_backstab
    assert not ae.is_blind

    bf.unit_facings[hero] = Facing.NORTH
    ae = AttackEvent(pirate, hero)
    assert ae.is_backstab
    assert not ae.is_blind

