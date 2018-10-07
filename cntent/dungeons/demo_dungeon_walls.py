from battlefield.Battlefield import Cell
from cntent.base_types import pirate_basetype, mud_golem_basetype, mud_wall
from game_objects.battlefield_objects import Unit
from game_objects.dungeon.Dungeon import Dungeon

pirate_band = [Unit(pirate_basetype) for i in range(3)]
locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

unit_locations = {pirate_band[i]: locations[i] for i in range(3)}

wall_x = 8
for wall_y in range(0,9):
    unit_locations[mud_wall.clone()] = Cell(wall_x, wall_y)

unit_locations[Unit(mud_golem_basetype)] = Cell(11, 0)


walls_dungeon = Dungeon(unit_locations, 12, 12, hero_entrance=Cell(3, 4))

