from battlefield.Vision import Vision
from battlefield.Facing import Facing
from battlefield.Cell import Cell
import pytest


f = Facing
@pytest.fixture(params=[f.NORTH, f.EAST, f.SOUTH, f.WEST])
def var_facing(request) -> complex:
    return request.param


@pytest.mark.parametrize('prc', [1, 10, 15, 70, 1000])
def test_symmetric(huge_game, hero, prc, var_facing):
    hero_c_coords = 30+30j
    hero.prc_base.base = prc

    assert hero.prc == prc

    huge_game.add_unit(hero, hero_c_coords, facing=var_facing)

    v = huge_game.battlefield.vision
    cells_seen = v.std_seen_cells(hero)

    cells_to_right = set()
    cells_to_left = set()
    for c in cells_seen:
        vec = c.complex - hero_c_coords
        deg, ccw = Cell.angle_between(vec, var_facing)
        if deg > 1e-3:
            collection = cells_to_right if ccw else cells_to_left
            collection.add(c)

    assert len(cells_to_left) == len(cells_to_right)
    pytest.skip("TODO: TEST INCOMPLETE. DIFFERENT SIGHT RANGES ARE NOT TESTED.")




def test_visibility(game_hvsp, hero):

    bf = game_hvsp.battlefield
    bf.unit_locations = {}
    bf.place(hero, Cell(1,1), Facing.SOUTH)

    vision = Vision(bf)
    cells_seen = vision.std_seen_cells(hero)

    assert Cell(0,0) not in cells_seen
    assert Cell(7,7) not in cells_seen
    assert Cell(7,0) not in cells_seen
    assert Cell(0,7) not in cells_seen

    assert Cell(1,1) in cells_seen
    cell = Cell(1,int(1+hero.sight_range))
    print(cells_seen)
    assert cell in cells_seen
    cell = Cell(1+int(hero.sight_range),1)
    assert cell not in cells_seen


def test_borders(game_hvsp, hero):

    bf = game_hvsp.battlefield
    bf.unit_facings[hero] = Facing.SOUTH

    bf.move(hero, Cell(1, 1))
    vision = Vision(bf)
    cells_seen_before = vision.std_seen_cells(hero)


    bf.move(hero, Cell(7, 7))
    cells_seen_after = vision.std_seen_cells(hero)

    assert len(cells_seen_after) < len(cells_seen_before)
    assert Cell(8,8) not in cells_seen_after

def test_direction(game_hvsp, hero):

    bf = game_hvsp.battlefield
    bf.unit_facings[hero] = Facing.SOUTH


    vision = Vision(bf)
    bf.unit_locations = {}
    bf.place(hero, Cell(4, 4))
    cells_seen_before = vision.std_seen_cells(hero)


    bf.unit_facings[hero] = Facing.SOUTH
    cells_seen_after = vision.std_seen_cells(hero)

    assert len(cells_seen_after) == len(cells_seen_before)
    assert cells_seen_before != cells_seen_after






